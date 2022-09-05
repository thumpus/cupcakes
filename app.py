"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret-collect"

connect_db(app)

def serialize_cupcake(cupcake):
    """serialize a SQLAlchemy object into a dictionary"""
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }

@app.route("/")
def show_home():
    return render_template("home.html")

@app.route("/api/cupcakes")
def get_cupcakes():
    """returns JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]}"""
    all_cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in all_cupcakes]
    return jsonify (cupcakes=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def cupcake_info(cupcake_id):
    """return JSON {'cupcake': {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)
    return jsonify (cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """creates a cupcake, respond with JSON {'cupcake': {id, flavor, size, rating, image}} """
    
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)
    
    return (jsonify(cupcake = serialized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]
    db.session.commit()
    serialized = serialize_cupcake(cupcake)
    return (jsonify(cupcake=serialized))

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({"message": "deleted!",})