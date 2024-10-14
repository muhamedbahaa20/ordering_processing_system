Order Processing System Documentation


Table of Contents
1. Introduction
2. Requirements
3. Setup Instructions
4. API Endpoints
5. Error Handling
6. Testing






1. Introduction
The Order Processing System is a Django-based application designed to manage customer orders, validate stock availability, process payments, and send order confirmation emails. This document outlines the setup process, usage instructions, and details about the application's functionality.
2. Requirements
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Django 3.2 or higher
- A database (SQLite, PostgreSQL, etc.)
- pip (Python package installer)
3. Setup Instructions

Run docker
“docker-compose up”
```bash
python manage.py createsuperuser
```
### Start the Development Server

Run the following command to start the server:

```bash
python manage.py runserver
```
The application will be accessible at `http://127.0.0.1:8000`.
4. API Endpoints
Create an Order
- URL: `/ order/`
-Authentication :Bearer token
- Method: `POST`
- Request Body:
```json
{
    "customer_id": 1,
    "product_id": 1,
    "quantity": 2
}
```
- **Response:**
- Success: `{"status": "Order Completed Successfully."}`
- Failure: `{"status": "Insufficient balance."}` or `{"status": "Stock unavailable."}`
Get All Customers
- URL: `order/customers`
- **Method:** `GET`
- Response:
```json
{
    "customers": [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "balance": 100}
    ]
}
```
Get All Products
- URL: `order/products`
- Method: `GET`
- Response:
```json
{
    "products": [
        {"id": 1, "name": "Product 1", "price": 25.00, "stock": 10}
    ]
}
```
5. Error Handling
The application includes error handling for various scenarios, including:
- Invalid JSON format
- Missing required fields
- Stock availability issues
- Insufficient customer balance
Error messages will be logged for debugging and can be found in the logs.
6. Testing
To test the API, you can use Postman or a similar tool. Below are some test cases to validate the functionality:
- Valid Order Creation: Ensure that valid requests create orders successfully.
- Insufficient Stock: Test with requests that exceed available stock.
- Insufficient Balance: Test with customers who do not have enough balance.


