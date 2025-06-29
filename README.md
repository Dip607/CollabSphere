# 🎓 CollabSphere - XYZ College Community Platform

A modern, feature-rich community platform designed specifically for college students, alumni, and professors. Built with Django and featuring a beautiful dark-themed UI with real-time messaging and notification systems.

![CollabSphere](https://img.shields.io/badge/Django-5.2.3-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)

## 🖼️ Screenshots

<h3 align="center">🔍 Screenshots</h3>

<p align="center">
  <img src="https://github.com/SouravUpadhyay7/Collab_Sphere/blob/main/Screenshot/Screenshot%202025-06-29%20154713.png?raw=true" 
       alt="Homepage" 
       width="45%" 
       style="border-radius: 12px; margin: 10px;" />

  <img src="https://github.com/SouravUpadhyay7/Collab_Sphere/blob/main/Screenshot/Screenshot%202025-06-29%20155103.png?raw=true" 
       alt="Dashboard" 
       width="45%" 
       style="border-radius: 12px; margin: 10px;" />
</p>

<p align="center">
  <img src="https://github.com/SouravUpadhyay7/Collab_Sphere/blob/main/Screenshot/Screenshot%202025-06-29%20155132.png?raw=true" 
       alt="Community Posts" 
       width="45%" 
       style="border-radius: 12px; margin: 10px;" />

  <img src="https://github.com/SouravUpadhyay7/Collab_Sphere/blob/main/Screenshot/Screenshot%202025-06-29%20155157.png?raw=true" 
       alt="Post Detail" 
       width="45%" 
       style="border-radius: 12px; margin: 10px;" />
</p>


## 🛠️ Tech Stack

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Font_Awesome-339AF0?style=for-the-badge&logo=fontawesome&logoColor=white" alt="Font Awesome">
</div>

## 🌟 Features

### 🔐 Authentication & User Management
- **Custom User Model** with email-based login
- **Role-based System**: Students, Alumni, Professors
- **Profile Management** with profile pictures and batch information
- **Password Reset** functionality with email integration

### 📝 Community Posts
- **Multiple Post Types**: Jobs, Projects, Internships, General
- **Rich Text Content** with modern formatting
- **Comment System** with real-time updates
- **User Role Badges** and profile information display

### 💬 Direct Messaging
- **Private Conversations** between users
- **Real-time Message Updates** with auto-refresh
- **Read Receipts** and delivery status
- **Message Inbox** with unread message counts
- **Easy Access** via "Send Message" buttons on posts

### 🔔 Smart Notifications
- **Real-time Notification Bell** in navigation
- **Automatic Notifications** for:
  - New comments on your posts
  - Direct messages received
  - Replies to your comments
- **Mark as Read** functionality (individual or bulk)
- **Notification Center** with full history

### 🎨 Modern UI/UX
- **Dark Theme** with glassmorphism effects
- **Responsive Design** for all devices
- **Animated Elements** with smooth transitions
- **Gradient Backgrounds** and modern typography
- **Bootstrap 5** with custom styling

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (recommended) or SQLite
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/collabsphere.git
   cd collabsphere
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   ```bash
   # For PostgreSQL (recommended)
   # Update settings.py with your database credentials
   
   # For SQLite (default)
   # No additional configuration needed
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

```
CollabSphere/
├── accounts/                 # User authentication & profiles
│   ├── models.py            # Custom user model
│   ├── views.py             # Authentication views
│   ├── forms.py             # User forms
│   └── templates/           # User templates
├── community/               # Posts & messaging
│   ├── models.py            # Post, Comment, DirectMessage models
│   ├── views.py             # Community views
│   ├── forms.py             # Post & message forms
│   └── templates/           # Community templates
├── collabsphere/            # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── templates/               # Base templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
└── manage.py               # Django management script
```

## 🎯 Usage Guide

### For Students
1. **Sign up** with your college email
2. **Complete your profile** with batch information
3. **Browse posts** for jobs, internships, and projects
4. **Comment** on posts to engage with the community
5. **Send direct messages** to connect with other users
6. **Stay updated** with notifications for new activity

### For Alumni
1. **Create posts** to share job opportunities
2. **Mentor students** through comments and messages
3. **Network** with other alumni and current students
4. **Share experiences** and career advice

### For Professors
1. **Post project opportunities** for students
2. **Share academic resources** and announcements
3. **Connect** with students and alumni
4. **Build research collaborations**

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/collabsphere
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Email Configuration
For password reset functionality, configure your email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🛠️ Customization

### Adding New Post Types
1. Update `POST_TYPE_CHOICES` in `community/models.py`
2. Add corresponding templates if needed
3. Update forms and views as necessary

### Customizing the Theme
1. Modify CSS variables in `templates/base.html`
2. Update color schemes and gradients
3. Customize animations and transitions

### Adding New Features
1. Create new Django apps for major features
2. Follow the existing code structure
3. Update URL configurations
4. Add appropriate templates

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Ensure PostgreSQL is running
- Check database credentials in settings.py
- Verify database exists

**Static Files Not Loading**
- Run `python manage.py collectstatic`
- Check STATIC_URL and STATIC_ROOT settings

**Email Not Working**
- Verify SMTP settings
- Check firewall settings
- Use Gmail App Passwords for 2FA accounts

**Migration Errors**
- Delete migration files and recreate them
- Ensure database is in sync with models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django** - The web framework for perfectionists with deadlines
- **Bootstrap** - The most popular CSS framework
- **Font Awesome** - The iconic font and CSS toolkit
- **XYZ College** - For inspiring this community platform

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: support@collabsphere.com
- Documentation: [docs.collabsphere.com](https://docs.collabsphere.com)

---

**Made with ❤️ for the XYZ College Community**

*Building connections, fostering collaboration, and empowering the next generation of innovators.* 
