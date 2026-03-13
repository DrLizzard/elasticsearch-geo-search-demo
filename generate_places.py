import random
import requests
import urllib3

urllib3.disable_warnings()

ES_URL = "https://localhost:9200/places/_doc"
AUTH = ("elastic", "0AO9u3rks4ZQrNa5cvbI")

categories = ["restaurant", "cafe", "bar", "pizza", "burger", "steakhouse"]

base_lat = -26.2041
base_lon = 28.0473

for i in range(1000):
    data = {
        "name": f"Place {i}",
        "category": random.choice(categories),
        "rating": round(random.uniform(3.0, 5.0), 1),
        "location": {
            "lat": base_lat + random.uniform(-0.15, 0.15),
            "lon": base_lon + random.uniform(-0.15, 0.15)
        }
    }

    r = requests.post(ES_URL, json=data, auth=AUTH, verify=False)

    if i % 100 == 0:
        print(f"Inserted {i} places")

print("Finished inserting places")