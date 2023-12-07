'''Module for serving API requests'''

from app import app
from bson.json_util import dumps, loads
from flask import request, jsonify
import json
import ast # helper library for parsing data from string
from importlib.machinery import SourceFileLoader
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# 1. Connect to the client
client = MongoClient(host="localhost", port=27017)

# Import the utils module
utils = SourceFileLoader('*', './app/utils.py').load_module()

# 2. Select the database
db = client.ecommerce

# Select the collection: products
products = db.products

# Select the collection: users
users = db.users

# Select the collection: payments
payments = db.payments

# Select the collection: orders
orders = db.orders


# Route decorator that defines which routes should be navigated to this function
@app.route("/") # '/' for directing all default traffic to this function get_initial_response()
def get_initial_response():
    '''
    Endpoint to get the initial response.
    ---
    Purpose: 
    - Provides a welcome message to the users.
    '''
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to eCommerce Database'
    }
    resp = jsonify(message)
    # Returning the object
    return resp


####==================== Products ====================####
@app.route("/create/products", methods=['POST'])
def create_products():
    '''
    Function to create new product post(s)
    ---
    Purpose: 
    - Creates new product post(s) in the MongoDB.
    Accepted Parameters:
    - JSON request body containing product post data.
    Potential Responses:
    - 201: Successful creation with a list of IDs.
    - 400: Bad request if the request body is missing or invalid.
    - 500: Server error in case of an exception.
    
    '''
    try:
        # Create new product post
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
            #body = request.get_json()
            if body is None:
                raise ValueError("Request body is not valid JSON.")
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400
        
        # Define requred fields
        required_fields = ['name', 'description', 'price', 'category']

        # Validate each item in the list
        for item in body:
            missing_fields = [field for field in required_fields if field not in item or not item[field]]
            if missing_fields:
                return f"Bad request: Missing or empty fields in item {body.index(item) + 1}: {', '.join(missing_fields)}", 400
        
        # Insert many field into the body
        record_created = products.insert_many(body)

        if record_created:
            inserted_id = record_created.inserted_ids
            # Prepare the response
            if isinstance(inserted_id, list):
                # Return list of Id of the newly created item
                ids = []
                for _id in inserted_id:
                    ids.append(str(_id))
                return jsonify(ids), 201
            else:
                # Return Id of the newly created item
                return jsonify(str(inserted_id)), 201
    except Exception as e:
        # Error while trying to create customers
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500


