from django.contrib import admin
from .models import Movie, Category, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rating', 'release_date', 'added_by', 'created_at']
    list_filter = ['category', 'release_date', 'rating', 'created_at']
    search_fields = ['title', 'description', 'actors']
    list_per_page = 20
    date_hierarchy = 'created_at'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_email']
    search_fields = ['user__username', 'user__email']

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'