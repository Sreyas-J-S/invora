# Invora - Invoice Management System

A comprehensive invoice management application built with Django. This system allows you to manage products, customers, and invoices efficiently, with built-in profit calculation and reporting features.

## Features

-   **Dashboard**: Overview of total products, invoices, and income.
-   **Invoice Management**: Create, view, and delete invoices.
-   **Product Management**: Add, edit, and delete products with cost and selling prices.
-   **Excel Export**: Download all invoices as an Excel file for offline analysis.
-   **Profit Calculator**: Visual monthly profit reports with interactive charts.
-   **User Profile**:
    -   Secure Login/Logout.
    -   Edit Profile (Username/Email).
    -   Change Password.
-   **Premium UI**: Modern glassmorphism design with animations and a custom wallpaper.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd django-invoice-management-master
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the application:**
    Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

-   **Login**: Use your superuser credentials to log in.
-   **Dashboard**: View key metrics at a glance.
-   **Products**: Navigate to "Products" to manage your inventory.
-   **Invoices**: Go to "Invoices" to generate bills for customers.
-   **Profit Calculator**: Check the "Profit Calculator" tab for financial insights.
-   **Settings**: Access "Settings" in the sidebar to manage your account.

## Credits

**BUILD BY SREYAS**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
Copyright (c) 2025 Sreyas.
