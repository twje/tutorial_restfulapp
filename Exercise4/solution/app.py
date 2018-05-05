from flask import Flask
from flask_restful import Api
from resources.item import Item, ItemList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # '/data.db' path to database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # TRACK modifications are handled by the underlying SQLAlchemy and not the exstention (more efficient)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask to propage an exception even if debug is set to false on app
api = Api(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# Flask decorator - called automatically before the first web request
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
