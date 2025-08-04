# Ecommerce RESTful API

## 📋 Description

This is a RESTful API built with **Django REST Framework** for managing an eCommerce platform. It provides endpoints for managing:

- Users & Admins
- Categories
- Products
- Cart & Orders

Key features include JWT-based authentication, product categorization, caching techniques, order placement, and more.

## 🚀 Features

### User/Admin Management
- **User Creation**: Register new users.
- **Authentication**: Secure login using **JWT** (JSON Web Tokens).
- **Profile Update**: Allow users to update their profile information.
- **Logout**: Secure logout functionality.

### Category Management
- **CRUD Operations**: Create, Read, Update, Delete categories.

### Product Management
- **CRUD Operations**: Create, Read, Update, Delete products.
- **Caching**: Caching for product and category lists to improve performance.
- **Pagination**: Pagination for product listing.
- **Filters**: Filter products based on category and price range.

### Cart Handling
- **Add Products to Cart**: Users can add products to their shopping cart.
- **Item Quantity Management**: Increment and decrement item quantities.
- **Remove Items**: Users can remove products from their cart.

### Order Handling
- **Order Placement**: Users can place orders.
- **Order History**: Users can view their order history.
- **Order Notifications**: Real-time notifications on order status changes using **Django Channels**.

### Role-Based Access Control (RBAC)
- **Admin Access**: Admins can manage products, categories, and user permissions.
- **Permissions**: Admin access controlled via Django REST framework’s permission classes.

## 🛠️ Technologies Used
- **Django REST Framework**
- **PostgreSQL**
- **Django Rest Framework SimpleJWT** for authentication
- **Redis** for caching and real-time notifications via Django Channels
- **Django Channels** for real-time notifications and asynchronous features

## 🔧 Setup Instructions

### Prerequisites
- **Python 3.13+**
- **pip** (Python package installer)
- **venv** (for creating a virtual environment)
- **Redis** (For caching and notifications)
- **PostgreSQL** (For the database)

### Installation Steps

1. **Clone the Repository:**

```bash
git clone https://github.com/arjunvjn/ENLOG-Ecommerce.git
cd ENLOG-Ecommerce/Ecommerce
```

2. **Create and Activate a Virtual Environment:**

```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment
# On macOS/Linux:
source myenv/bin/activate

# On Windows (Command Prompt):
myenv\Scripts\activate

# On Windows (PowerShell):
myenv\Scripts\Activate.ps1
```

3. **Install the Required Packages:**

```bash
pip install -r requirements.txt
```

4. **Install and Run Redis:**

### Installation:

- On macOS with Homebrew:
```bash
brew install redis
 ```

 - On Linux:
```bash
sudo apt-get install redis-server
```
- On Windows:

Download and install Redis from Redis for Windows.

### Start Redis Server:
```bash
redis-server
```

5. **Setup the .env File:**

Create a .env file in the root of your project (next to manage.py).

```bash
# PostgreSQL settings
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

6. **Migrate the Database:**

```bash
python manage.py migrate
```

7. **Run the Django Server:**

```bash
python manage.py runserver
```