# Shopify API Challenge

### To run the project
- Make sure to have MySQL installed with a database setup
- Import all SQL files to your database from SQLFiles
- Edit src/config.py and enter your credentials

#### Clone project into a virtual environment
```sh
git clone https://github.com/shashanoid/marketplaceAPI.git
```

#### Install required tools

```sh
pip install -r requirements.txt
```

#### Run
```sh
cd src
python2 app.py
```

#### Endpoints
- **/products** - Returns all available products
- **/product/<int:product_id>** - Returns specific product details
- **/cart/init** - Initializes a cart
- **/product/add/<int:product_id>** - Adds a product to the cart
- **/product/delete/<int:product_id>** - Deletes a product from the cart
- **/cart** - Displays the cart with products and total amount
- **/cart/checkout** - Checks out a cart, updates inventory and logs into "orders" database
