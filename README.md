# fashion-ecoommerce-part1

## I. Purpose
MongoDB, with its JSON-like format and user-friendly integration with web applications, was selected as the database for our e-commerce platform. Its schema-less design facilitates quick adaptations and expansions, a vital feature for the ever-changing landscape of e-commerce. This flexibility is crucial for handling complex and varied data structures, including product collections with diverse SKUs, detailed user profiles, and secure payment information storage.

The database schema is meticulously crafted to manage product lines and user data effectively. It places a strong emphasis on unique email identifiers for user accounts and employs secure methods for storing sensitive credit card details, aligning with data protection standards. Moreover, the schema design addresses the handling of order data by adopting a static approach. This strategy, which focuses on capturing essential details like shipping addresses and tracking IDs in a non-dynamic format, ensures the reliability and consistency of transactional records, a key factor in maintaining the integrity of the e-commerce platform.


## II. Tasks
### Step 1. Schema Design
MongoDB, known for its JSON-like format and user-friendly web application integration, was chosen for our e-commerce platform's database. Its schema-less design is key for quick adaptations in the ever-changing e-commerce environment, allowing for the management of complex data structures. This includes product collections with diverse SKUs, detailed user profiles, and secure payment information storage.

The schema is designed to ensure effective management of product lines and user data, focusing on unique email identifiers for user accounts and secure storage methods for sensitive credit card details, in line with data protection standards. A static approach to order data maintains the reliability and consistency of transactional records, crucial for the platform's integrity.

#### Users Collection Structure
- **email**: Unique email for user identification and login.
- **firstName** and **lastName**: For user personalization and identification.
- **hashedPassword**: Securely stored for privacy and safety.
- **billingAddress** and **shippingAddress**: Includes country, streets, city, state, and zip for accurate billing and delivery.

#### Key Points:
- **Security**: Utilizes hashed passwords for data protection.
- **User Identification**: Email prevents duplicate accounts.
- **User Experience**: Names and addresses provide personalization.

#### Products Collection Structure
- **name**: Identifier of the product.
- **description**: Details about the product.
- **price**: Cost of the product.
- **skus**: Variants including size and quantity.
- **category**: Type of product for organization.
- **picture**: Visual reference for the product.

#### Key Points:
- **Detailed Descriptions & Images**: Aids user decision-making.
- **Effective Inventory Tracking**: SKU details for stock management.
- **Organized Display**: Categorization for user-friendly navigation.

#### Orders Collection Structure Overview
- **userId**: Identifier for the customer's order.
- **paymentStatus**: Transaction condition (e.g., 'processed', 'authorized', 'declined').
- **status**: Fulfillment stage (e.g., 'delivered', 'pending', 'cancelled').
- **amount**: Financial total of the order.
- **items**: Product details in the order.
- **shippingAddress** & **billingAddress**: Details for accurate order processing.
- **trackingNumber**: For delivery tracking.

#### Key Points:
- **Security and Privacy**: Excludes direct payment details for security.
- **Data Consistency**: Employs static data for accuracy.
- **User-Centric Design**: Includes comprehensive details for customer experience.

#### Payment Collection Structure
- **userId**: Links payment to the user.
- **type**: Payment type (e.g., credit, debit, digital wallets).
- **cardDetails** (if applicable):
  - **type**: Card provider (e.g., Visa, Mastercard).
  - **lastFour**: Identification digits.
  - **expiry**: Expiration date.
  - **cvvVerified**: CVV confirmation status.

#### Key Points:
- **Security**: Minimal card details for safety.
- **Variety**: Various payment types for convenience.
- **Compliance**: Verified and secure payment methods.


### Step 2. Data Transformation and Import
Using the outlined schema design, I generated mock data in .json format with assistance from ChatGPT. This data was then preserved as reference files. To integrate this data into the MongoDB environment, I employed a specific import process using Pymongo. An example that illustrates the import process specifically for the **'products.json'** file is detailed below:

```python
# connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]


# define collections
products = db["products"] 
users = db["users"]
payments = db["payments"]
orders = db["orders"]


# loop through products.json rows and insert into MongoDB
with open('products.json', 'r') as file:
    data = json.load(file)
    for row in data['products']:
        print(row)
        products.insert_one(row)
```
### Step 3. Set-up
Begin by launching your MongoDB instance through Docker by executing the command docker-compose up -d. This will set up MongoDB in a detached mode, allowing continuous access to the database service.

