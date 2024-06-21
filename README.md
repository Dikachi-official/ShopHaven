# ShopHaven
<p>MultiVendor E-commerce Platform</p>

## Overview

ShopHaven is a dynamic and scalable solution designed to empower multiple vendors to sell their products online seamlessly. This platform leverages Python and Django for backend operations, with HTML, CSS, and JavaScript enhancing the frontend experience. It offers a comprehensive suite of features tailored for both vendors and customers, ensuring a user-friendly interface and robust functionality for managing and growing an online marketplace.

## Table of Contents

- [Features](#features)
  - [General Features](#general-features)
  - [Vendor Features](#vendor-features)
  - [Customer Features](#customer-features)
  - [Admin Features](#admin-features)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Development](#development)
- [Deployment](#deployment)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Features

### General Features
- **Responsive Design**: Fully optimized for various screen sizes and devices.
- **Secure User Authentication**: Includes registration, login, password management, and optional social media authentication.
- **Comprehensive Search and Filtering**: Advanced product search and filtering capabilities to enhance user experience.
- **Notifications**: Real-time updates for orders, messages, and other activities.

### Vendor Features
- **Vendor Registration and Profile Management**: Vendors can create and personalize their profiles.
- **Product Management**: Easy-to-use interface for adding, editing, and removing products.
- **Order and Inventory Management**: Vendors can track and manage orders and maintain their inventory.
- **Sales Reports and Analytics**: Detailed insights into sales performance and customer behavior.

### Customer Features
- **User-Friendly Shopping Cart**: Add, update, and remove products with ease.
- **Order Tracking**: Customers can track the status of their orders and view order history.
- **Product Reviews and Ratings**: Customers can leave feedback and ratings for products.
- **Wishlist**: Save products for future purchase.

### Admin Features
- **Dashboard Management**: A powerful dashboard for overseeing the entire platform.
- **User and Vendor Management**: Admins can manage both customers and vendors, including approvals and disputes.
- **Product and Category Management**: Admins have control over product listings and categories.
- **Order and Payment Management**: Monitor and manage orders, payments, and refunds.

## Technology Stack

- **Backend**:
  - **Python**: Core programming language.
  - **Django**: Web framework for backend development.

- **Frontend**:
  - **HTML5**: Markup language for structuring web pages.
  - **CSS3**: Stylesheet language for designing web pages.
  - **JavaScript**: For interactive and dynamic content.
  - **Bootstrap**: Framework for responsive and modern UI design.
  - **jQuery**: Simplifies JavaScript interactions and AJAX requests.

- **Database**:
  - **SQLite**: Django default database management system.
  - **PostgreSQL**: Relational database management system.

- **Others**:
  - **Celery**: Task queue for handling asynchronous tasks.
  - **Stripe/PayPal**: Payment processing gateways.
    



## Installation and Setup

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8+
- PostgreSQL


### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Dikachi-official/ShopHaven.git
   cd ShopHaven
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Backend Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL** (Optional):
   - Create a new PostgreSQL database and user.
   - Update the `DATABASES` configuration in `settings.py` with your database details.

5. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

8. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```



## Usage

- Access the platform at `http://localhost:8000` to view the homepage.
- Visit `http://localhost:8000/admin` to access the admin dashboard using the superuser credentials created during setup.
- Vendors and customers can register and manage their activities from their respective dashboards.

## Development

To contribute to this project:

1. **Fork the repository**.
2. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes** with a clear message:
   ```bash
   git commit -m 'Add feature or fix'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Submit a pull request** and describe your changes in detail.

## Deployment

For a production-ready deployment, we recommend using Docker and Nginx:

1. **Build Docker Images**:
   ```bash
   docker-compose build
   ```

2. **Run Docker Containers**:
   ```bash
   docker-compose up -d
   ```

3. **Configure Nginx**:
   - Update `nginx.conf` to include your domain and server details.
   - Ensure Nginx is set up to handle HTTPS for secure connections.

4. **Secure Your Application**:
   - Use SSL/TLS certificates to secure communication.
   - Set up environment variables securely.

