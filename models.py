from app import db

#alleen nodig voor json in column    db.Column(JSON)
from sqlalchemy.dialects.postgresql import JSON


class Products(db.Model):
    __tablename__='products'

    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    price= db.Column(db.Integer)
    status = db.Column(db.String(20))
    created_at = db.Column(db.String(30))

    #runs when we created a new one
    def __init__(self,merchant_id, name, price, status, created_at):
        self.merchant_id=merchant_id
        self.name=name
        self.price=price
        self.status=status
        self.created_at=created_at

    #represents object when we query for it
    def __repr__(self):
        return '<id {}>'.format(self.id)

