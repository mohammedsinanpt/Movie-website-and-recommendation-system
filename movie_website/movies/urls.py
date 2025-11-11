from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('category/<int:category_id>/', views.movies_by_category, name='movies_by_category'),
    
    # Upcoming movies
    path('upcoming/', views.upcoming_movies, name='upcoming_movies'),
    path('upcoming/add/', views.add_upcoming_movie, name='add_upcoming_movie'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User movie management
    path('add-movie/', views.add_movie, name='add_movie'),
    path('movie/<int:pk>/edit/', views.edit_movie, name='edit_movie'),
    path('movie/<int:pk>/delete/', views.delete_movie, name='delete_movie'),
    
    # Rating and Review system
    path('movie/<int:pk>/rate/', views.rate_movie, name='rate_movie'),
    path('movie/<int:pk>/review/', views.add_review, name='add_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    
    # Watchlist
    path('movie/<int:pk>/watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path('watchlist/', views.watchlist_view, name='watchlist'),

    # User profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Admin views
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/categories/', views.manage_categories, name='manage_categories'),
    path('admin/categories/add/', views.add_category, name='add_category'),
    path('admin/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]