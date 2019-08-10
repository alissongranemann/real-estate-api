from app import db


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    city = db.Column(db.String())
    neighbourhood = db.Column(db.String())
    cep = db.Column(db.String(9))

    def __repr__(self):
        return f"<id {self.id}>"
