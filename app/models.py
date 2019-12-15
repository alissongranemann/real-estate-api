from app import db
from geoalchemy2 import Geometry
from sqlalchemy.sql import func


class TimeMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class State(db.Model):
    __tablename__ = "state"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    short_name = db.Column(db.String(2), nullable=False)

    cities = db.relationship("City", back_populates="state")

    def __repr__(self):
        return f"<id: {self.id}, state: {self.short_name}>"


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), nullable=False)

    state = db.relationship("State", back_populates="cities", cascade="save-update")
    neighbourhoods = db.relationship("Neighbourhood", back_populates="city")

    def __repr__(self):
        return f"<id: {self.id}, city: {self.name}>"


class Neighbourhood(db.Model):
    __tablename__ = "neighbourhood"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"), nullable=False)

    city = db.relationship(
        "City", back_populates="neighbourhoods", cascade="save-update"
    )
    streets = db.relationship("Street", back_populates="neighbourhood")

    def __repr__(self):
        return f"<id: {self.id}, neighbourhood: {self.name}>"


class Street(db.Model):
    __tablename__ = "street"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    postal_code = db.Column(db.String(9), nullable=False, unique=True)
    neighbourhood_id = db.Column(
        db.Integer, db.ForeignKey("neighbourhood.id"), nullable=False
    )

    neighbourhood = db.relationship(
        "Neighbourhood", back_populates="streets", cascade="save-update"
    )
    locations = db.relationship("Location", back_populates="street")

    def __repr__(self):
        return f"<id: {self.id}, street: {self.name}>"


class Location(db.Model, TimeMixin):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    geom = db.Column(Geometry("POINT"), nullable=False)
    places_id = db.Column(db.String(), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey("street.id"), nullable=False)

    street = db.relationship(
        "Street", back_populates="locations", cascade="save-update"
    )
    properties = db.relationship("Property", back_populates="location")

    def __repr__(self):
        return f"<id: {self.id}, postal_code: {self.postal_code}>"


class Property(db.Model, TimeMixin):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    url = db.Column(db.String(), nullable=False)

    location = db.relationship(
        "Location", back_populates="properties", cascade="all, delete"
    )

    # __table_args__ = (db.Index("area_price_index", area, price),)

    def __repr__(self):
        return f"<id: {self.id}, location: {self.location}>"
