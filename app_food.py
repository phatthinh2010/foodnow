from flask import Flask, request, jsonify, abort, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodnow.sqlite3'
db = SQLAlchemy(app)



class Food(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(511))
    image = db.Column(db.String(255))
    price = db.Column(db.Float(asdecimal = True))
    resId = db.Column(db.Integer)
    
    def __init__(self, name, image, price, resId):
        self.name = name
        self.image = image
        self.price = price
        self.resId = resId

class Restaurant(db.Model): 
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(511))
    logo = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    address = db.Column(db.String(1023))
    openHours = db.Column(db.String(255))
    lat = db.Column(db.String(127))
    lng = db.Column(db.String(127)) 

    def __init__(self, name, logo, cover, address, openHours, lat, lng):
        self.name = name 
        self.logo = logo 
        self.cover = cover 
        self.address = address 
        self.openHours = openHours
        self.lat = lat 
        self.lng = lng 

@app.route('/restaurants/<string:latLng>', methods = ['GET'])
def get_restaurants(latLng): 
    res = Restaurant.query.all()
    response = []
    for r in res: 
        item = {
            'id': r.id, 
            'name': r.name,
            'logo': url_for('static', filename=r.logo), 
            'cover': url_for('static', filename=r.cover),
            'address': r.address, 
            'openHours': r.openHours, 
            'lat': r.lat,
            'lng': r.lng
        }
        response.append(item)
    return jsonify({
        'restaurants': response
    })

# @app.route('/restaurants', methods = ['GET'])
# def get_restaurants(): 
#     res = Restaurant.query.all()
#     response = []
#     for r in res: 
#         item = {
#             'id': r.id, 
#             'name': r.name,
#             'logo': url_for('static', filename=r.logo), 
#             'cover': url_for('static', filename=r.cover),
#             'address': r.address, 
#             'openHours': r.openHours, 
#             'lat': r.lat,
#             'lng': r.lng
#         }
#         response.append(item)
#     return jsonify({
#         'restaurants': response
#     })

@app.route('/foods/<int:resId>', methods = ['GET'])
def get_foods(resId):
    if request.method == 'GET': 
        foods = Food.query.filter_by(resId = resId)
        response = []
        if not foods: 
            return jsonify({
                'foods': response
            })
        else:
            for f in foods: 
                item = {
                    'id': f.id, 
                    'name': f.name, 
                    'price': str(f.price), 
                    'resId': f.resId, 
                    'image': url_for('static', filename=f.image)
                }
                response.append(item)
            return jsonify({
                'foods': response
            })
    else: 
        abort(404)

@app.route('/food', methods = ['POST'])
def add_food(): 
    if request.method == 'POST':
        name = request.form.get('name')
        image = request.form.get('image')
        price = request.form.get('price')
        resId = request.form.get('resId')
        food = Food(name, image, price, resId)
        db.session.add(food)
        db.session.commit()
        return jsonify({
            'id': food.id,
            'name': food.name, 
            'price': str(food.price), 
            'resId': food.resId, 
            'image': url_for('static', filename=food.image)
        })


@app.route('/restaurant', methods = ['POST'])
def add_res(): 
    if request.method == 'POST':
        name = request.form.get('name')
        logo = request.form.get('logo')
        cover = request.form.get('cover')
        address = request.form.get('address')
        openHours = request.form.get('openHours')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        res = Restaurant(name, logo, cover, address, openHours, lat, lng)
        db.session.add(res)
        db.session.commit()
        return jsonify({
            'id': res.id,
            'name': res.name, 
            'logo': url_for('static', filename=res.logo), 
            'cover': url_for('static', filename=res.cover), 
            'address': res.address, 
            'openHours': res.openHours, 
            'lat': res.lat, 
            'lng': res.lng
        })


if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
