from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from opencage.geocoder import OpenCageGeocode
from models import db, Event
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar sesiones
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = []
    for event in events:
        events_list.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d %H:%M:%S'),
            'location': event.location
        })
    return jsonify(events_list), 200

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    date_str = data.get('date')
    location = data.get('location')

    if not title or not description or not date_str or not location:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    new_event = Event(title=title, description=description, date=date, location=location)
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Evento creado exitosamente'}), 201

@app.route('/api/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Evento eliminado exitosamente'}), 200

geocoder = OpenCageGeocode('cce8b143f92849e4941c386955721814')

class RecyclingPoint(db.Model):
    __tablename__ = 'recycling_point'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    materials_accepted = db.Column(db.String(200), nullable=False)

@app.route('/init-db')
def init_db():
    db.create_all()
    return jsonify({"message": "Base de datos inicializada"}), 200

@app.route('/api/recycling-points', methods=['POST'])
def add_recycling_point():
    data = request.get_json()
    address = data['address']
    result = geocoder.geocode(address)
    if result and len(result) > 0:
        latitude = result[0]['geometry']['lat']
        longitude = result[0]['geometry']['lng']
        new_point = RecyclingPoint(
            name=data['name'],
            address=address,
            latitude=latitude,
            longitude=longitude,
            materials_accepted=data['materials_accepted']
        )
        db.session.add(new_point)
        db.session.commit()
        return jsonify({"message": "Punto de reciclaje agregado exitosamente!"}), 201
    else:
        print(f"Geocoding result: {result}")
        return jsonify({"message": "No se encontraron coordenadas para la dirección proporcionada. Por favor, asegúrate de que la dirección sea correcta y específica."}), 400

@app.route('/api/recycling-points', methods=['GET'])
def get_recycling_points():
    points = RecyclingPoint.query.all()
    points_list = [
        {
            "name": point.name,
            "address": point.address,
            "latitude": point.latitude,
            "longitude": point.longitude,
            "materials_accepted": point.materials_accepted
        }
    for point in points]
    return jsonify(points_list), 200

users = {
    'testuser': 'testpass'  # Usuario de ejemplo
}

# Ruta de registro
@app.route('/api/auth/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')

    if not email or not password or not name:
        return jsonify({"message": "Todos los campos son obligatorios"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "El correo electrónico ya está registrado"}), 409

    new_user = User(email=email, password=password, name=name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201


# Ruta de inicio de sesión
@app.route('/api/auth/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email or not password:
        return jsonify({"message": "Todos los campos son obligatorios"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        session['user_id'] = user.id
        session['user_name'] = user.name
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401

# Ruta para la página de usuario
@app.route('/usuario')
def usuario():
    if 'user_name' in session:
        return render_template('usuario.html', user_name=session['user_name'])
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)