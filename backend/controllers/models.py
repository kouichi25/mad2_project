from datetime import datetime
from controllers.database import db
from flask_security import UserMixin, RoleMixin


 
# USER + ROLE MODELS
 

class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)   # 'admin', 'user'
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    
    # Flask-Security required fields
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    # Relationship
    roles = db.relationship("Role", secondary="user_roles", backref="users")

    # User can have multiple reservations
    reservations = db.relationship("Reservation", backref="user", lazy=True)


class UserRoles(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))



 
# PARKING LOT MODELS
 

class ParkingLot(db.Model):
    __tablename__ = "parking_lots"

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)

    number_of_spots = db.Column(db.Integer, nullable=False)

    # Relationship to spots
    spots = db.relationship("ParkingSpot", backref="lot", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ParkingLot {self.prime_location_name}>"


 
# INDIVIDUAL PARKING SPOTS
 

class ParkingSpot(db.Model):
    __tablename__ = "parking_spots"

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lots.id"), nullable=False)

    status = db.Column(db.String(1), nullable=False, default="A")  
    # A = available, O = occupied

    # Relationship: one spot -> many reservations (historical)
    reservations = db.relationship("Reservation", backref="spot", lazy=True)

    def __repr__(self):
        return f"<Spot {self.id} in Lot {self.lot_id}>"


 
# RESERVATION MODEL
 

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)

    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spots.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)

    parking_cost = db.Column(db.Float, default=0)

    def __repr__(self):
        return f"<Reservation spot={self.spot_id} user={self.user_id}>"

