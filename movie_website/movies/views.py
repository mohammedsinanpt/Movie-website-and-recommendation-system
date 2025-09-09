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
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
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
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_movies = Movie.objects.filter(added_by=request.user)
    return render(request, 'movies/profile.html', {'profile': profile, 'user_movies': user_movies})


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