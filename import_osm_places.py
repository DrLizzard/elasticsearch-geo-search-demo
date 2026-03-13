import requests
import urllib3

urllib3.disable_warnings()

ELASTIC_URL = "https://localhost:9200/places/_doc"
AUTH = ("elastic","0AO9u3rks4ZQrNa5cvbI")

overpass_url = "https://overpass-api.de/api/interpreter"

query = """
[out:json][timeout:25];
(
  node["amenity"="restaurant"](-26.3,27.8,-25.7,28.4);
  node["amenity"="cafe"](-26.3,27.8,-25.7,28.4);
  node["amenity"="fast_food"](-26.3,27.8,-25.7,28.4);
  node["amenity"="bar"](-26.3,27.8,-25.7,28.4);
);
out;
"""

print("Downloading data from OpenStreetMap...")

# Ensure index exists
mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "category": {"type": "keyword"},
            "location": {"type": "geo_point"}
        }
    }
}

requests.put(
    "https://localhost:9200/places",
    json=mapping,
    auth=AUTH,
    verify=False
)

response = requests.post(overpass_url, data=query)
data = response.json()

count = 0

for place in data["elements"]:
    tags = place.get("tags", {})

    name = tags.get("name")

    if not name:
        continue

    doc = {
        "name": name,
        "category": tags.get("amenity", "unknown"),
        "location": {
            "lat": place["lat"],
            "lon": place["lon"]
        }
    }

    r = requests.post(
        ELASTIC_URL,
        json=doc,
        auth=AUTH,
        verify=False
    )

    if r.status_code >= 300:
        print("Error inserting:", r.text)

    count += 1

    if count % 100 == 0:
        print(f"Inserted {count} places")

print("Finished importing real locations:", count)