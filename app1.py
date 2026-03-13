import streamlit as st
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "0AO9u3rks4ZQrNa5cvbI"),
    verify_certs=False
)

st.title("Nearby Places Finder")

lat = st.number_input("Latitude", value=-26.2041)
lon = st.number_input("Longitude", value=28.0473)
distance = st.slider("Distance (km)", 1, 20, 5)

category = st.selectbox(
    "Category",
    ["all", "restaurant", "cafe", "bar", "pizza", "burger"]
)

query = {
    "bool": {
        "filter": [
            {
                "geo_distance": {
                    "distance": f"{distance}km",
                    "location": {"lat": lat, "lon": lon}
                }
            }
        ]
    }
}

if category != "all":
    query["bool"]["must"] = [{"term": {"category": category}}]



agg = es.search(
    index="places",
    size=0,
    aggs={
        "categories": {
            "terms": {"field": "category"}
        }
    }
)

st.subheader("Place distribution")

for bucket in agg["aggregations"]["categories"]["buckets"]:
    st.write(bucket["key"], bucket["doc_count"])








if st.button("Search"):
    res = es.search(index="places", query=query)

    locations = []

    for hit in res["hits"]["hits"]:
        place = hit["_source"]

        st.write(f"📍 {place['name']} | {place['category']} | ⭐ {place['rating']}")

        locations.append({
            "lat": place["location"]["lat"],
            "lon": place["location"]["lon"]
        })

    if locations:
        st.map(locations)