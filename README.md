# 🛍️ Django Online Shop

This is a fully functional **Django-based online shop web application**, allowing users to browse products, manage a shopping basket, mark favorites, post reviews, and maintain personal profiles.

---

## 🚀 Features

- User Registration & Authentication
- Product Listings with Categories
- Product Detail Pages
- Search by Product Name
- Add to Basket (Cart) Functionality
- Favorites (Wishlist) Management
- Product Reviews by Users
- User Profile Page (with Activity Stats & Own Products)
- Admin Interface for Product & Order Management
- Contact Us Page (via Email)
- Fully Responsive Design (Bootstrap 5)

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Bootstrap 5)
- **Database:** SQLite (for development)
- **Email:** SMTP via Django Email Backend
- **Environment Variables:** Python `dotenv`

---

## 🏗️ Project Structure (Important Folders)

shop_blog/
│
├── website/ # Project settings folder
├── blog_app/ # Main application (models, views, templates)
│ ├── templates/
│ │ ├── components/ # Reusable template parts (cards, pagination)
│ │ ├── index.html
│ │ ├── favourites.html
│ │ ├── login.html
│ │ ├── search.html
│ │ ├── register.html
│ │ ├── about.html
│ │ ├── product_list.html
│ │ ├── profile.html
│ │ ├── basket.html
│ │ └── contact.html
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ └── urls.py
│
├── media/ # Product images and user uploads
├── templates/ # Base Html file for frontend 
├── static/ # CSS, JS, static assets
├── .env # Environment config (hidden)
├── db.sqlite3 # SQLite database file
└── manage.py # Django management script

## 🚀 Installation & Setup Instructions

### 1. Clone the repository
bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables
Create .env file in the project root:
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=yourpassword
DEFAULT_FROM_EMAIL=you@example.com
CONTACT_RECEIVER_EMAIL=receiver@example.com
5. Apply migrations
python manage.py migrate
6. Create superuser (for Admin panel)
python manage.py createsuperuser
7. Run development server
python manage.py runserver
8. Stop the server
Press CTRL + C in the terminal to stop the server.
