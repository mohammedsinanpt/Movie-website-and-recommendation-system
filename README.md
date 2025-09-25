# 🎬 Movie Hub - Django Movie Discovery Platform

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
</div>

<div align="center">
  <h3>A comprehensive movie discovery and recommendation platform built with Django</h3>
  <p><em>Share, discover, and discuss movies with fellow enthusiasts</em></p>
</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🌟 Overview

Movie Hub is a full-featured Django web application that allows users to discover, rate, and review movies. The platform includes a comprehensive rating system, personal watchlists, upcoming movie tracking, and administrative features for content management.

### Key Highlights
- **Interactive Rating System**: 5-star rating with real-time updates
- **Personal Watchlists**: Save and organize movies to watch later
- **Community Reviews**: Share detailed movie reviews and opinions
- **Upcoming Movies**: Track and manage upcoming releases
- **Admin Dashboard**: Comprehensive content and user management
- **Responsive Design**: Optimized for all devices

## ✨ Features

### 🎭 **Core Functionality**
- **Movie Database Management**: Complete CRUD operations for movies
- **Advanced Search**: Multi-field search across titles, descriptions, and cast
- **Category System**: Genre-based organization with filtering
- **Image Upload**: Movie poster and profile picture handling
- **Pagination**: Efficient browsing of large datasets

### ⭐ **Rating & Review System**
- **5-Star Rating Interface**: Interactive star-based rating system
- **Real-time Updates**: AJAX-powered rating updates without page refresh
- **Average Rating Calculation**: Dynamic community rating aggregation
- **Review Management**: Full CRUD operations for user reviews
- **Review Moderation**: Edit and delete functionality for personal reviews

### ❤️ **Watchlist & Favorites**
- **Personal Watchlist**: Save movies for future viewing
- **Quick Actions**: One-click add/remove from movie cards
- **Watchlist Dashboard**: Dedicated page for managing saved movies
- **Visual Indicators**: Clear watchlist status indicators

### 👤 **User Management**
- **Authentication System**: Registration, login, logout functionality
- **User Profiles**: Customizable profiles with bio and preferences
- **Profile Pictures**: Upload and manage profile images
- **Favorite Genres**: Select and display preferred movie categories
- **Activity Tracking**: View contributed movies and reviews

### 🎪 **Upcoming Movies**
- **Release Tracking**: Manage upcoming movie releases
- **Date Management**: Expected release date tracking
- **Staff Controls**: Admin-only upcoming movie management
- **Category Integration**: Filter upcoming movies by genre

### 🛡️ **Administrative Features**
- **Admin Dashboard**: Comprehensive statistics and overview
- **User Management**: Full user account administration
- **Category Management**: Create, edit, and delete movie categories
- **Content Oversight**: Monitor and manage user-generated content
- **Staff Permissions**: Role-based access control

### 🎨 **UI/UX Features**
- **Responsive Design**: Mobile-first Bootstrap 5 implementation
- **Modern Interface**: Clean, intuitive user experience
- **Interactive Elements**: Smooth animations and transitions
- **Accessibility**: WCAG compliant design patterns
- **Cross-browser Compatibility**: Tested across major browsers

## 🛠 Tech Stack

### Backend
- **Django 5.x**: Web framework
- **Python 3.8+**: Programming language
- **SQLite**: Default database (PostgreSQL/MySQL compatible)
- **Pillow**: Image processing library

### Frontend
- **HTML5 & CSS3**: Markup and styling
- **Bootstrap 5**: CSS framework
- **JavaScript (ES6)**: Client-side functionality
- **AJAX**: Asynchronous web requests
- **Font Awesome 6**: Icon library

### Development Tools
- **Git**: Version control
- **Django Admin**: Administrative interface
- **Django Forms**: Form handling and validation
- **Django ORM**: Database abstraction layer

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/movie-hub-django.git
   cd movie-hub-django
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv movie_env
   
   # Windows
   movie_env\Scripts\activate
   
   # macOS/Linux
   source movie_env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Main Application: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 📱 Usage

### For Regular Users
1. **Registration**: Create an account to access all features
2. **Browse Movies**: Explore movies by category or search
3. **Rate & Review**: Share your opinions with 5-star ratings and detailed reviews
4. **Manage Watchlist**: Save movies to watch later
5. **Profile Management**: Customize your profile and preferences

### For Administrators
1. **Admin Dashboard**: Access comprehensive site statistics
2. **User Management**: Monitor and manage user accounts
3. **Content Moderation**: Oversee movies, reviews, and categories
4. **Upcoming Movies**: Add and manage upcoming releases

## 📁 Project Structure

```
movie_hub/
├── movie_website/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── movies/
│   ├── migrations/
│   ├── templates/
│   │   └── movies/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── movie_detail.html
│   │       ├── watchlist.html
│   │       ├── add_review.html
│   │       ├── upcoming_movies.html
│   │       └── ...
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/
├── media/
├── requirements.txt
├── manage.py
└── README.md
```

## 🔗 API Endpoints

### Public Endpoints
- `GET /` - Home page with movie listings
- `GET /movie/<id>/` - Movie detail page
- `GET /category/<id>/` - Movies by category
- `GET /upcoming/` - Upcoming movies

### User Endpoints (Login Required)
- `POST /movie/<id>/rate/` - Rate a movie (AJAX)
- `POST /movie/<id>/watchlist/` - Toggle watchlist (AJAX)
- `GET|POST /movie/<id>/review/` - Add/edit review
- `GET /watchlist/` - User's watchlist
- `GET /profile/` - User profile

### Admin Endpoints (Staff Only)
- `GET /admin-dashboard/` - Admin dashboard
- `GET /admin/categories/` - Manage categories
- `GET /admin/users/` - Manage users
- `POST /upcoming/add/` - Add upcoming movie

## 📸 Screenshots


### Home Page


- Movie grid with ratings and categories
- Search and filter functionality

### Movie Detail Page
- Interactive rating system
- Reviews section
- Watchlist toggle

### User Dashboard
- Personal movie contributions
- Profile management
- Watchlist overview

### Admin Panel
- Site statistics
- User and content management

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Project**
2. **Create Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to Branch** (`git push origin feature/AmazingFeature`)
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📞 Contact

**mohammed sinan P T** - [cnansinz@gmail.com](mailto:cnansinz@gmail.com)

**Project Link**: [https://github.com/mohammedsinanpt/Movie-website-and-recommendation-system](https://github.com/mohammedsinanpt/Movie-website-and-recommendation-system)



---

<div align="center">
  <p>⭐ Star this repository if you found it helpful!</p>
  <p>🍴 Fork it to create your own version!</p>
  <p>🐛 Found a bug? Create an issue!</p>
</div>

---

### 🎯 Future Enhancements

- [ ] User recommendation algorithm
- [ ] Social features (follow users, movie discussions)
- [ ] Advanced filtering (by year, rating, etc.)
- [ ] Movie trailer integration
- [ ] Email notifications for upcoming movies
- [ ] API for mobile app integration
- [ ] Internationalization (i18n) support

---

<div align="center">
  <p><em>Built with ❤️ using Django</em></p>
</div>