@app.route("/update_inventory", methods=['POST'])
def update_inventory():
    '''
    Update product quantity by name and size.
    ---
    Purpose: 
    - Increments/Decrements product quantity by product name and size.
    Accepted Parameters:
    - name, size, operation, and quantity to adjust.
    Potential Responses:
    - 200: Successful update with the product info.
    - 404: Product not found.
    - 500: Server error in case of an exception.
    '''
    try:
        # Fetch the data from the request
        product_name = request.form.get('name')
        product_size = request.form.get('size')
        operation = request.form.get('operation', 'decrement')  # Default operation is decrement
        change_amount = int(request.form.get('amount', 1))  # Default amount is 1

        # Find the product by name and size
        product = products.find_one({"name": product_name, "skus.size": product_size})
        if product is None:
            return jsonify({"message": "Product not found"}), 404

        # Determine increment or decrement
        update_value = change_amount if operation == 'increment' else -change_amount

        # Update the product quantity
        update_result = products.update_one(
            {"name": product_name, "skus.size": product_size},
            {"$inc": {"skus.$.quantity": update_value}}
        )
        
        # If the count is 0, then no changes were made
        if update_result.modified_count == 0:
            return jsonify({"message": "No changes made to the product quantity"}), 200

        return jsonify({"message": f"Product quantity {operation}ed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



####==================== Orders ====================####
@app.route('/different_addresses', methods=['GET'])
def get_users_with_different_addresses():
    '''
    Retrieve users with different shipping and billing addresses.
    ---
    Purpose: 
    - Retrieves users whose shipping address and billing address are different.
    Potential Responses:
    - 200: Successful retrieval of users.
    - 500: Server error in case of an exception.
    '''

    try:
        # Define a MongoDB aggregation pipeline to find users with different addresses
        # $expr allows us to use aggregation expressions within the $match stage
        pipeline = [
            {"$match": {
                "$expr": {
                    "$ne": ["$shippingAddress", "$billingAddress"]
                }
            }},
            {"$project": {
                "userId": 1,
                "shippingAddress": 1,
                "billingAddress": 1
            }}
        ]
        # Execute the aggregation pipeline and store the results
        results = list(orders.aggregate(pipeline))

        # Return a JSON response with the results
        return jsonify(str(results)), 200

    except Exception as e:
        # Return a JSON response with an error message in case of an exception
        return jsonify({"error": str(e)}), 500

@app.route('/total_sales', methods=['GET'])
def get_total_sales():
    '''
    Retrieve total sales amount for a specified product.
    ---
    Purpose: 
    - Retrieves the total sales amount for a specified product from the orders collection.
    Accepted Parameters:
    - product_name: The name of the product to calculate total sales for
    Potential Responses:
    - 200: Successful retrieval of total sales.
    - 400: Bad request if the product_name parameter is missing.
    - 500: Server error in case of an exception.
    '''

    try:
        # Extract the 'product' name parameter from the request's query parameters
        product_name = request.form.get('product')

        # Check if 'product' parameter is missing or empty
        if not product_name:
            # Return a JSON response with an error message and a status code 400 (Bad Request)
            return jsonify({"error": "The product parameter is required"}), 400

        # Define a MongoDB aggregation pipeline to calculate total sales for the specified product
        pipeline = [
            {"$unwind": "$items"},
            {"$match": {"items.name": product_name}},
            {"$group": {
                "_id": "$items.name",
                "pretaxTotal": {
                    "$sum": "$items.preTax"
                },
                "afterTaxTotal": {
                    "$sum": "$items.afterTax"
                }
            }}
        ]
        # Execute the aggregation pipeline and store the results
        results = list(orders.aggregate(pipeline))

        # Return a JSON response with the results
        return jsonify(results), 200

    except Exception as e:
        # Return a JSON response with an error message in case of an exception
        return jsonify({"error": str(e)}), 500


#### ==================== Payments ==================== ####
@app.route('/expired_credit_cards', methods=['GET'])
def get_expired_credit_cards():
    '''
    Retrieve expired credit cards.
    ---
    Purpose: 
    - Retrieves credit cards that have expired.
    Potential Responses:
    - 200: Successful retrieval of expired credit cards.
    - 500: Server error in case of an exception.
    '''

    try:
        from datetime import datetime
        # Get current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Query to find an expired credit card
        expired_cards = list(payments.find({
            "$or": [
                {"card.expiryYear": {"$lt": current_year}},
                {"$and": [
                    {"card.expiryYear": current_year},
                    {"card.expiryMonth": {"$lt": current_month}}
                ]}
            ]
        }))
        
        # return a JSON response with the results
        return jsonify(str(expired_cards)), 200

    # Return a JSON response with an error message in case of an exception
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/count_payment_types', methods=['GET'])
def count_payment_types():
    '''
    Count each type of payment in the database.
    ---
    Purpose: 
    - Counts the number of each payment type (credit, debit, stripe, paypal).
    Potential Responses:
    - 200: Successful retrieval of payment type counts.
    - 500: Server error in case of an exception.
    '''

    try:
        # List of payment types to count
        payment_types = ['credit', 'debit', 'stripe', 'paypal']

        # Count for each payment type
        counts = {}
        for payment_type in payment_types:
            count = payments.count_documents({'type': payment_type})
            counts[payment_type] = count

        # Return a JSON response with the results
        return jsonify(counts), 200

    # Return a JSON response with an error message in case of an exception
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#### ==================== Users ==================== ####
@app.route('/incomplete_address_users', methods=['GET'])
def get_incomplete_address_users():
    '''
    Retrieve users with incomplete address information.
    ---
    Purpose: 
    - Identifies users who have missing fields in their billing address.
    Potential Responses:
    - 200: Successful retrieval of users with incomplete address information.
    - 500: Server error in case of an exception.
    '''

    try:
        # Find users with incomplete address information
        incomplete_address_users = list(users.find({
            "$or": [
                {
                    "$or": [
                        {"billingAddress.street 1": {"$exists": False}},
                        {"billingAddress.city": {"$exists": False}},
                        {"billingAddress.state": {"$exists": False}},
                        {"billingAddress.zip": {"$exists": False}}
                    ]
                },
                {
                    "$or": [
                        {"shippingAddress.street 1": {"$exists": False}},
                        {"shippingAddress.city": {"$exists": False}},
                        {"shippingAddress.state": {"$exists": False}},
                        {"shippingAddress.zip": {"$exists": False}}
                    ]
                }
            ]
        }))            

    # Return a JSON response with the results
        return jsonify([user['email'] for user in incomplete_address_users]), 200

    # Return a JSON response with an error message in case of an exception
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users_by_state_city', methods=['GET'])
def users_by_state_city():
    '''
    Aggregate users by state and city.
    ---
    Purpose: 
    - Aggregates and counts the number of users based on their state and city in the billing address.
    Potential Responses:
    - 200: Successful retrieval of user aggregation data.
    - 500: Server error in case of an exception.
    '''

    try:
        # Pipeline for aggregation
        pipeline = [
            {"$group": {"_id": {"state": "$billingAddress.state", "city": "$billingAddress.city"}, "count": {"$sum": 1}}}
        ]

        # Perform aggregation
        result = list(users.aggregate(pipeline))

        # Return a JSON response with the results
        return jsonify(result), 200

    # Return a JSON response with an error message in case of an exception
    except Exception as e:
        return jsonify({"error": str(e)}), 500










