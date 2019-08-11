from app import db


class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String())
    neighbourhood = db.Column(db.String())
    cep = db.Column(db.String(9))

    property = db.relationship("Property", uselist=False, back_populates="address")

    def __repr__(self):
        return f"<id {self.id}>"


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    address = db.relationship("Address", back_populates="property")

    def __repr__(self):
        return f"<id {self.id}>"
