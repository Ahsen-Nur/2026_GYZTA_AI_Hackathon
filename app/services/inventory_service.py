from app.database import SessionLocal
from app.models import Inventory

def get_inventory():

    db = SessionLocal()

    return db.query(Inventory).all()