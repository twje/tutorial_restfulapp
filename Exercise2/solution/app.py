from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask to propage an exception even if debug is set to false on app
api = Api(app)
 
# In memory database
items = [] 

# Represents the Item resource
class Item(Resource):
	# class attribute - setup parser to extract values from request body
	parser = reqparse.RequestParser()
	parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
	
	# GET /item/<name>
	# Description: Get item by name
	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		return {'item': item}, 200 if item else 404
		
	# POST /item/<name>
	# Description: Create item		
	def post(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item:
			return {"message": "An item with name 'ball' already exists."}, 400				
		else:			
			request_data = Item.parser.parse_args()
			item = {
				"name": name,
				"price": request_data['price'],
			}
			items.append(item)			
			return item, 201

	# PUT /item/<name>
	# Description: Create or update item			
	def put(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		request_data = Item.parser.parse_args()
		if item:
			item.update({
				"price": request_data['price']
			})
			return {"price": request_data['price']}, 200		
		else:		
			item = {
				"name": name,
				"price": request_data['price'],
			}
			items.append(item)
			return {"price": request_data['price']}, 201		

	# DELETE /item/<name>
	# Description: Delete an item
	def delete(self, name):	
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item deleted'}, 200	

# Represents an Item collection resource
class ItemList(Resource):
    def get(self):
        return {'items': items}		
		
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
	
app.run(port=5000, debug=True)