from django.urls import path
from .views import LogoutView
from .views import (
    SignUpView, LoginView, RoleListCreateView, RoleDetailView,
    UserListView, UserDetailView, WebsiteListCreateView, WebsiteDetailView,
    HomeView, WebsiteCreateView, WebsiteEditView, WebsiteListView,
    WebsitePreviewView, AIGeneratorView, RoleManagementView, UserManagementView, WebsiteDeleteView
)

urlpatterns = [
    # API Endpoints
    path('api/auth/signup/', SignUpView.as_view(), name='signup'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/roles/', RoleListCreateView.as_view(), name='role-list'),
    path('api/roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/websites/', WebsiteListCreateView.as_view(), name='website-list'),
    path('api/websites/<int:pk>/', WebsiteDetailView.as_view(), name='website-detail'),
    
    # Template Views
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('websites/<int:pk>/delete/', WebsiteDeleteView.as_view(), name='website-delete'),
    path('websites/create/', WebsiteCreateView.as_view(), name='website-create'),
    path('websites/edit/<int:pk>/', WebsiteEditView.as_view(), name='website-edit'),
    path('websites/', WebsiteListView.as_view(), name='website-list-view'),
    path('preview/<int:pk>/', WebsitePreviewView.as_view(), name='website-preview'),
    path('ai-generator/', AIGeneratorView.as_view(), name='ai-generator'),
    path('admin/roles/', RoleManagementView.as_view(), name='role-management'),
    path('admin/users/', UserManagementView.as_view(), name='user-management'),
    path('logout/', LogoutView.as_view(), name='logout'),
]