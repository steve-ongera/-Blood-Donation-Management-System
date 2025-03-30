# Blood Donation Management System

A comprehensive Django application designed to manage blood donation operations, connecting donors with recipients through an efficient inventory management system.

## Overview

This application provides a platform for blood banks, hospitals, and healthcare facilities to:

- Register and manage blood donors
- Track recipient information and blood requests
- Maintain blood inventory records
- Process and approve blood donation requests
- Allow medical professionals to oversee the donation process

## Features

- **User Management**: Different user types (donors, recipients, doctors, administrators)
- **Donor Management**: Track donor information, donation history, and eligibility
- **Recipient System**: Manage patient information and blood requests
- **Inventory Tracking**: Real-time monitoring of available blood units by blood type
- **Request Processing**: Workflow for blood request approval and fulfillment
- **Doctor Verification**: System for medical professional verification and oversight

## Prerequisites

- Python 3.8+
- Django 3.2+
- Pillow library (for image processing)
- Database (SQLite for development, PostgreSQL recommended for production)
- Virtual environment tool (venv, pipenv, or conda)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/blood-donation-system.git
   cd blood-donation-system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3  # For development
   ```

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

## Project Structure

The application is organized around the following models:

- **Donor**: Stores information about blood donors including personal details, blood type, and donation history
- **Recipient**: Manages information about patients requiring blood, including medical details
- **BloodInventory**: Tracks available blood units by blood type
- **Donation**: Records individual donation events and automatically updates inventory
- **BloodRequest**: Manages the blood request workflow from submission to fulfillment
- **Doctor**: Stores information about medical professionals who oversee the donation process

## Configuration

### Media Files

The application stores various uploaded files:
- Donor health reports: `/media/donor_reports/`
- Donor profile pictures: `/media/doner/profile_pictures/`
- Recipient profile pictures: `/media/recipient/profile_pictures/`
- Doctor profile pictures: `/media/doctors/profile_pictures/`

Configure your `settings.py` to handle these media files:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Static Files

Default images and other static assets should be placed in a static folder:
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

## Usage

After installation, you can:

1. Access the admin interface at `http://localhost:8000/admin/`
2. Use the admin panel to add initial blood inventory records
3. Register donors and recipients through the application
4. Process blood requests and track inventory

## API Endpoints (if applicable)

Document your API endpoints here if you plan to create a REST API for the application.

## Development

### Adding New Features

To extend the application, you can:
- Add new models to `models.py`
- Create new views in `views.py`
- Define URL patterns in `urls.py`
- Design templates in the `templates` directory

### Running Tests

```
python manage.py test
```

## Deployment

Instructions for deploying to production:

1. Set `DEBUG=False` in your production settings
2. Configure a production database (PostgreSQL recommended)
3. Set up static files serving with a web server
4. Configure media files storage
5. Use a WSGI server like Gunicorn
6. Set up a reverse proxy with Nginx or Apache

## License

[Specify your license here]

## Contributing

[Guidelines for contributing to your project]

## Contact

- Gadafi Imran ( Project Lead )
- Dedra Cheche