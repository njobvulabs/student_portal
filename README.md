# NJOBVU COLLEGE Student Portal

A comprehensive student portal system built with modern technologies to manage academic activities, course enrollments, grades, and communications between students, instructors, and administrators.

## Technologies Used

- **Backend Framework:** Django 4.2+
- **Frontend Technologies:**
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Bootstrap 5.3
  - Font Awesome 6.0
- **Database:** SQLite (default) / PostgreSQL (optional)
- **Authentication:** Django Authentication System
- **Additional Libraries:**
  - django-crispy-forms
  - django-allauth
  - Pillow (Python Imaging Library)

## Features

- Role-based Authentication (Student, Instructor, Administrator)
- Course Management System
- Grade Tracking
- Announcement System
- User Profile Management
- Responsive Design
- Dark/Light Theme Toggle
- Real-time Notifications
- Mobile-friendly Interface

## Prerequisites

### Common Requirements (All Operating Systems)
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Windows-specific Requirements
- Windows 10 or higher
- Microsoft Visual C++ 14.0 or higher

### Linux-specific Requirements
- Python development headers
- Database development libraries

### macOS-specific Requirements
- Command Line Tools for Xcode
- Homebrew (recommended)

## Installation Instructions

### Windows Installation

1. **Install Python:**
   ```bash
   # Download Python from official website
   https://www.python.org/downloads/windows/
   # During installation, check "Add Python to PATH"
   ```

2. **Install Git:**
   ```bash
   # Download from
   https://git-scm.com/download/windows
   ```

3. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/student_portal.git
   cd student_portal
   ```

4. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Linux Installation

1. **Install Python and Required Packages:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-dev python3-venv git

   # Fedora
   sudo dnf install python3 python3-pip python3-devel python3-virtualenv git

   # Arch Linux
   sudo pacman -Syu
   sudo pacman -S python python-pip python-virtualenv git base-devel
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/student_portal.git
   cd student_portal
   ```

3. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For Ubuntu/Debian/Fedora
   source venv/bin/activate   # For Arch Linux
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### macOS Installation

1. **Install Command Line Tools:**
   ```bash
   xcode-select --install
   ```

2. **Install Homebrew:**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Install Python:**
   ```bash
   brew install python
   ```

4. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/student_portal.git
   cd student_portal
   ```

5. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

6. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Project Setup

1. **Apply Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create Superuser (Admin):**
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect Static Files:**
   ```bash
   python manage.py collectstatic
   ```

## Running the Project

1. **Start Development Server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the Portal:**
   - Open web browser and navigate to: `http://127.0.0.1:8000`
   - Admin interface: `http://127.0.0.1:8000/admin`

## Default User Roles

- **Student:** Can view courses, enroll, view grades, and receive announcements
- **Instructor:** Can manage courses, post grades, and create announcements
- **Administrator:** Full system access and user management

## Environment Variables (Optional)

Create a `.env` file in the project root:
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

## Production Deployment Considerations

1. Set `DEBUG=False` in production
2. Use a production-grade database (e.g., PostgreSQL)
3. Configure proper email settings
4. Set up static files serving
5. Use HTTPS
6. Configure proper security settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please email nj0075@mca.ac.mw or create an issue in the repository.
