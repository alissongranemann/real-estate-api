from app import db

from collections import OrderedDict

class DictSerializable(object):
    def to_json(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

class Address(db.Model, DictSerializable):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String())
    neighbourhood = db.Column(db.String())
    cep = db.Column(db.String(9))

    property = db.relationship("Property", uselist=False, back_populates="address")

    def __repr__(self):
        return f"<id {self.id}>"


class Property(db.Model, DictSerializable):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    address = db.relationship("Address", back_populates="property", cascade="all, delete, delete-orphan", single_parent=True)

    def __repr__(self):
        return f"<id {self.id}>"
