from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Movie, Category, UserProfile
from .forms import CustomUserCreationForm, MovieForm, CategoryForm, UserProfileForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Rating, Review, Watchlist, UpcomingMovie
from .forms import RatingForm, ReviewForm, UpcomingMovieForm
from .forms import EditProfileForm
from django.core.exceptions import ValidationError
from django.db import transaction

def home(request):
    categories = Category.objects.all()
    recent_movies = Movie.objects.all()[:8]
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    movies = Movie.objects.all()

    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(actors__icontains=search_query)
        )

    if category_filter:
        movies = movies.filter(category_id=category_filter)

    paginator = Paginator(movies, 12)
    page = request.GET.get('page')
    movies = paginator.get_page(page)

    context = {
        'categories': categories,
        'movies': movies,
        'recent_movies': recent_movies,
        'search_query': search_query,
        'selected_category': category_filter,
    }
    return render(request, 'movies/home.html', context)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Safely create or get the user profile
            from .models import UserProfile
            UserProfile.objects.get_or_create(user=user)

            messages.success(request, f'Welcome {user.first_name or user.username}! Your account has been created successfully.')
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            messages.success(request, 'Movie added successfully!')
            return redirect('movie_detail', pk=movie.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})


@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if not movie.can_edit(request.user):
        messages.error(request, 'You can only edit movies you added.')
        return redirect('movie_detail', pk=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully!')
            return redirect('movie_detail', pk=pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movies/edit_movie.html', {'form': form, 'movie': movie})



@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if not movie.can_edit(request.user):
        messages.error(request, 'You can only delete movies you added.')
        return redirect('movie_detail', pk=pk)

    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully!')
        return redirect('home')
    return render(request, 'movies/delete_movie.html', {'movie': movie})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {
        'movie': movie,
        'can_edit': movie.can_edit(request.user) if request.user.is_authenticated else False
    }
    return render(request, 'movies/movie_detail.html', context)


def movies_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    movies = Movie.objects.filter(category=category)
    paginator = Paginator(movies, 12)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'movies/category_movies.html', {'category': category, 'movies': movies})


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'movies/edit_profile.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


# Admin Views
@staff_member_required
def admin_dashboard(request):
    total_movies = Movie.objects.count()
    total_users = User.objects.count()
    total_categories = Category.objects.count()
    recent_movies = Movie.objects.all()[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]

    context = {
        'total_movies': total_movies,
        'total_users': total_users,
        'total_categories': total_categories,
        'recent_movies': recent_movies,
        'recent_users': recent_users,
    }
    return render(request, 'movies/admin_dashboard.html', context)


@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'movies/manage_categories.html', {'categories': categories})


@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'movies/add_category.html', {'form': form})


@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manage_categories')
    return render(request, 'movies/delete_category.html', {'category': category})


@staff_member_required
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    return render(request, 'movies/manage_users.html', {'users': users})


@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('manage_users')

    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User {user.username} deleted successfully!')
        return redirect('manage_users')
    return render(request, 'movies/delete_user.html', {'user_to_delete': user})

@login_required
@require_POST
def rate_movie(request, pk):
    """AJAX view to handle movie ratings"""
    movie = get_object_or_404(Movie, pk=pk)
    
    try:
        data = json.loads(request.body)
        rating_value = int(data.get('rating', 0))
        
        if not (1 <= rating_value <= 5):
            return JsonResponse({'success': False, 'error': 'Rating must be between 1 and 5'})
        
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'rating': rating_value}
        )
        
        return JsonResponse({
            'success': True,
            'rating': rating.rating,
            'average_rating': movie.average_rating(),
            'total_ratings': movie.total_ratings(),
            'message': 'Rating updated!' if not created else 'Rating added!'
        })
    
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid data'})


@login_required
def add_review(request, pk):
    """Add/Edit review for a movie"""
    movie = get_object_or_404(Movie, pk=pk)
    
    try:
        review = Review.objects.get(user=request.user, movie=movie)
        form = ReviewForm(request.POST or None, instance=review)
        editing = True
    except Review.DoesNotExist:
        form = ReviewForm(request.POST or None)
        editing = False
    
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.movie = movie
        review.save()
        messages.success(request, 'Review updated!' if editing else 'Review added!')
        return redirect('movie_detail', pk=pk)
    
    context = {
        'form': form,
        'movie': movie,
        'editing': editing
    }
    return render(request, 'movies/add_review.html', context)


@login_required
def delete_review(request, pk):
    """Delete user's review"""
    review = get_object_or_404(Review, pk=pk, user=request.user)
    movie_pk = review.movie.pk
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('movie_detail', pk=movie_pk)
    
    return render(request, 'movies/delete_review.html', {'review': review})


