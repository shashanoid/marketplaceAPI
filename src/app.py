from flask import Flask, jsonify, make_response, abort
import pymysql
import itertools
import datetime
import time
import config


class Handler:
    app = Flask(__name__)

    connection = pymysql.connect(config.db_data["host"], config.db_data["user"],\
                                 config.db_data["pass"], config.db_data["db"])
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cart_id = None
    cart_total = 0
    product_map = {}

    def __init__(self):
        return None

    def index(self):
        return make_response("Shopify products/cart API challenge")

    # Returns all products with available inventory
    def get_all_products(self):
        sql = "SELECT * FROM products WHERE inventory_count > 0"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return self.end('products', result)

    # Gets a product
    def get_product(self, product_id):
        sql = "SELECT * FROM products WHERE id= '%d'"
        self.cursor.execute(sql % product_id)
        result = self.cursor.fetchone()

        if result is not None:
            return self.end('product', result)
        else:
            abort(404)

    # Checks if product is available
    def check_inventory(self, product_id):
        check_inventory_query = "SELECT * FROM products WHERE id=%d AND \
                            inventory_count > 0" % product_id
        self.cursor.execute(check_inventory_query)
        result = self.cursor.fetchone()

        if result is not None:
            return True
        else:
            return False

    # Initializes a cart
    def initialize_cart(self):
        if self.cart_id is None:
            self.cart_id = 1
        self.product_map.clear()
        self.cart_total = 0

        return self.end('Success', 'Cart ID %d Initilized' % self.cart_id)

    # Displays contents of the current cart
    def view_cart(self):
        try:
            product_ids = [id for id in self.product_map.keys()]
            if len(product_ids) == 1:
                items_query = "SELECT * FROM products WHERE id=%d" % product_ids[0]
            else:
                id_tuple = tuple(product_ids)
                items_query = "SELECT * FROM products WHERE id IN {0}".format(id_tuple)

            self.cursor.execute(items_query)
            result = self.cursor.fetchall()
            return jsonify({'cart_id': self.cart_id, 'products': result,\
                            'total': self.cart_total})
        except:
            return self.end('Error', 'Cart is empty')

    # Adds products to the cart
    def add_to_cart(self, product_id):
        if self.cart_id is not None:
            if self.check_inventory(product_id) is True:
                if product_id not in self.product_map:
                    self.product_map.update({product_id: 1})
                else:
                    product_count = self.product_map[product_id]
                    self.product_map.update({product_id: product_count + 1})
                get_price_query = "SELECT price FROM products \
                                  WHERE id={0}".format(product_id)
                self.cursor.execute(get_price_query)
                product_price = self.cursor.fetchone()['price']
                self.cart_total = self.cart_total + product_price
                return self.end('Success', "Successfully added to your cart")
            else:
                return self.end('Error',"Product is not available at this moment")
        else:
            return self.end('Error',"Please initialize a cart to purchase this product")

    # Deletes an product from the cart
    def delete_from_cart(self, product_id):
        if self.cart_id is not None:
            if product_id in self.product_map:
                del self.product_map[product_id]
                return self.end('Success','Successfully deleted from the cart')
            else:
                return self.end('Error','Item not in your cart')
        else:
            return self.end('Error', "Please initialize a cart to purchase this product")

    # Completes the cart, updates inventory and logs it
    def checkout_cart(self):
        if self.cart_id is not None:
            if len(self.product_map) > 0:
                for product, quantity in self.product_map.iteritems():
                    purchase_item_query = "UPDATE products SET inventory_count=inventory_count-{0} \
                                          WHERE id={1}".format(quantity, product)
                    self.cursor.execute(purchase_item_query)
                    self.connection.commit()

                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                order_query = "INSERT INTO orders (total, complete, created_at) VALUES ({0}, \
                              True, '{1}')".format(self.cart_total, str(timestamp))
                self.cursor.execute(order_query)
                self.connection.commit()
                self.reset()
                return self.end("Success", "Checkout successful !")
            else:
                return self.end("Error", "Empty cart, please add some items")
        else:
            return self.end("Error","Initialize a cart first to checkout")

    # Resets data
    def reset(self):
        self.product_map.clear()
        self.cart_total = 0
        self.cart_id = None

    @staticmethod
    def not_found(e):
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    @staticmethod
    def end(response_type, response):
        return make_response(jsonify({response_type:response}))

if __name__ == '__main__':
    handler = Handler()
    handler.app.register_error_handler(Exception, handler.not_found)
    handler.app.add_url_rule('/', 'index', handler.index)
    handler.app.add_url_rule('/products', 'products', handler.get_all_products)
    handler.app.add_url_rule('/product/<int:product_id>', 'getProduct', handler.get_product, methods=['GET'])
    handler.app.add_url_rule('/product/add/<int:product_id>', 'add', handler.add_to_cart, methods=['GET'])
    handler.app.add_url_rule('/product/delete/<int:product_id>', 'delete', handler.delete_from_cart, methods=['GET'])
    handler.app.add_url_rule('/cart/init', 'initialize', handler.initialize_cart)
    handler.app.add_url_rule('/cart', 'view', handler.view_cart)
    handler.app.add_url_rule('/cart/checkout', 'checkout', handler.checkout_cart)
    handler.app.secret_key = 'qwerty123@'
    handler.app.run(debug=True, port=8000)
    handler.connection.close()
    