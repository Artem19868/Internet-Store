# Internet Store

Django-based e-commerce platform with product catalog, shopping cart, and user authentication.

## Features

- Product catalog with categories
- Shopping cart functionality  
- User registration and authentication
- Product search
- Price filtering
- Responsive design

## Technologies Used

- **Backend:** Django, Django ORM
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** PostgreSQL

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Artem19868/Internet-Store.git
   cd internet-store

2. **Create virtual environment**
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # or
    venv\Scripts\activate     # Windows

3. **Install dependencies**
    pip install -r requirements.txt

4. **Set up environment variables**
    cp .env.example .env
    # Edit .env with your settings

5. **Apply migrations**
    python manage.py migrate

6. **Create superuser (optional)**
    python manage.py createsuperuser

7. **Run development server**
    python manage.py runserver
    # Visit http://localhost:8000 in your browser.