@login_required
@require_POST
def toggle_watchlist(request, pk):
    """AJAX view to add/remove movie from watchlist"""
    movie = get_object_or_404(Movie, pk=pk)
    
    watchlist_item, created = Watchlist.objects.get_or_create(
        user=request.user,
        movie=movie
    )
    
    if not created:
        watchlist_item.delete()
        in_watchlist = False
        message = 'Removed from watchlist'
    else:
        in_watchlist = True
        message = 'Added to watchlist'
    
    return JsonResponse({
        'success': True,
        'in_watchlist': in_watchlist,
        'message': message
    })


@login_required
def watchlist_view(request):
    """View user's watchlist"""
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('movie')
    
    context = {
        'watchlist_items': watchlist_items,
        'watchlist_count': watchlist_items.count()
    }
    return render(request, 'movies/watchlist.html', context)


def upcoming_movies(request):
    """View upcoming movies"""
    upcoming = UpcomingMovie.objects.all()
    categories = Category.objects.all()
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        upcoming = upcoming.filter(category_id=category_filter)
    
    paginator = Paginator(upcoming, 12)
    page = request.GET.get('page')
    upcoming = paginator.get_page(page)
    
    context = {
        'upcoming_movies': upcoming,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, 'movies/upcoming_movies.html', context)


@login_required
def add_upcoming_movie(request):
    """Add upcoming movie (admin/staff only)"""
    if not request.user.is_staff:
        messages.error(request, 'Only staff members can add upcoming movies.')
        return redirect('upcoming_movies')
    
    if request.method == 'POST':
        form = UpcomingMovieForm(request.POST, request.FILES)
        if form.is_valid():
            upcoming_movie = form.save(commit=False)
            upcoming_movie.added_by = request.user
            upcoming_movie.save()
            messages.success(request, 'Upcoming movie added successfully!')
            return redirect('upcoming_movies')
    else:
        form = UpcomingMovieForm()
    
    return render(request, 'movies/add_upcoming_movie.html', {'form': form})


# Update your existing movie_detail view to include ratings and reviews
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie).select_related('user')
    user_review = None
    user_rating = 0
    in_watchlist = False
    
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(user=request.user, movie=movie)
        except Review.DoesNotExist:
            pass
        
        user_rating = movie.user_rating(request.user)
        in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie).exists()
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'user_review': user_review,
        'user_rating': user_rating,
        'in_watchlist': in_watchlist,
        'can_edit': movie.can_edit(request.user) if request.user.is_authenticated else False,
        'average_rating': movie.average_rating(),
        'total_ratings': movie.total_ratings(),
    }
    return render(request, 'movies/movie_detail.html', context)


@login_required
def edit_profile(request):
    """
    View to handle user profile editing
    """
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile, user=request.user)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Update User model fields
                    user = request.user
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.email = form.cleaned_data['email']
                    user.username = form.cleaned_data['username']
                    user.save()

                    # Update UserProfile
                    profile = form.save(commit=False)
                    profile.user = user
                    profile.save()

                    messages.success(request, 'Your profile has been updated successfully!')
                    return redirect('profile')  # Redirect to profile view page

            except ValidationError as e:
                messages.error(request, f'Validation error: {e}')
            except Exception as e:
                messages.error(request, f'An error occurred while updating your profile: {str(e)}')
        else:
            # Form has errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show the form
        form = EditProfileForm(instance=profile, user=request.user)

    context = {
        'form': form,
        'user': request.user,
        'profile': profile,
        'title': 'Edit Profile'
    }

    return render(request, 'movies/edit_profile.html', context)


@login_required
def profile(request):
    """
    View to display user profile
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    user_movies = Movie.objects.filter(added_by=request.user)

    # Calculate profile completion percentage
    completion_fields = [
        bool(request.user.first_name),
        bool(request.user.last_name),
        bool(request.user.email),
        bool(profile.profile_picture),
        bool(profile.age),
        bool(profile.gender),
        bool(profile.location),
        bool(profile.bio),
        bool(profile.favorite_genres),
    ]

    completed_fields = sum(completion_fields)
    total_fields = len(completion_fields)
    profile_completion_percentage = int((completed_fields / total_fields) * 100)

    # Get user stats (you might need to adjust these based on your models)
    try:
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
    except:
        watchlist_count = 0

    try:
        # Assuming you have a Rating model
        ratings_count = request.user.rating_set.count() if hasattr(request.user, 'rating_set') else 0
    except:
        ratings_count = 0

    context = {
        'user': request.user,
        'profile': profile,
        'title': 'My Profile',
        'profile_completion_percentage': profile_completion_percentage,
        'watchlist_count': watchlist_count,
        'ratings_count': ratings_count,
        'user_movies':user_movies,

    }

    return render(request, 'movies/profile.html', context)