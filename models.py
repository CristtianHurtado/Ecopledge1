from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecopledge.db'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Event {self.title}>"

class RecyclingPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    materials_accepted = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<RecyclingPoint {self.name}>'

@app.route('/api/recycling-points', methods=['GET'])
def get_recycling_points():
    points = RecyclingPoint.query.all()
    return jsonify([{
        'id': point.id,
        'name': point.name,
        'address': point.address,
        'latitude': point.latitude,
        'longitude': point.longitude,
        'materials_accepted': point.materials_accepted
    } for point in points])

@app.route('/api/recycling-points', methods=['POST'])
def add_recycling_point():
    data = request.get_json()
    new_point = RecyclingPoint(
        name=data['name'],
        address=data['address'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        materials_accepted=data['materials_accepted']
    )
    db.session.add(new_point)
    db.session.commit()
    return jsonify({'message': 'Recycling point added successfully'}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
