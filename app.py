import streamlit as st
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "0AO9u3rks4ZQrNa5cvbI"),
    verify_certs=False
)

def get_heatmap():
    res = es.search(
        index="places",
        size=0,
        aggs={
            "hotspots": {
                "geohash_grid": {
                    "field": "location",
                    "precision": 5
                }
            }
        }
    )
    return res["aggregations"]["hotspots"]["buckets"]

st.set_page_config(page_title="Nearby Places Finder", layout="wide")

st.sidebar.markdown("### Elasticsearch Demo")
st.sidebar.write("Search nearby places using geospatial queries.")

st.title("📍 Nearby Places Finder")
st.write("Search for nearby restaurants, cafes, and other places using Elasticsearch geospatial queries.")

# Layout columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Search Settings")

    st.sidebar.header("Search Controls")

    lat = st.sidebar.number_input("Latitude", value=-26.2041)
    lon = st.sidebar.number_input("Longitude", value=28.0473)

    distance = st.sidebar.slider("Distance (km)", 1, 20, 5)

    category = st.sidebar.selectbox(
        "Category",
        ["all", "restaurant", "cafe", "bar", "pizza", "burger"]
    )

    search = st.sidebar.button("Search")

with col2:
    st.subheader("Results")

if search:

    query = {
        "bool": {
            "filter": [
                {
                    "geo_distance": {
                        "distance": f"{distance}km",
                        "location": {
                            "lat": lat,
                            "lon": lon
                        }
                    }
                }
            ]
        }
    }

    if category != "all":
        query["bool"]["must"] = [{"term": {"category": category}}]

    res = es.search(
        index="places",
        query=query,
        size=200,
        sort=[
            {
                "_geo_distance": {
                    "location": {"lat": lat, "lon": lon},
                    "order": "asc",
                    "unit": "km"
                }
            }
        ]
    )

    total_results = res["hits"]["total"]["value"]
    search_time = res["took"]

    st.info(f"🔎 {total_results} places found in {search_time} ms")

    locations = []

    for hit in res["hits"]["hits"]:
        place = hit["_source"]
        distance = hit["sort"][0]

        rating = place.get("rating", "N/A")

        st.success(
            f"📍 {place['name']} | {place['category']} | ⭐ {rating} | {distance:.2f} km away"
        )

        locations.append({
            "lat": place["location"]["lat"],
            "lon": place["location"]["lon"]
        })

    # 🔥 Hotspot analytics
    st.subheader("🔥 Location Hotspots")

    buckets = get_heatmap()

    for bucket in buckets[:10]:
        st.write(f"Grid: {bucket['key']} | Places: {bucket['doc_count']}")

    if locations:
        st.subheader("Map View")
        st.map(locations)
