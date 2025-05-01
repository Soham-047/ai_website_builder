from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, Website
import openai
import os
from dotenv import load_dotenv
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, Website
import google.generativeai as genai
import json

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class WebsiteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Website
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def generate_ai_content(self, business_type, industry):
        prompt = f"""
        Generate website content for a {business_type} business in the {industry} industry.
        Include:
        - Hero section with headline and subheadline
        - About section with 2-3 paragraphs
        - Services section with 3 services
        - Contact section with basic info
        
        Return the content in JSON format with these keys:
        hero, about, services, contact
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates website content in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def create(self, validated_data):
        request = self.context.get('request')
        business_type = validated_data.get('business_type')
        industry = validated_data.get('industry')
        
        # Generate AI content
        try:
            ai_content = self.generate_ai_content(business_type, industry)
            validated_data['content'] = eval(ai_content)
        except Exception as e:
            validated_data['content'] = {
                "hero": {"headline": "Welcome to My Website", "subheadline": "A great business in your industry"},
                "about": "This is a sample about section.",
                "services": ["Service 1", "Service 2", "Service 3"],
                "contact": {"email": "contact@example.com", "phone": "123-456-7890"}
            }
        
        website = Website.objects.create(owner=request.user, **validated_data)
        return website
    

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

User = get_user_model()

class WebsiteSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Website
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def generate_ai_content(self, business_type, industry, title):
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
            
            # Extract and clean the JSON content
            json_str = response.text.replace('```json', '').replace('```', '').strip()
            content_json = json.loads(json_str)
            
            return {
                "id": f"web_{os.urandom(4).hex()}",
                "type": "website_content",
                "content": content_json
            }
            
        except Exception as e:
            print(f"Error generating AI content: {e}")
            return {
                "hero": {
                    "headline": f"Welcome to {title}",
                    "subheadline": f"Your {business_type} solution in the {industry} industry"
                },
                "about": "This is a sample about section.",
                "services": [
                    {"name": "Service 1", "description": "Description of service 1"},
                    {"name": "Service 2", "description": "Description of service 2"},
                    {"name": "Service 3", "description": "Description of service 3"}
                ],
                "contact": {
                    "email": "contact@example.com",
                    "phone": "123-456-7890",
                    "address": "123 Business St, City"
                },
                "features": [
                    {"title": "Feature 1", "description": "Description of feature 1"},
                    {"title": "Feature 2", "description": "Description of feature 2"},
                    {"title": "Feature 3", "description": "Description of feature 3"}
                ]
            }
    
    def create(self, validated_data):
        request = self.context.get('request')
        website = Website.objects.create(
            owner=request.user,
            **validated_data,
            content=self.generate_ai_content(
                validated_data.get('business_type'),
                validated_data.get('industry'),
                validated_data.get('title')
            )
        )
        return website