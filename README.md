# 🛒 E-Commerce Web Application

A full-stack e-commerce web application built using **Python Flask and MySQL**. The application provides user authentication, product management, shopping cart functionality, checkout, order management, and invoice generation.

The application is deployed on **Render** and uses **Aiven MySQL** as the production database.

## 🚀 Live Demo

🔗 https://e-commerce-project-1-0rsg.onrender.com

## ✨ Features

### 👤 User Features

- User registration and login
- Session-based authentication
- Product browsing
- Add products to cart
- Update cart item quantities
- Checkout functionality
- Order placement and management
- Invoice generation

### 🔐 Admin Features

- Admin login
- Product management
- Order management

### 🛡️ Security

- Session-based authentication
- Environment-based configuration
- Secure database connection using SSL

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Flask Session |
| Payment | Razorpay |
| Deployment | Render |
| Database Hosting | Aiven MySQL |
| Server | Gunicorn |

## 🏗️ Application Workflow

1. Users register or log in to the application.
2. Users browse available products.
3. Products can be added to the shopping cart.
4. Users update quantities and proceed to checkout.
5. Orders are placed and stored in the MySQL database.
6. Users can manage their orders and generate invoices.
7. Admins can manage products and orders.

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/manojkumarbathula/e-commerce_project.git
cd e-commerce_project
```

### 2. Create a Virtual Environment

```bash
python -m venv ecom
```

Activate the virtual environment:

**Windows:**

```bash
ecom\Scripts\activate
```

**Linux/macOS:**

```bash
source ecom/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and configure the required application settings, including database credentials and application secrets.

> Do not commit `.env` files or sensitive credentials to the repository.

### 5. Run the Application

```bash
python app.py
```

Open the application in your browser using the local URL displayed by Flask.

## ☁️ Deployment

- **Application Hosting:** Render
- **Database Hosting:** Aiven MySQL
- **Production Database Connection:** MySQL over SSL
- **Application Server:** Gunicorn

## 📌 Future Improvements

- Product search and filtering
- Pagination
- User profile management
- Improved responsive UI
- Automated testing
- AI-powered product recommendations

## 👨‍💻 Author

**Manoj Kumar Bathula**

- GitHub: https://github.com/manojkumarbathula
