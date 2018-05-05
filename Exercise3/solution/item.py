from flask_restful import Resource, Api, reqparse
import sqlite3

# Represents the Item resource
class Item(Resource):
	# class attribute - setup parser to extract values from request body
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    # class method - find item by name or return None
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table='items')
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    # class method - insert a new item
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    # class method - update an item
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

	# GET /item/<name>
	# Description: Get item by name
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item, 200
        else:
            return {'message': 'Item not found'}, 404

	# POST /item/<name>
	# Description: Create item
    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with name 'ball' already exists."}, 400

        data = Item.parser.parse_args()

        item = { "name": name, "price": data['price'] }
        try:
            self.insert(item)
        except:
            return {'message': 'An error occured inserting the item.'}, 500 # Internal Server Error

        return item, 201

    # PUT /item/<name>
    # Description: Create or update item
    def put(self, name):
        data = Item.parser.parse_args()

        # search for item by name
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        # Update exisiting item
        if item:
            try:
                self.update(updated_item)
                return updated_item, 200
            except:
                return {'message': 'An oeeor occured inserting the item'}, 500
        # Insert new item
        else:
            try:
                self.insert(updated_item)
                return updated_item, 201
            except:
                return {'message': 'An oeeor occured inserting the item'}, 500

	# DELETE /item/<name>
	# Description: Delete an item
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}, 200

# Represents an Item collection resource
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}, 200
