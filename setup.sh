#!/bin/bash

# Online Bookstore - Setup and Run Script

echo "========================================="
echo "Online Bookstore - Django Project Setup"
echo "========================================="
echo ""

# Step 1: Check MySQL
echo "Step 1: Checking MySQL..."
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL is not installed. Please install MySQL first."
    echo "Run: sudo apt install mysql-server"
    exit 1
fi
echo "✅ MySQL is installed"
echo ""

# Step 2: Create Database
echo "Step 2: Creating MySQL database..."
echo "Please enter your MySQL root password when prompted:"
mysql -u root -p << EOF
CREATE DATABASE IF NOT EXISTS bookstore_db;
SHOW DATABASES LIKE 'bookstore_db';
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database created/verified"
else
    echo "❌ Failed to create database"
    exit 1
fi
echo ""

# Step 3: Activate virtual environment
echo "Step 3: Activating virtual environment..."
source ../venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Step 4: Run migrations
echo "Step 4: Running database migrations..."
python manage.py makemigrations
python manage.py migrate

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed"
    exit 1
fi
echo ""

# Step 5: Create superuser
echo "Step 5: Creating superuser..."
echo "Please create an admin account:"
python manage.py createsuperuser
echo ""

# Step 6: Run server
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "Starting development server..."
echo "Access the application at: http://127.0.0.1:8000/"
echo "Access admin panel at: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python manage.py runserver
