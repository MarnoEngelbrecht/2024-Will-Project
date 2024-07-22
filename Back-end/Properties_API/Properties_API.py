from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS

class User:
    def __init__(self, RefUser, Username, Email, Password):
        self.RefUser = RefUser
        self.Username = Username
        self.Email = Email
        self.Password = Password

    def to_dict(self):
        return {
            'RefUser': self.RefUser,
            'Username': self.Username,
            'Email': self.Email,
            'Password': self.Password
        }

class Property:
    def __init__(self, RefProperty, Title, Thumbnail, Address, NrBeds, NrBathrooms, HasPool, ParkingSpots, HasWifi, HasGarden, PropertySize):
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
            'PropertySize': self.PropertySize
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

def parsePropertyJSON(data):
    return Property(None, data['Title'], data['Thumbnail'], data['Address'], data['NrBeds'], data['NrBathrooms'], data['HasPool'], data['ParkingSpots'], data['HasWifi'], data['HasGarden'], data['PropertySize'])
        


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Configure database connection
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:/Users/Marno/Desktop/School/Will Project/2024-Will-Project/Back-end/Property Listings.accdb;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
# Users 
# @app.route('/items', methods=['GET'])
# def get_items():
#     cursor.execute("SELECT * FROM items")
#     rows = cursor.fetchall()
#     items = []
#     for row in rows:
#         items.append(User(row.RefUser, row.Username, row.Email, row.Password))
#     return jsonify(items)

@app.route('/user/<int:RefUser>', methods=['GET'])
def get_user(RefUser):
    cursor.execute("SELECT * FROM users WHERE RefUser=?", RefUser)
    row = cursor.fetchone()
    if row:
        return jsonify(User(row.RefUser, row.Username, row.Email, row.Password).to_dict())
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/insert', methods=['POST'])
def create_user():
    data = request.get_json()
    cursor.execute("INSERT INTO users (Username, Email, Password) VALUES (?, ?, ?)", data['Username'], data['Email'], data['Password'])
    conn.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/user/update/<int:RefUser>', methods=['PUT'])
def update_user(RefUser):
    data = request.get_json()
    cursor.execute("UPDATE users SET Username=?, Email=?, Password=? WHERE RefUser=?", data['Username'], data['Email'], data['Password'], RefUser)
    conn.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/user/delete/<int:RefUser>', methods=['DELETE'])
def delete_user(RefUser):
    cursor.execute("DELETE FROM users WHERE RefUser=?", RefUser)
    conn.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Properties

@app.route('/properties/getcollection', methods=['GET'])
def get_property_collection():
    cursor.execute("SELECT * FROM properties")
    rows = cursor.fetchall()
    items = []
    for row in rows:
        items.append(Property(row.RefProperty, row.Title, row.Thumbnail, row.Address, row.NrBeds, row.NrBathrooms, row.HasPool, row.ParkingSpots, row.HasWifi, row.HasGarden, row.PropertySize).to_dict())
    return jsonify(items)

@app.route('/properties/<int:RefProperty>', methods=['GET'])
def get_property(RefProperty):
    cursor.execute("SELECT * FROM properties WHERE RefProperty=?", RefProperty)
    row = cursor.fetchone()
    if row:
        return jsonify(Property(row.RefProperty, row.Title, row.Thumbnail, row.Address, row.NrBeds, row.NrBathrooms, row.HasPool, row.ParkingSpots, row.HasWifi, row.HasGarden, row.PropertySize).to_dict())
    return jsonify({'error': 'Property not found'}), 404

@app.route('/properties/insert', methods=['POST'])
def create_property():
    data = request.get_json()
    property = parsePropertyJSON(data)
    cursor.execute("INSERT INTO properties (Title, Thumbnail, Address, NrBeds, NrBathrooms, HasPool, ParkingSpots, HasWifi, HasGarden, PropertySize) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", property.Title, property.Thumbnail, property.Address, property.NrBeds, property.NrBathrooms, property.HasPool, property.ParkingSpots, property.HasWifi, property.HasGarden, property.PropertySize)
    conn.commit()
    return jsonify({'message': 'Property created successfully'}), 201

@app.route('/properties/update/<int:RefProperty>', methods=['PUT'])
def update_property(RefProperty):
    data = request.get_json()
    property = parsePropertyJSON(data)
    cursor.execute("UPDATE properties SET Title=?, Thumbnail=?, Address=?, NrBeds=?, NrBathrooms=?, HasPool=?, ParkingSpots=?, HasWifi=?, HasGarden=?, PropertySize=? WHERE RefProperty=?", property.Title, property.Thumbnail, property.Address, property.NrBeds, property.NrBathrooms, property.HasPool, property.ParkingSpots, property.HasWifi, property.HasGarden, property.PropertySize, RefProperty)
    conn.commit()
    return jsonify({'message': 'Property updated successfully'}), 200

@app.route('/properties/delete/<int:RefProperty>', methods=['DELETE'])
def delete_property(RefProperty):
    cursor.execute("DELETE FROM properties WHERE RefProperty=?", RefProperty)
    conn.commit()
    return jsonify({'message': 'Property deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
