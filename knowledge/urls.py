# knowledge/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    # 1. ルートURL (/) にアクセスした時、自動的に login へリダイレクト
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='index'),

    # 2. メイン機能のルーティング（knowledge/ が不要になります）
    path('home/', views.home, name='home'),
    path('articles/', views.knowledge_list, name='knowledge_list'),
    path('tags/<str:tag_name>/', views.tag_posts, name='tag_posts'),
    path('new/', views.knowledge_create, name='knowledge_create'),
    path('mypage/', views.mypage, name='mypage'),
    
    # 3. 個別データに対するルーティング
    path('<int:pk>/', views.knowledge_detail, name='knowledge_detail'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    
    # 4. 認証系のルーティング
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]