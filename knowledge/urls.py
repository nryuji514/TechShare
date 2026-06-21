# knowledge/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('',views.home, name='home'),
    path('arigicles/', views.knowledge_list, name='knowledge_list'),
    path('tag/<str:tag_name>/', views.tag_posts,name='tag_posts'),
    path('new/',views.knowledge_create, name='knowledge_create'),
    path('edit/<int:pk>/', views.knowledge_edit, name='knowledge_edit'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/edit/', views.profile_edit, name='profile_edit'),
    path('mypage/avatar/', views.avatar_upload, name='avatar_upload'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('<int:pk>/', views.knowledge_detail, name='knowledge_detail'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    
    # 4. 認証系のルーティング
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]