from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Role, Website
from .serializers import UserSerializer, RoleSerializer, WebsiteSerializer
from .permissions import IsAdmin, IsEditor, IsViewer, IsOwnerOrAdmin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(View):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'registration/signup.html', {'form': form})
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
class LogoutView(View):
    def get(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class WebsiteListCreateView(generics.ListCreateAPIView):
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role and self.request.user.role.name == 'Admin':
            return Website.objects.all()
        return Website.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WebsiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [IsOwnerOrAdmin]

# Template Views
class HomeView(View):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return render(request, 'home.html')

class WebsiteDeleteView(View):
    def post(self, request, pk):
        website = get_object_or_404(Website, pk=pk, owner=request.user)
        website.delete()
        return HttpResponseRedirect(reverse('website-list-view'))

from django import forms 
class WebsiteForm(forms.Form):
    title = forms.CharField(max_length=100)
    business_type = forms.CharField(max_length=100)
    industry = forms.CharField(max_length=100)

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class WebsiteCreateView(View):
    def get(self, request):
        form = WebsiteForm()
        return render(request, 'website/create.html', {'form': form})

    def post(self, request):
        form = WebsiteForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            business_type = form.cleaned_data['business_type']
            industry = form.cleaned_data['industry']

            # Generate content using the AI model (Gemini)
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(
                    f"""Generate complete website content in JSON format for a {business_type} 
                    business in the {industry} industry called {title}. Include:
                    - hero: {{headline, subheadline}}
                    - about: (2-3 paragraphs)
                    - services: [array of 3 services with name and description]
                    - contact: {{email, phone, address}}
                    - features: [array of 3 features]
                    
                    Return ONLY valid JSON, no markdown or additional text.
                    """
                )
                
                # Clean and parse the response
                json_str = response.text.replace('```json', '').replace('```', '').strip()
                content = json.loads(json_str)
                
                # Create the Website instance with generated content
                website = Website.objects.create(
                    owner=request.user,
                    title=title,
                    business_type=business_type,
                    industry=industry,
                    content=content  # Save the generated content as a JSON field or text field
                )
                
                return redirect('website-list-view')  # Redirect to the list of websites
            except Exception as e:
                return render(request, 'website/create.html', {'form': form, 'error': str(e)})

        return render(request, 'website/create.html', {'form': form})



class WebsiteEditView(View):
    def get(self, request, pk):
        website = get_object_or_404(Website, pk=pk, owner=request.user)
        return render(request, 'website/edit.html', {'website': website})

class WebsiteListView(View):
    def get(self, request):
        websites = Website.objects.filter(owner=request.user)
        return render(request, 'website/list.html', {'websites': websites})

class WebsitePreviewView(View):
    def get(self, request, pk):
        website = get_object_or_404(Website, pk=pk)
        return render(request, 'website/preview.html', {'website': website})

class RoleManagementView(View):
    def get(self, request):
        if not request.user.role or request.user.role.name != 'Admin':
            return render(request, '403.html', status=403)
        roles = Role.objects.all()
        return render(request, 'admin/role_management.html', {'roles': roles})

class UserManagementView(View):
    def get(self, request):
        if not request.user.role or request.user.role.name != 'Admin':
            return render(request, '403.html', status=403)
        users = User.objects.all()
        return render(request, 'admin/user_management.html', {'users': users})
    

from .forms import AIGeneratorForm
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
class AIGeneratorView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        form = AIGeneratorForm()
        return render(request, 'ai_generator.html', {'form': form})
    def post(self, request):
        try:
            business_type = request.data.get('business_type')
            industry = request.data.get('industry')
            title = request.data.get('title')
            
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(
                f"""Generate complete website content in JSON format for a {business_type} 
                business in the {industry} industry called {title}. Include:
                - hero: {{headline, subheadline}}
                - about: (2-3 paragraphs)
                - services: [array of 3 services with name and description]
                - contact: {{email, phone, address}}
                - features: [array of 3 features]
                
                Return ONLY valid JSON, no markdown or additional text.
                """
            )
            
            # Clean and parse the response
            json_str = response.text.replace('```json', '').replace('```', '').strip()
            content = json.loads(json_str)
            
            return Response({
                "id": f"msg_{os.urandom(8).hex()}",
                "type": "message",
                "role": "assistant",
                "content": [{
                    "type": "output_text",
                    "text": content,
                    "annotations": []
                }]
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)