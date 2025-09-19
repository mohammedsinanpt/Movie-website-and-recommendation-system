from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=500)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Rating out of 10"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='movies')
    youtube_trailer = models.URLField(max_length=200, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def can_edit(self, user):
        return self.added_by == user or user.is_staff
    
    def average_rating(self):
        """Calculate average user rating from 1-5 scale"""
        avg = self.user_ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0
    
    def total_ratings(self):
        """Get total number of user ratings"""
        return self.user_ratings.count()
    
    def user_rating(self, user):
        """Get specific user's rating for this movie"""
        if user.is_authenticated:
            try:
                return self.user_ratings.get(user=user).rating
            except Rating.DoesNotExist:
                return 0
        return 0


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    favorite_genres = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Rating(models.Model):
    """User ratings for movies (1-5 stars)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title}: {self.rating}/5"


class Review(models.Model):
    """User reviews for movies"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title}"


class Watchlist(models.Model):
    """User's watchlist/favorites"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='in_watchlists')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class UpcomingMovie(models.Model):
    """Upcoming movies"""
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='upcoming_posters/', blank=True, null=True)
    description = models.TextField()
    expected_release_date = models.DateField()
    actors = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='upcoming_movies')
    youtube_trailer = models.URLField(max_length=200, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['expected_release_date']

    def __str__(self):
        return f"{self.title} (Coming {self.expected_release_date})"