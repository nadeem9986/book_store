# 🚀 Quick Start Guide - Online Bookstore

## Prerequisites Checklist
- [ ] Python 3.x installed
- [ ] MySQL Server installed and running
- [ ] MySQL root password known

## Step-by-Step Setup

### 1. Update MySQL Password
```bash
cd /home/n/Desktop/new_project/bookstore_project
nano bookstore_project/settings.py
```
Find line 80 and update:
```python
'PASSWORD': 'your_mysql_password_here',
```

### 2. Create Database
```bash
mysql -u root -p
```
```sql
CREATE DATABASE bookstore_db;
SHOW DATABASES;
exit;
```

### 3. Run Migrations
```bash
source ../venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```
Enter:
- Username: admin
- Email: admin@bookstore.com
- Password: (your choice)

### 5. Start Server
```bash
python manage.py runserver
```

### 6. Access Application
- **Main Site:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## First Time Setup - Add Sample Data

1. Login to admin panel
2. Add Categories:
   - Fiction
   - Non-Fiction
   - Science
   - Programming
   - History

3. Add Sample Books:
   ```
   Title: "The Great Gatsby"
   Author: "F. Scott Fitzgerald"
   Category: Fiction
   Price: 299
   Stock: 10
   Description: "A classic American novel..."
   ```

## Common Commands

```bash
# Activate virtual environment
source ../venv/bin/activate

# Run server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell
```

## Testing the Application

### User Flow Test:
1. ✅ Visit home page → See books
2. ✅ Click category → Filter works
3. ✅ Click book → See details
4. ✅ Add to cart → Cart updates
5. ✅ View cart → See items
6. ✅ Update quantity → Total updates
7. ✅ Checkout → Fill form
8. ✅ Place order → See confirmation

### Admin Test:
1. ✅ Login to admin
2. ✅ Add new book
3. ✅ View orders
4. ✅ Update order status

## Troubleshooting

### "Can't connect to MySQL"
```bash
sudo systemctl start mysql
sudo systemctl status mysql
```

### "Database doesn't exist"
```bash
mysql -u root -p
CREATE DATABASE bookstore_db;
```

### "Port 8000 already in use"
```bash
# Kill process
sudo lsof -t -i tcp:8000 | xargs kill -9

# Or use different port
python manage.py runserver 8080
```

### "No module named 'mysqlclient'"
```bash
source ../venv/bin/activate
pip install mysqlclient
```

## Project URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Book Detail | http://127.0.0.1:8000/book/1/ |
| Cart | http://127.0.0.1:8000/cart/cart/ |
| Checkout | http://127.0.0.1:8000/orders/place-order/ |
| Admin | http://127.0.0.1:8000/admin/ |

## Stop Server
Press `Ctrl + C` in terminal

---

**Ready to go! 🎉**
