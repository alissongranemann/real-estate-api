from app import db

from geoalchemy2 import Geometry


class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    initials = db.Column(db.String(2), nullable=False)

    locations = db.relationship("Location", back_populates="state")

    def __repr__(self):
        return f"<id {self.id}>"


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    postal_code = db.Column(db.String(9), nullable=False)
    street = db.Column(db.String(), nullable=False)
    neighbourhood = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    places_id = db.Column(db.String(), nullable=False)
    geom = db.Column(Geometry("POINT"), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"), nullable=False)

    state = db.relationship("State", back_populates="locations", cascade="save-update")
    properties = db.relationship("Property", back_populates="location")

    def __repr__(self):
        return f"<id {self.id}>"


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)

    location = db.relationship(
        "Location", back_populates="properties", cascade="all, delete"
    )

    def __repr__(self):
        return f"<id {self.id}>"
