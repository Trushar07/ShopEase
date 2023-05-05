# ShopEase, an E-commerce Website Backend with Django and Django Rest Framework

This is the backend implementation of an E-commerce website built using Django and Django Rest Framework.

## Requirements

To run this project, you need to have the following installed on your machine:

- Python with pip

## Installation

1. Clone the repository:<br />
`git clone https://github.com/Trushar07/ShopEase.git`

2. Create a virtual environment:<br />
`python -m venv env`

3. Activate the virtual environment:<br />
`source env/bin/activate`

4. Install the dependencies:<br />
`pip install -r requirements.txt`

5. Apply the database migrations:<br />
`python manage.py migrate`

6. Run the development server:<br />
`python manage.py runserver`

## API Endpoints

The following API endpoints are available:

### Authentication
Authentication is implemented using Djoser. Below are some important endpoints but there are many more. Checkout Djoser documentation to know more about other endpoints.

- POST `/auth/jwt/token/` - Obtain JWT authentication token
- POST `/auth/jwt/refresh/` - Refresh JWT authentication token

### Products

- GET `/store/products/` - List all products
- GET `/store/products/{id}/` - Retrieve a single product by ID
- POST `/store/products/` - Add new product (Only admin users)
- DELETE `/store/products/{id}` - Delete product (Only admin users)

### Product Reviews

- GET `/store/products/{id}/reviews` - List all product reviews
- GET `/store/products/{id}/reviews/{id}` - Retrieve a single product review by ID
- POST `/store/products/{id}/reviews/` - Add review of a product
- PUT `/store/products/{id}/reviews/{id}` - Update product review
- DELETE `/store/products/{id}/reviews/{id}` - Delete product review

### Collections

- GET `/store/collections/` - List all collections
- GET `/store/collections/{id}/` - Retrieve a single collection by ID
- POST `/store/collections/` - Add collection (Only admin users)
- PUT `/store/collections/{id}` - Update collection (Only admin users)
- DELETE `/store/collections/{id}` - Delete product (Only admin users)

### Carts

- POST `/store/carts/` - Create a new cart
- DELETE `/store/carts/{id}/` - Delete a cart

### Cart Items
- GET `/store/cart/{id}/items` - Retrieve a cart items
- GET `/store/cart/{id}/items/{id}` - Retrieve a particular cart item
- POST `/store/cart/{id}/items/` - Add a new item to a cart
- PATCH `/store/cart/{id}/items/{id}` - Update item of a cart
- DELETE `/store/cart/{id}/items/{id}` - Delete a cart item

### Customers
These endpoints are secured and only admins can access them.

- GET `/store/customer/` - List all customers
- GET `/store/customers/{id}/` - Retrieve a single customer by ID
- POST `/store/customers/` - Add new customer
- PUT `/store/customers/{id}` - Update customer details
- DELETE `/store/customers/{id}` - Delete customer

### Orders

- GET `/store/orders/` - List all orders if user is admin otherwise only orders of a user
- GET `/store/orders/{id}/` - Retrieve a single order by ID
- PATCH `/store/orders/{id}` - Update an order (only admin users)
- DELETE `/store/orders/{id}` - Delete order (Only admin users)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
