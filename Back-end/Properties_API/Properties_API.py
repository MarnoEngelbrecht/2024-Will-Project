from flask import Flask, request, jsonify, make_response
import pyodbc
from flask_cors import CORS
import jwt
import datetime
import bcrypt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '&2b6X8V!hHR*EyipHico'
CORS(app, supports_credentials=True, resources={r"/*": {
    "origins": ["http://127.0.0.1:5500"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})


class User:
    def __init__(self, RefUser, Username, Email, Password, Salt):
        self.RefUser = RefUser
        self.Username = Username
        self.Email = Email
        self.Password = Password
        self.Salt = Salt

    def to_dict(self):
        return {
            'RefUser': self.RefUser,
            'Username': self.Username,
            'Email': self.Email,
            'Password': self.Password,
            'Salt' : self.Salt
        }

currentUser = User(None, None, None, None, None)

class Property:
    def __init__(self, RefProperty, Title, Thumbnail, Address, NrBeds, NrBathrooms, HasPool, ParkingSpots, HasWifi, HasGarden, PropertySize, RefUser):
        self.RefProperty = RefProperty
        self.Title = Title
        self.Thumbnail = Thumbnail
        self.Address = Address
        self.NrBeds = NrBeds
        self.NrBathrooms = NrBathrooms
        self.HasPool = HasPool
        self.ParkingSpots = ParkingSpots
        self.HasWifi = HasWifi
        self.HasGarden = HasGarden
        self.PropertySize = PropertySize
        self.RefUser = RefUser
    
    def to_dict(self):
        return {
            'RefProperty': self.RefProperty,
            'Title': self.Title,
            'Thumbnail': self.Thumbnail,
            'Address': self.Address,
            'NrBeds': self.NrBeds,
            'NrBathrooms': self.NrBathrooms,
            'HasPool': self.HasPool,
            'ParkingSpots': self.ParkingSpots,
            'HasWifi': self.HasWifi,
            'HasGarden': self.HasGarden,
            'PropertySize': self.PropertySize,
            'RefUser' : self.RefUser
        }

    # def parseJSON(self, data):
    #     self.RefProperty = data['RefProperty']
    #     self.Title = data['Title']
    #     self.Thumbnail = data['Thumbnail']
    #     self.Address = data['Address']
    #     self.NrBeds = data['NrBeds']
    #     self.NrBathrooms = data['NrBathrooms']
    #     self.HasPool = data['HasPool']
    #     self.ParkingSpots = data['ParkingSpots']
    #     self.HasWifi = data['HasWifi']
    #     self.HasGarden = data['HasGarden']
    #     self.PropertySize = data['PropertySize']
    #     return self

#Login
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return salt, hashed_password

def generate_jwt(RefUser, username, email):
    token = jwt.encode({
        'RefUser': RefUser,
        'Username': username,
        'Email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'])
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('properties_token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if not user_exists(data.get("RefUser")):
                return jsonify({'message': 'User not found'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 403

        return f(*args, **kwargs)
    return decorated

def parsePropertyJSON(data):
    return Property(None, data['Title'], data['Thumbnail'], data['Address'], data['NrBeds'], data['NrBathrooms'], data['HasPool'], data['ParkingSpots'], data['HasWifi'], data['HasGarden'], data['PropertySize'], data['RefUser'])

# Configure database connection
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:/Users/Marno/Desktop/School/Will Project/Property Listings.accdb;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
# Users 

@app.route('/user/validate', methods=['GET'])
@token_required
def validate():
    return jsonify({'success' : True}), 200

@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data['Password']
    exist, status = get_user_email(data['Email'])
    if status == 404:
        return jsonify({'error': 'User was not found'}), 404
    user = exist.get_json()
    u_password = user['Password']
    byte_password = password.encode('utf-8')
    u_byte_password = u_password.encode('utf-8')
    # if bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')) == exist['Password']:
    if bcrypt.checkpw(byte_password, u_byte_password):
        token = generate_jwt(user['RefUser'], user['Username'], user['Email'])
        resp = make_response(jsonify({'message': 'Login successful'}))
        resp.set_cookie('properties_token', token, httponly=True)
        currentUser = User(user['RefUser'], user['Username'], user['Email'], None, None)
        return resp
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/user/<int:RefUser>', methods=['GET'])
@token_required
def get_user(RefUser):
    cursor.execute("SELECT * FROM users WHERE RefUser=?", RefUser)
    row = cursor.fetchone()
    if row:
        return jsonify(User(row.RefUser, row.Username, row.Email, None, None).to_dict())
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/GetModelByEmail', methods=['GET'])
@token_required
def get_model_email():
    data = request.get_json()
    return get_user_email(data['Email'])

def get_user_email(email):
    cursor.execute("SELECT * FROM users WHERE email = ?", email)
    row = cursor.fetchone()
    if row:
        return jsonify(User(row.RefUser, row.Username, row.Email, row.Password.decode('utf-8'), row.Salt.decode('utf-8')).to_dict()), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/register', methods=['POST'])
def create_user():
    data = request.get_json()
    exist, status = get_user_email(data['Email'])
    if status == 200:
        return jsonify({'error': 'User already exists'}), 406
    salt, hashed_password = hash_password(data['Password'])
    cursor.execute("INSERT INTO users (Username, Email, Password, Salt) VALUES (?, ?, ?, ?)", data['Username'], data['Email'], hashed_password, salt)
    conn.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/user/update/<int:RefUser>', methods=['PUT'])
@token_required
def update_user(RefUser):
    data = request.get_json()
    cursor.execute("UPDATE users SET Username=?, Email=? WHERE RefUser=?", data['Username'], data['Email'], RefUser)
    conn.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/user/delete/<int:RefUser>', methods=['DELETE'])
@token_required
def delete_user(RefUser):
    cursor.execute("DELETE FROM users WHERE RefUser=?", RefUser)
    conn.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

def get_users_collection():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    items = []
    for row in rows:
        items.append(User(row.RefUser, row.Username, row.Email, None, None).to_dict())
    return jsonify(items)

def user_exists(RefUser):
    cursor.execute('SELECT * FROM users WHERE RefUser = ?', RefUser)
    rows = cursor.fetchall()
    if len(rows) >= 1:
        return True
    return False

# Properties

@app.route('/properties/getcollection', methods=['GET'])
def get_property_collection():
    cursor.execute("SELECT * FROM properties")
    rows = cursor.fetchall()
    items = []
    for row in rows:
        items.append(Property(row.RefProperty, row.Title, row.Thumbnail, row.Address, row.NrBeds, row.NrBathrooms, row.HasPool, row.ParkingSpots, row.HasWifi, row.HasGarden, row.PropertySize, row.RefUser).to_dict())
    return jsonify(items)

@app.route('/properties/<int:RefProperty>', methods=['GET'])
def get_property(RefProperty):
    cursor.execute("SELECT * FROM properties WHERE RefProperty=?", RefProperty)
    row = cursor.fetchone()
    if row:
        return jsonify(Property(row.RefProperty, row.Title, row.Thumbnail, row.Address, row.NrBeds, row.NrBathrooms, row.HasPool, row.ParkingSpots, row.HasWifi, row.HasGarden, row.PropertySize, row.RefUser).to_dict())
    return jsonify({'error': 'Property not found'}), 404

@app.route('/properties/insert', methods=['POST'])
@token_required
def create_property():
    data = request.get_json()
    property = parsePropertyJSON(data)
    cursor.execute("INSERT INTO properties (Title, Thumbnail, Address, NrBeds, NrBathrooms, HasPool, ParkingSpots, HasWifi, HasGarden, PropertySize, RefUser) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", property.Title, property.Thumbnail, property.Address, property.NrBeds, property.NrBathrooms, property.HasPool, property.ParkingSpots, property.HasWifi, property.HasGarden, property.PropertySize, currentUser.RefUser)
    conn.commit()
    return jsonify({'message': 'Property created successfully'}), 201

@app.route('/properties/update/<int:RefProperty>', methods=['PUT'])
@token_required
def update_property(RefProperty):
    data = request.get_json()
    property = parsePropertyJSON(data)
    cursor.execute("UPDATE properties SET Title=?, Thumbnail=?, Address=?, NrBeds=?, NrBathrooms=?, HasPool=?, ParkingSpots=?, HasWifi=?, HasGarden=?, PropertySize=? WHERE RefProperty=?", property.Title, property.Thumbnail, property.Address, property.NrBeds, property.NrBathrooms, property.HasPool, property.ParkingSpots, property.HasWifi, property.HasGarden, property.PropertySize, RefProperty)
    conn.commit()
    return jsonify({'message': 'Property updated successfully'}), 200

@app.route('/properties/delete/<int:RefProperty>', methods=['DELETE'])
@token_required
def delete_property(RefProperty):
    cursor.execute("DELETE FROM properties WHERE RefProperty=?", RefProperty)
    conn.commit()
    return jsonify({'message': 'Property deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
