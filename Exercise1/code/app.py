from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask to propage an exception even if debug is set to false on app 
 
# In memory database
items = [] 
 
# GET /items
# Description: Get all items
@app.route('/items') 
def getAllItems():
	return jsonify({'items': items})
 
# GET /item/<name>
# Description: Get item by name
@app.route('/item/<string:name>')
def getItem(name):
	item = next(filter(lambda x: x['name'] == name, items), None)
	if item:
		# Add logc here
		pass		
	else:
		return jsonify({"item": item}), 404

# POST /item/<name>
# Description: Create item
@app.route('/item/<string:name>', methods=['POST'])
def createItem(name):
	item = next(filter(lambda x: x['name'] == name, items), None)
	if item:
		return jsonify({"message": "An item with name 'ball' already exists."}), 400				
	else:
		request_data = request.get_json()
		item = {
			"name": name,
			"price": request_data['price'],
		}
		# Add logc here		
 
# PUT /item/<name>
# Description: Create or update item
@app.route('/item/<string:name>', methods=['PUT'])
def updateItem(name):
	item = next(filter(lambda x: x['name'] == name, items), None)
	request_data = request.get_json()
	if item:
		item.update({
			"price": request_data['price']
		})
		return jsonify({"price": request_data['price']}), 200		
	else:		
		# Add logc here
		return jsonify({"price": request_data['price']}), 201		

# DELETE /item/<name>
# Description: Delete an item
@app.route('/item/<string:name>', methods=['DELETE'])
def deleteItem(name):	
	global items
	items = list(filter(lambda x: x['name'] != name, items))
	return jsonify({'message': 'Item deleted'}), 200	
		
app.run(port=5000, debug=True)