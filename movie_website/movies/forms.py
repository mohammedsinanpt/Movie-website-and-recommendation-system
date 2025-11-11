from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movie, Category, UserProfile, Rating, Review, UpcomingMovie


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'rating', 'category', 'youtube_trailer']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actors': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '0.1'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'youtube_trailer': forms.URLInput(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'favorite_genres']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'favorite_genres': forms.CheckboxSelectMultiple(),
        }


class RatingForm(forms.ModelForm):
    """Form for rating movies (1-5 stars)"""
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = "Rate this movie"


class ReviewForm(forms.ModelForm):
    """Form for writing movie reviews"""
    class Meta:
        model = Review
        fields = ['review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_text'].label = "Your Review"


class UpcomingMovieForm(forms.ModelForm):
    """Form for adding upcoming movies"""
    class Meta:
        model = UpcomingMovie
        fields = ['title', 'poster', 'description', 'expected_release_date', 'actors', 'category', 'youtube_trailer']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'expected_release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actors': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'youtube_trailer': forms.URLInput(attrs={'class': 'form-control'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
        }


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'age', 'gender', 'location', 'bio', 'favorite_genres']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '13',
                'max': '120',
                'placeholder': 'Your age'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Select Gender'),
                ('M', 'Male'),
                ('F', 'Female'),
                ('O', 'Other'),
            ]),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': '500',
                'placeholder': 'Tell us about yourself and your movie preferences...'
            }),
            'favorite_genres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Action, Comedy, Drama, etc.'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.user.id if hasattr(self.instance, 'user') else None

        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.user.id if hasattr(self.instance, 'user') else None

        if User.objects.filter(username=username).exclude(id=user_id).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 13 or age > 120):
            raise forms.ValidationError("Age must be between 13 and 120.")
        return age