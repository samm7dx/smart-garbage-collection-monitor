import datetime
import random
import os
import sys

# Ensure the backend directory is in sys.path so 'app' can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models import GarbageBin, CollectionRecord, Complaint, BinStatus, CollectionStatus, ComplaintStatus
from app.ml import train_model
from app.status_utils import utcnow_naive

def seed_db():
    print("Training ML model...")
    train_model.train()

    print("Recreating database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    areas = ["Koramangala", "Indiranagar", "Jayanagar", "Whitefield", "Malleswaram"]
    base_coords = {
        "Koramangala": (12.9352, 77.6245),
        "Indiranagar": (12.9784, 77.6408),
        "Jayanagar": (12.9299, 77.5826),
        "Whitefield": (12.9698, 77.7499),
        "Malleswaram": (13.0031, 77.5643)
    }

    # Bins
    bins_data = []
    for i in range(1, 21):
        area = random.choice(areas)
        base_lat, base_lon = base_coords[area]
        lat = base_lat + random.uniform(-0.01, 0.01)
        lon = base_lon + random.uniform(-0.01, 0.01)
        
        if area == "Whitefield":
            fill = random.uniform(70, 100)
            status = BinStatus.OVERFLOW_RISK
        else:
            fill = random.uniform(10, 60)
            status = BinStatus.NORMAL

        b = GarbageBin(
            name=f"Bin {area}-{i}",
            area=area,
            latitude=lat,
            longitude=lon,
            capacity=100.0,
            current_fill_percentage=fill,
            collection_frequency_days=random.choice([1, 2]),
            scheduled_collection_time="09:00",
            status=status
        )
        bins_data.append(b)
        db.add(b)
    
    db.commit()

    print("Seeding collections...")
    bins = db.query(GarbageBin).all()
    now = utcnow_naive()

    for b in bins:
        for j in range(5, 0, -1):
            sch_date = now - datetime.timedelta(days=j*b.collection_frequency_days)
            
            if b.area == "Whitefield":
                act_date = sch_date
                act_time = "12:30" 
                delay = 210
                c_status = CollectionStatus.DELAYED
            elif b.area == "Jayanagar" and j % 2 == 0:
                act_date = None
                act_time = None
                delay = 0
                c_status = CollectionStatus.MISSED
            else:
                act_date = sch_date
                act_time = "09:15"
                delay = 15
                c_status = CollectionStatus.ON_TIME

            c = CollectionRecord(
                bin_id=b.id,
                scheduled_date=sch_date,
                scheduled_time="09:00",
                actual_collection_date=act_date,
                actual_collection_time=act_time,
                delay_minutes=delay,
                status=c_status
            )
            db.add(c)
    
    db.commit()

    print("Seeding complaints...")
    for b in bins:
        if b.area in ["Whitefield", "Jayanagar"]:
            comp = Complaint(
                bin_id=b.id,
                area=b.area,
                description=f"Garbage is overflowing in {b.area}. Please collect soon.",
                status=ComplaintStatus.OPEN
            )
            db.add(comp)
    
    db.commit()
    db.close()
    print("Seeding completed successfully.")

if __name__ == "__main__":
    seed_db()
