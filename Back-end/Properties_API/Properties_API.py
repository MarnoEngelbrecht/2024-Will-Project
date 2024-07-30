from flask import Flask, request, jsonify, make_response, send_file
import pyodbc
from flask_cors import CORS
import jwt
import datetime
import bcrypt
from functools import wraps
import io
import base64

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
    def __init__(self, RefProperty, Title, Address, NrBeds, NrBathrooms, ParkingSpots, RefUser):
        self.RefProperty = RefProperty
        self.Title = Title
        self.Address = Address
        self.NrBeds = NrBeds
        self.NrBathrooms = NrBathrooms
        self.ParkingSpots = ParkingSpots
        self.RefUser = RefUser
    
    def to_dict(self):
        return {
            'RefProperty': self.RefProperty,
            'Title': self.Title,
            'Address': self.Address,
            'NrBeds': self.NrBeds,
            'NrBathrooms': self.NrBathrooms,
            'ParkingSpots': self.ParkingSpots,
            'RefUser' : self.RefUser
        }
    
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

def getUserByToken():
    token = request.cookies.get('properties_token')
    if not token:
        return jsonify({'message': 'Token is missing'}), 403
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data.get('RefUser')
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 403

def parsePropertyJSON(data):
    return Property(None, data['Title'], data['Address'], data['NrBeds'], data['NrBathrooms'], data['ParkingSpots'], data['RefUser'])

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
        resp = make_response(jsonify({'message': 'Login successful', 'User' : user['RefUser']}))
        resp.set_cookie('properties_token', token, httponly=True)
        return resp
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/user/<int:RefUser>', methods=['GET'])
def get_user(RefUser):
    try:
        cursor.execute("SELECT * FROM users WHERE RefUser=?", (RefUser,))
        row = cursor.fetchone()
        if row:
            return jsonify(User(row.RefUser, row.Username, row.Email, None, None).to_dict())
        return jsonify({'error': 'User not found'}), 404
    except pyodbc.Error as e:
        return jsonify({'error': str(e)}), 500

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
        items.append(Property(row.RefProperty, row.Title, row.Address, row.NrBeds, row.NrBathrooms, row.ParkingSpots, row.RefUser).to_dict())
    return jsonify(items)

@app.route('/properties/<int:RefProperty>', methods=['GET'])
def get_property(RefProperty):
    cursor.execute("SELECT * FROM properties WHERE RefProperty=?", RefProperty)
    row = cursor.fetchone()
    if row:
        return jsonify(Property(row.RefProperty, row.Title, row.Address, row.NrBeds, row.NrBathrooms, row.ParkingSpots, row.RefUser).to_dict())
    return jsonify({'error': 'Property not found'}), 404

@app.route('/properties/insert', methods=['POST'])
@token_required
def create_property():
    data = request.get_json()
    if currentUser.RefUser == None:
        currentUser.RefUser = getUserByToken()
    property = parsePropertyJSON(data)
    #Image does not want to get uploaded 
    # image_data = data['Thumbnail']
    cursor.execute("INSERT INTO properties (Title, Thumbnail, Address, NrBeds, NrBathrooms, ParkingSpots, RefUser) VALUES (?, ?, ?, ?, ?, ?, ?)", property.Title, None, property.Address, property.NrBeds, property.NrBathrooms, property.ParkingSpots, currentUser.RefUser)
    conn.commit()
    return jsonify({'message': 'Property created successfully'}), 201


# def insert_property():
#     title = request.form.get('Title')
#     address = request.form.get('Address')
#     nr_beds = request.form.get('NrBeds')
#     nr_bathrooms = request.form.get('NrBathrooms')
#     parking_spots = request.form.get('ParkingSpots')
#     thumbnail = request.files.get('Thumbnail')

#     # if not title or not thumbnail:
#     #     return jsonify({'error': 'Title and Thumbnail are required'}), 400

#     thumbnail_bytes = thumbnail.read()

#     c = conn.cursor()
#     c.execute("INSERT INTO properties (Title, Address, NrBeds, NrBathrooms, ParkingSpots, Thumbnail, RefUser) VALUES (?, ?, ?, ?, ?, ?, ?)",
#               (title, address, nr_beds, nr_bathrooms, parking_spots, thumbnail_bytes, currentUser.RefUser))
#     conn.commit()

#     return jsonify({'success': 'Property inserted successfully'}), 200


@app.route('/properties/update/<int:RefProperty>', methods=['PUT'])
@token_required
def update_property(RefProperty):
    data = request.get_json()
    property = parsePropertyJSON(data)
    cursor.execute("UPDATE properties SET Title=?, Thumbnail=?, Address=?, NrBeds=?, NrBathrooms=?, ParkingSpots=? WHERE RefProperty=?", property.Title, property.Thumbnail, property.Address, property.NrBeds, property.NrBathrooms, property.ParkingSpots, RefProperty)
    conn.commit()
    return jsonify({'message': 'Property updated successfully'}), 200

@app.route('/properties/delete/<int:RefProperty>', methods=['DELETE'])
@token_required
def delete_property(RefProperty):
    cursor.execute("DELETE FROM properties WHERE RefProperty=?", RefProperty)
    conn.commit()
    return jsonify({'message': 'Property deleted successfully'}), 200

@app.route('/user/properties/<int:RefUser>', methods=['GET'])
@token_required
def get_user_property(RefUser):
    cursor.execute("SELECT * FROM properties where RefUser = ?", RefUser)
    rows = cursor.fetchall()
    items = []
    if rows:
        for row in rows:
            items.append(Property(row.RefProperty, row.Title, row.Address, row.NrBeds, row.NrBathrooms, row.ParkingSpots, row.RefUser).to_dict())
        return jsonify(items)
    return jsonify({'error': 'No properties found'}), 404

@app.route('/properties/image/<int:RefProperty>', methods=['GET'])
def get_image(RefProperty):
    cursor.execute("SELECT thumbnail FROM properties WHERE RefProperty=?", (RefProperty,))
    row = cursor.fetchone()
    if row:
        image_bytes = row[0]
        return jsonify({'image','cant load'}), 201
        # b64_image = base64.b64encode(image_bytes).decode('utf-8')
        # return jsonify({'image': f'data:image/png;base64,{b64_image}'})
        # return send_file(
        #     io.BytesIO(image_bytes),
        #     mimetype='image/jpeg',
        #     as_attachment=False,
        #     download_name='image.jpg'
        # )
    return jsonify({'error': 'Image not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)

