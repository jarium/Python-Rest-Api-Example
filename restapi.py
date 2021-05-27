from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/USER/Desktop/Whatsappbot/thedb.db'
db = SQLAlchemy(app)

class Drink (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String(120))
    isDeleted = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return f"{self.name} - {self.description}"

#Main Page
@app.route("/")
def index():
    return "Hello, this is the main page"

#Show All Drinks
@app.route("/drinks", methods = ['GET'])
def get_all_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {"name": drink.name, "description": drink.description}
        if not drink.isDeleted:
            output.append(drink_data)
    if len(output) == 0:
        return {"message": "no drinks exist"}
    else:
        return {"drinks": output}

#Show Drinks(Pagination, 5 per page)
@app.route("/drinks/<int:page_num>", methods = ['GET'])
def all_drinks(page_num):
    drinks = Drink.query.paginate(per_page = 5, page = page_num, error_out = True)
    return render_template("index.html", drinks = drinks)

#Show a spesific drink with ID
@app.route("/drinks/spesific/<id>", methods = ['GET'] )
def get_drink(id):
    drink = Drink.query.get(id)
    if drink is None or drink.isDeleted == True:
       return {"error":"The drink does not exist"}
    else:
       return ({"name": drink.name, "description": drink.description})

#Add drink
@app.route("/drinks", methods = ['POST'])
def add_drink():
    try:
     drink = Drink(name = request.json['name'], description = request.json['description'])
     db.session.add(drink)
     db.session.commit()
     return {'id': drink.id}
    except Exception:
     return {'error': "You cannot add a drink that already exists or deleted. Also make sure you didn't make a syntax mistake."}

#Delete Drink (Soft Delete)
@app.route("/drinks/<id>", methods = ['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None or drink.isDeleted == True:
        return {"error": "the drink you wanted to delete is not found"}
    else:
        drink.isDeleted = True
        db.session.commit()
        return {"message": "The drink succesfully deleted"}


if __name__ == "__main__":
   app.run(debug=True)