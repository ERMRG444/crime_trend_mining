import os
import random
from datetime import datetime, timedelta
from faker import Faker
from app import app, db, Incident

fake = Faker('en_IN')

# Define Indian Bounding Box and Major Cities roughly
# Let's focus on a few hubs to make the heatmap look good
CITIES = [
    {"name": "Delhi", "lat": 28.6139, "lng": 77.2090, "spread": 0.2},
    {"name": "Mumbai", "lat": 19.0760, "lng": 72.8777, "spread": 0.15},
    {"name": "Bangalore", "lat": 12.9716, "lng": 77.5946, "spread": 0.1},
    {"name": "Kolkata", "lat": 22.5726, "lng": 88.3639, "spread": 0.15},
    {"name": "Chennai", "lat": 13.0827, "lng": 80.2707, "spread": 0.1}
]

CRIME_TYPES = ["Theft", "Assault", "Vandalism", "Cyber/Fraud", "Burglary"]
SEVERITIES = ["Low", "Medium", "High"]

def seed_data(num_records=500):
    with app.app_context():
        print("Clearing existing incidents...")
        db.session.query(Incident).delete()
        
        print(f"Generating {num_records} incidents...")
        incidents = []
        for _ in range(num_records):
            city = random.choice(CITIES)
            
            # Add random spread to coords
            lat = city["lat"] + random.uniform(-city["spread"], city["spread"])
            lng = city["lng"] + random.uniform(-city["spread"], city["spread"])
            
            # Generate date within last 30 days
            days_ago = random.randint(0, 30)
            timestamp = (datetime.now() - timedelta(days=days_ago)).isoformat()
            
            incident = Incident(
                type=random.choice(CRIME_TYPES),
                lat=lat,
                lng=lng,
                severity=random.choices(SEVERITIES, weights=[40, 40, 20])[0], # Less high severity
                status=random.choice(["Active", "Resolved"]),
                area=f"{city['name']} - {fake.street_name()}",
                timestamp=timestamp
            )
            incidents.append(incident)
            
        db.session.bulk_save_objects(incidents)
        db.session.commit()
        
        from app import PatrolUnit
        print("Clearing existing patrols...")
        db.session.query(PatrolUnit).delete()
        print("Generating mock Patrol Units...")
        patrols = []
        for i, city in enumerate(CITIES):
            # 2 units per city
            for j in range(2):
                lat = city["lat"] + random.uniform(-city["spread"], city["spread"])
                lng = city["lng"] + random.uniform(-city["spread"], city["spread"])
                patrols.append(PatrolUnit(name=f"Unit-{city['name'][:3].upper()}-0{j+1}", lat=lat, lng=lng, status="Available"))
        db.session.bulk_save_objects(patrols)
        db.session.commit()
        
        print("Seed complete! Dashboard is ready for demo.")

if __name__ == '__main__':
    seed_data(500)
