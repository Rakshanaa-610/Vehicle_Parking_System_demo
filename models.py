from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String,unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    phoneno = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String, nullable=False, default='user')
    
    userid = db.relationship("Reserved",backref="user",cascade='all, delete-orphan')

class Parking_Lot(db.Model):
    __tablename__ = "parking_lot"
    
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    priceperhr = db.Column(db.Integer, nullable=False)
    maximum_spots = db.Column(db.Integer, nullable=False)

    lotid = db.relationship("Parking_Spot", backref="lot",cascade='all, delete-orphan')

class Parking_Spot(db.Model):
    __tablename__ = "parking_spot"
    id = db.Column(db.Integer, primary_key=True)
    lotid = db.Column(db.Integer, db.ForeignKey("parking_lot.id"), nullable=False)
    status = db.Column(db.String, nullable=False)

    spotid = db.relationship("Reserved", backref="spot",cascade='all, delete-orphan')

class Reserved(db.Model):
    __tablename__ = "reserved"

    id = db.Column(db.Integer, primary_key=True)
    spotid = db.Column(db.Integer, db.ForeignKey("parking_spot.id"), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    vehicle_no = db.Column(db.String, nullable=False, unique=True)
    parking_timestamp = db.Column(db.DateTime,server_default=db.func.now())
    leaving_timestamp = db.Column(db.DateTime,server_default=db.func.now())
    parking_cost = db.Column(db.Integer)
 
