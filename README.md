# Shopify MarketPlace API
This API represents barebones of an online marketplace. It allows you to view all the products in the inventory and fits them into the context of a simple shopping cart.

### Clone project into a virtual environment
```sh
git clone https://github.com/shashanoid/marketplaceAPI.git
```

### Install required tools

```sh
pip install -r requirements.txt
```
### Setup MySQL
- Install MySQL in your system.
- Create a database named '**cart**'
- Select **cart** as your schema and import SQLFiles/Cart_db.sql
- Edit config.py accordingly with your credentials.
### Run
```sh
cd src
python2 app.py
```

### API Endpoints
- To interact with the cart (add/delete/empty/checkout), it's necessary to initialize the cart first.
- #### **/products**

```coffee
curl -i http://localhost:8000/products

'Returns a list of all available products (inventory count > 0)'

{
  "products": [
    {
      "id": 1, 
      "inventory_count": 20, 
      "price": 600.0, 
      "title": "Iphone X"
    }, 
    {
      "id": 2, 
      "inventory_count": 9, 
      "price": 40.0, 
      "title": "Ipod Mini"
    }
  ]
}
```
- #### **/product/id=<integer_value>**
```sh
curl -i http://localhost:8000/product/id=5

'Returns all details about a specific product'

{
  "product": {
    "id": 5, 
    "inventory_count": 18, 
    "price": 120.0, 
    "title": "Bose QC 35"
  }
}
```
- #### **/cart/init**
```sh
curl -i http://localhost:8000/cart/init

'Initializes an empty cart'

{
  "message": "Cart ID 1 Initilized", 
  "success": true
}
```
- #### **/product/add/id=<integer_value>**
```sh
curl -i http://localhost:8000/product/add/id=1

'Adds the product to the cart. Calling this multiple times
would multiply the product count in the cart and will reflect
in the total amount'

{
  "message": "Successfully added to your cart", 
  "success": true
}
```
- #### **/product/delete/id=<integer_value>**
```sh
curl -i http://localhost:8000/product/delete/id=1

'Deletes a product from the cart'

{
  "message": "Successfully deleted from the cart", 
  "success": true
}
```
- #### **/cart**
```sh
curl -i http://localhost:8000/cart

'Displays contents of the cart along with total amount'

{
  "cart_id": 1, 
  "products": [
    {
      "id": 1, 
      "inventory_count": 20, 
      "price": 600.0, 
      "title": "Iphone X"
    }, 
    {
      "id": 5, 
      "inventory_count": 18, 
      "price": 120.0, 
      "title": "Bose QC 35"
    }
  ], 
  "total": 1320.0
}
```
- #### **/cart/emptycart**
```sh
curl -i http://localhost:8000/cart/emptycart

'Resets the cart'

{
  "message": "Your cart is now empty", 
  "success": true
}
```
- #### **/cart/checkout**
```sh
curl -i http://localhost:8000/cart/checkout

'Checks out a cart, updates product inventory and logs the details 
into 'orders' database'

{
  "message": "Checkout successful !", 
  "success": true
}
```

**Note:** Endpoints mentioned above can be accessed through the browser as well. Simply paste
the mentioned URLs into the address bar.

### Design Considerations

The application uses Python's Flask framework as it is extremely lightweight, customizable and simple. This makes it ideal for designing APIs with not so complex endpoints.

The application uses MySQL as its database since it makes simple SQL queries which becomes relatively easy with libraries like 'pymysql'.
