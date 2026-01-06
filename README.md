# Online Bookstore - Django Project

A complete Django-based online bookstore management system with MySQL database.

## 🚀 Features

- 📚 Browse books by category
- 🔍 View detailed book information
- 🛒 Shopping cart functionality
- 📦 Order placement and management
- 👨‍💼 Admin panel for inventory management
- 💳 Customer checkout with order confirmation
- 📱 Responsive design

## 🛠️ Tech Stack

- **Backend:** Python 3.x, Django 6.0
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, Django Templates
- **ORM:** Django ORM

## 📋 Prerequisites

Before running this project, ensure you have:

- Python 3.x installed
- MySQL Server installed and running
- pip (Python package manager)

## 🔧 Installation & Setup

### Option 1: Automated Setup (Recommended)

1. **Navigate to project directory:**
```bash
cd /home/n/Desktop/new_project/bookstore_project
```

2. **Update MySQL password in settings.py:**
   - Open `bookstore_project/settings.py`
   - Find the `DATABASES` section
   - Update the `PASSWORD` field with your MySQL root password

3. **Run the setup script:**
```bash
./setup.sh
```

The script will:
- Verify MySQL installation
- Create the database
- Run migrations
- Prompt you to create a superuser
- Start the development server

### Option 2: Manual Setup

1. **Create virtual environment (if not exists):**
```bash
cd /home/n/Desktop/new_project
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install django mysqlclient
```

3. **Create MySQL database:**
```bash
mysql -u root -p
```
```sql
CREATE DATABASE bookstore_db;
exit;
```

4. **Update database password:**
   - Edit `bookstore_project/settings.py`
   - Update MySQL password in `DATABASES` configuration

5. **Run migrations:**
```bash
cd bookstore_project
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
```

7. **Start development server:**
```bash
python manage.py runserver
```

## 🌐 Access the Application

- **Main Website:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
bookstore_project/
├── manage.py
├── setup.sh                    # Automated setup script
├── bookstore_project/          # Main project settings
│   ├── settings.py            # Database & app configuration
│   ├── urls.py                # Main URL routing
│   └── wsgi.py
├── books/                      # Books app
│   ├── models.py              # Book & Category models
│   ├── views.py               # Book listing & details
│   ├── urls.py
│   └── admin.py
├── cart/                       # Shopping cart app
│   ├── models.py              # CartItem model
│   ├── views.py               # Cart operations
│   ├── urls.py
│   └── admin.py
├── orders/                     # Orders app
│   ├── models.py              # Order & OrderItem models
│   ├── views.py               # Checkout & confirmation
│   ├── forms.py               # Order form
│   ├── urls.py
│   └── admin.py
├── templates/                  # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── book_detail.html
│   ├── cart.html
│   ├── place_order.html
│   └── order_confirmation.html
└── static/                     # Static files
    └── css/
        └── style.css
```

## 💾 Database Models

### Books App
- **Category:** Book categories (Fiction, Non-Fiction, etc.)
- **Book:** Book details (title, author, price, stock, etc.)

### Cart App
- **CartItem:** Shopping cart items with quantity

### Orders App
- **Order:** Customer orders with delivery info
- **OrderItem:** Individual items in an order

## 🎯 Usage Guide

### For Administrators

1. **Login to Admin Panel:**
   - Go to http://127.0.0.1:8000/admin/
   - Use superuser credentials

2. **Add Categories:**
   - Click "Categories" → "Add Category"
   - Enter category name (e.g., Fiction, Science, History)

3. **Add Books:**
   - Click "Books" → "Add Book"
   - Fill in book details (title, author, category, price, stock, description)
   - Save

4. **Manage Orders:**
   - View all orders in "Orders" section
   - Update order status (Pending → Confirmed → Delivered)

### For Customers

1. **Browse Books:**
   - Visit home page
   - Filter by category
   - View book details

2. **Add to Cart:**
   - Click "Add to Cart" on any book
   - View cart to see items

3. **Checkout:**
   - Click "Proceed to Checkout"
   - Fill in delivery information
   - Place order

4. **Order Confirmation:**
   - View order details
   - Note order ID for reference

## 🎨 Features Showcase

- **Modern UI:** Gradient backgrounds, card-based layouts
- **Responsive Design:** Works on desktop and mobile
- **Real-time Cart:** Session-based cart for guest users
- **Admin Dashboard:** Full CRUD operations for books and orders
- **Order Tracking:** View order status and history

## 🔒 Security Features

- CSRF protection on all forms
- SQL injection prevention via Django ORM
- Password hashing for admin users
- Session-based authentication

## 📝 Sample Data

After setup, add some sample books via admin panel:

**Example Books:**
- Title: "The Great Gatsby", Author: "F. Scott Fitzgerald", Category: "Fiction", Price: 299
- Title: "Sapiens", Author: "Yuval Noah Harari", Category: "Non-Fiction", Price: 499
- Title: "Python Crash Course", Author: "Eric Matthes", Category: "Programming", Price: 599

## 🐛 Troubleshooting

### MySQL Connection Error
- Verify MySQL is running: `sudo systemctl status mysql`
- Check password in `settings.py`
- Ensure database exists: `SHOW DATABASES;`

### Migration Errors
- Delete migration files (except `__init__.py`)
- Run: `python manage.py makemigrations` then `python manage.py migrate`

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check `STATIC_URL` in settings.py

### Port Already in Use
- Kill existing process: `sudo lsof -t -i tcp:8000 | xargs kill -9`
- Or use different port: `python manage.py runserver 8080`

## 📚 Resume Points

- Developed a full-stack Online Bookstore using Django MVT architecture with Python and MySQL
- Implemented CRUD operations for books, cart, and order management using Django ORM
- Created responsive UI using HTML5, CSS3, and Django Template Language
- Integrated Django Admin panel for efficient backend management
- Built shopping cart functionality with session-based storage
- Designed relational database schema with proper foreign key relationships

## 📄 License

This is a college project for educational purposes.

## 👨‍💻 Author

Created as a Django learning project demonstrating full-stack web development.

---



to run the code 

✅ Your Bookstore is LIVE!
🌐 Access the Application:
Open your web browser and visit:

Main Website: http://127.0.0.1:8000/
Browse books, add to cart, place orders
Admin Panel: http://127.0.0.1:8000/admin/


Username: admin
Password: admin123


📝 Next Steps:
Add Sample Books (via Admin Panel):
Login to http://127.0.0.1:8000/admin/


Click "Categories" → Add categories (Fiction, Science, etc.)
Click "Books" → Add sample books with prices and stock
Test the Application:
Browse books on home page
Add books to cart
Proceed to checkout
Place an order
🛑 To Stop the Server:
Press Ctrl + C in the terminal

🔄 To Run Again Later:


bash
cd /home/n/Desktop/new_project/bookstore_project
source ../venv/bin/activate
python manage.py runserver