Once MongoDB is up and running, initiate the MongoDB Shell (mongosh) with the following command to interact with your database:
```bash
docker-compose exec mongodb mongosh
```
Within this shell, you can explore the backend of your database, making a wide array of changes and querying data directly.

If you need to enter the shell environment for MongoDB, enter:
```bash
docker-compose exec mongodb sh
```
To get the Flask app up and running, open a new terminal window and run:
```bash
python run-app.py
```
This will start your Flask application. Now, when you first open Postman, you will be greeted at the default address, confirming that the backend is operational and ready for interaction.

### Step 4. Flask App Queries
#### Homepage
The project's homepage sets the stage for a user-friendly experience. When users access the default root URL path (/ or http://localhost:5000/), they're greeted with a welcome message. This welcoming message doesn't require complex HTML rendering; instead, it's delivered through a straightforward JSON response.
<p align="center">
  <img width="817" alt="welcome" src="https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/becc1823-c577-4053-9c4c-1d815fa10ad8">
</p>

#### Create Products
This endpoint enables users to add new products by submitting data that must contain the essential fields: 'name', 'description', 'price', and 'category'. Correct entries result in the products being stored in the database with their unique IDs provided in response. In case of missing fields or server issues, the system will return relevant error messages to assist in troubleshooting.

As you see below, once users submit all the necessary key-value pairs, they will receive a successful response that includes the new **object_id** of the entry.
![create1](https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/bb12a35e-0869-419b-94ad-69cb039de579)

If users omit any of the required fields — 'name', 'description', 'price', or 'category' — they will be notified with a message indicating that one or more fields are missing.
![create2](https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/c20d855b-e44e-4d69-b5f5-63f2e00c83e3)

The successful addition of the new product to our database can be confirmed through a query in mongosh, as demonstrated.

<img width="486" alt="new product" src="https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/ace913a0-b83d-4cef-a4f4-9d113683c25d">

#### Inventory Update
The **'/update_inventory'** endpoint is designed to modify the quantity of a specific product based on its name and size. You can simply submit the product details and choose to 'increment' (add) or 'decrement' (subtract) from the inventory. Default adjustments reduce the stock by one. Successful changes are confirmed, or an error is flagged if the product doesn't exist.

Here's an example of subtracting the stock for the S size "Relaxed Fit Coat" by 2
<img width="817" alt="increament" src="https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/020b17e0-f9a4-4598-9177-ab2932154650">

After updating the inventory, a check in the database shows that the quantity of the S size "Relaxed Fit Coat" has successfully decreased from 30 to 28.

![decrement_result](https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/9b09436d-3ccc-42f3-81ef-614a6a9619ec)

Now, we have added the stock for the S size "Relaxed Fit Coat" by 2.

<img width="817" alt="increament" src="https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/42590d6c-4232-45bb-88dc-d132426a0afd">

The increment process was successfully executed, and the stock for the S size "Relaxed Fit Coat" has been updated, increasing from 28 to 30.

![increment_result](https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/e6d934a8-e7f1-46e9-96cd-2fd9d485df8b)

#### Different Shipping and Billing addresses
The function is designed to fetch users who have distinct shipping and billing addresses. It's particularly useful in scenarios where address verification or specialized marketing strategies are required. On success, it returns a list of these users, including their user IDs and both addresses. 

<img width="819" alt="different address" src="https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/5a3d20e3-5504-4d89-9869-a8f1edddc365">

#### Total Sales
The endpoint is designed to calculate the total sales amount(pre-tax and after-tax) for a specific product. Users would provide the **'product_name'** to calculate, and the responses indicate successful totals or errors for missing parameters and server issues. It's a useful function for analyzing sales performance and tracking product popularity.

![total_sales](https://github.com/minu803/fashion-ecommerce-part1/assets/111295624/329eac5e-8c76-4538-94a0-06a37ec74972)

#### Expired Credit Cards

#### Count Payment Types

#### Users with Incomplete Addresses

#### Users by Area

## III. Use of GenAI
1. **Convert ObjectId:**


2. **delete_by_job_title:**


3. **Comments:**



