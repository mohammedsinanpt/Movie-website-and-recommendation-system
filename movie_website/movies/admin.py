from django.contrib import admin
from .models import Category, Movie, UserProfile, Rating, Review, Watchlist, UpcomingMovie

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rating', 'added_by', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'actors']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'created_at']
    search_fields = ['review_text']

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'added_at']

@admin.register(UpcomingMovie)
class UpcomingMovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'expected_release_date', 'category', 'added_by']
    list_filter = ['category', 'expected_release_date']