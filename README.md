---
output:
  word_document: default
  html_document: default
---
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

##### Key Points:
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

##### Key Points:
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

##### Key Points:
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

##### Key Points:
- **Security**: Minimal card details for safety.
- **Variety**: Various payment types for convenience.
- **Compliance**: Verified and secure payment methods.


### Step 2. Data Transformation and Import
I read all the CSV files and created a consolidated table by performing a join using the primary key 'id'. Next, I extracted the essential columns as defined in the schema design, and these were used to create separate dataframes. Subsequently, I transformed all the entries within the dataframes into JSON format to prepare them for import into the MongoDB environment. These JSON files were also saved for reference. Finally, the data was imported into the Pymongo environment using the following procedure:




### Step 3. Flask App
#### Homepage
The project's homepage sets the stage for a user-friendly experience. When users access the default root URL path (/ or http://localhost:5000/), they're greeted with a welcome message. This welcoming message doesn't require complex HTML rendering; instead, it's delivered through a straightforward JSON response.


## III. Use of GenAI
1. **Convert ObjectId:**


2. **delete_by_job_title:**


3. **Comments:**



