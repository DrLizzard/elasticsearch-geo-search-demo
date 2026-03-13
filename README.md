# Elasticsearch Geospatial Search Project

## Overview

This project demonstrates how Elasticsearch can be used to perform **geospatial search queries**.
The system indexes location-based data (restaurants, cafes, etc.) and allows users to search for nearby places using a **Python Streamlit web interface**.

The project showcases several Elasticsearch capabilities:

* Geo-point indexing
* Distance-based queries
* Sorting by proximity
* Category filtering
* Data ingestion via Python
* Interactive UI using Streamlit

The application simulates a **"Nearby Places Finder"** similar to how delivery or ride-sharing applications search for nearby locations.

---

# System Architecture

Components used:

* **Ubuntu 24.04 VM**
* **Docker**
* **Elasticsearch 8**
* **Python 3**
* **Streamlit UI**
* **Python Elasticsearch client**

Flow:

```
Python Script → Elasticsearch → Streamlit UI → User
```

1. Python script generates and indexes sample locations.
2. Elasticsearch stores and indexes the data.
3. Streamlit queries Elasticsearch.
4. Results are displayed in a web interface.

---

# Installation Guide (Step-by-Step)

## 1. Update Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

---

# 2. Install Docker

Install required packages:

```bash
sudo apt install -y ca-certificates curl gnupg
```

Add Docker repository:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

Add Docker source:

```bash
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list
```

Install Docker:

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y
```

Test Docker:

```bash
docker run hello-world
```

---

# 3. Configure Elasticsearch Requirements

Elasticsearch requires this kernel setting:

```bash
sudo sysctl -w vm.max_map_count=262144
```

Make it permanent:

```bash
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

---

# 4. Run Elasticsearch Container

```bash
docker run -d \
--name elasticsearch \
-p 9200:9200 \
-p 9300:9300 \
-e "discovery.type=single-node" \
-e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
docker.elastic.co/elasticsearch/elasticsearch:8.13.4
```

---

# 5. Reset Elasticsearch Password

```bash
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```

Save the generated password.

Test connection:

```bash
curl -k -u elastic:PASSWORD https://localhost:9200
```

---

# 6. Create Project Directory

```bash
mkdir elastic_project
cd elastic_project
```

---

# 7. Create Python Virtual Environment

```bash
sudo apt install python3-venv python3-full -y
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

---

# 8. Install Python Dependencies

```bash
pip install streamlit
pip install "elasticsearch>=8,<9"
pip install requests
```

---

# 9. Create Elasticsearch Index

```bash
curl -k -u elastic:PASSWORD \
-X PUT https://localhost:9200/places \
-H "Content-Type: application/json" \
-d '{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "category": { "type": "keyword" },
      "rating": { "type": "float" },
      "location": { "type": "geo_point" }
    }
  }
}'
```

---

# 10. Generate Sample Data

Create `generate_places.py` to insert ~1000 locations.

Run:

```bash
python generate_places.py
```

Verify data count:

```bash
curl -k -u elastic:PASSWORD https://localhost:9200/places/_count
```

---

# 11. Run the Streamlit Web Interface

Start the application:

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

# Features Demonstrated

### Geospatial Search

Find places within a radius.

Example:

```
Find restaurants within 5km
```

---

### Distance Sorting

Return results ordered by proximity.

---

### Category Filtering

Search only specific types of locations:

* Restaurants
* Cafes
* Bars
* Pizza
* Burgers

---

### Aggregations

Elasticsearch can compute analytics such as:

* Number of restaurants
* Number of cafes
* Average ratings

---

# Example Queries

### Geo Distance Query

```json
{
  "query": {
    "geo_distance": {
      "distance": "5km",
      "location": {
        "lat": -26.2041,
        "lon": 28.0473
      }
    }
  }
}
```

---

# Future Improvements

Possible extensions:

* Map visualization with markers
* Real-world datasets from OpenStreetMap
* Heatmap visualization using geohash grids
* Integration with a frontend framework
* Real-time data ingestion

---

# Conclusion

This project demonstrates how Elasticsearch can power **location-based search systems** similar to those used by modern applications such as:

* Food delivery services
* Ride-sharing platforms
* Store locator systems

The combination of Elasticsearch, Python, and Streamlit provides a lightweight but powerful framework for building interactive geospatial applications.

---

# Lessons Learned

During the development of this project several important concepts and practical skills were learned.

### Working with Docker

Running Elasticsearch inside Docker simplified the setup process. Instead of installing Elasticsearch directly on the system, Docker allowed the service to run in an isolated container that could easily be started, stopped, or recreated. It also made it easier to manage ports and system resources.

### Elasticsearch Configuration

Elasticsearch requires certain system configurations, such as increasing the `vm.max_map_count` kernel parameter. Without this setting Elasticsearch may fail to start. Understanding these requirements helped ensure the container runs reliably.

### Index Design and Mapping

Defining the correct mapping is important for Elasticsearch performance and functionality.
In this project the `geo_point` field type was used to store geographic coordinates. This allowed Elasticsearch to perform geospatial queries such as distance calculations and location filtering.

### Geospatial Queries

One of the key features explored was Elasticsearch's geospatial capabilities. Using `geo_distance` queries made it possible to search for locations within a specific radius from a given coordinate. This type of functionality is commonly used in applications like delivery services, ride-sharing platforms, and store locators.

### Data Ingestion with Python

Python was used to generate and insert sample data into Elasticsearch. This demonstrated how applications can programmatically send documents to Elasticsearch using its REST API.

### Version Compatibility

During development a version mismatch occurred between the Elasticsearch server and the Python Elasticsearch client library. The issue was resolved by installing the correct client version (`elasticsearch>=8,<9`). This highlighted the importance of matching client libraries with the server version.

### Using Virtual Environments

Ubuntu prevents system-wide Python package installation for safety reasons. Creating a Python virtual environment (`venv`) allowed project dependencies to be installed safely without affecting the system Python installation.

### Building a Simple UI

Streamlit made it possible to quickly build a web interface for querying Elasticsearch. With only a few lines of Python code, the application could accept user input, send search queries to Elasticsearch, and display results in a browser.

### Practical Use of Elasticsearch

This project demonstrated that Elasticsearch is not only a search engine but also a powerful analytics and geospatial database. The ability to perform location-based queries and aggregations makes it suitable for many real-world applications.

Overall, the project provided hands-on experience with containerized services, search infrastructure, geospatial data, and building simple data-driven applications.



