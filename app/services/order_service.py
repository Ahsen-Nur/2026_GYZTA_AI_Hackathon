from app.database import SessionLocal
from app.models import Order

def get_all_orders():

    db = SessionLocal()

    return db.query(Order).all()