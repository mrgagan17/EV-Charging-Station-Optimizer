<div align="center">
  <h1>⚡ Smart City EV Charging Station Optimizer</h1>
  <p><i>An AI-driven geospatial clustering tool for urban infrastructure planning.</i></p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

---

## 📖 About The Project

As the adoption of Electric Vehicles (EVs) accelerates, city planners face a critical challenge: **Where is the most mathematically optimal location to build new charging infrastructure?**

This project solves that problem for **Bengaluru, India** (and can be scaled globally). By ingesting live geospatial data of existing infrastructure and applying unsupervised machine learning (**K-Means Clustering**), this web application identifies the highest-density EV traffic zones and calculates the exact geographic coordinates for future charging hubs. 

It completely removes the guesswork from urban planning, replacing it with data-driven, interactive mapping.

<details>
  <summary><strong>View Table of Contents</strong></summary>
  <ol>
    <li><a href="#-key-features">Key Features</a></li>
    <li><a href="#-tech-stack">Tech Stack</a></li>
    <li><a href="#-how-it-works-under-the-hood">How It Works</a></li>
  </ol>
</details>

---

## ✨ Key Features

* 📡 **Live API Integration:** Bypasses static CSV files by querying the OpenStreetMap Overpass API for real-time `amenity=charging_station` nodes.
* 🧠 **Unsupervised Machine Learning:** Implements `scikit-learn`'s K-Means algorithm to dynamically cluster geographical coordinates based on user inputs.
* 🗺️ **Interactive Geospatial Mapping:** Uses `folium` to render a responsive, Google-styled map featuring existing stations (blue) and proposed mathematical optimal hubs (red).
* 📍 **Automated Reverse Geocoding:** Translates raw mathematically-derived GPS coordinates into real-world, human-readable street addresses using `geopy` (Nominatim API).
* 📈 **Elbow Method Analytics:** Features a built-in mathematical evaluation tool to help users verify the optimal number of clusters ($k$) via Within-Cluster Sum of Squares (WCSS).
* 🛡️ **Failsafe Mechanisms:** Includes automatic `try/except` fallbacks for API rate-limiting to ensure the application remains strictly highly available.

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | `Streamlit` | Rapid deployment of the interactive web dashboard. |
| **Data Processing** | `Pandas`, `NumPy` | Data structuring, cleaning, and matrix array manipulation. |
| **Machine Learning** | `Scikit-Learn` | Execution of the K-Means algorithm and inertia calculations. |
| **Mapping / GIS** | `Folium`, `Streamlit-Folium` | Rendering the interactive Leaflet.js map and markers. |
| **External APIs** | `Requests`, `Geopy` | Fetching OSM data and reverse-geocoding coordinates. |

---

## 🧠 How It Works (Under the Hood)

1. **Data Ingestion:** A bounding-box query `(12.75,77.40, 13.15,77.80)` is sent to the Overpass API. This isolates Bengaluru and fetches all known EV stations in milliseconds.
2. **Hyperparameter Tuning:** The algorithm calculates the inertia (WCSS) for $k$ values 1 through 10. The user inspects the resulting **Elbow Curve** to select the optimal number of proposed hubs.
3. **Centroid Calculation:** The K-Means model iteratively assigns each geographic point to the nearest cluster and recalculates the mean (centroid) of that cluster. The final converged centroids represent the absolute mathematical minimum distance for the highest number of drivers.
4. **Geocoding:** The raw float values (e.g., `12.9716, 77.5946`) of the centroids are passed to the Nominatim API, which returns the nearest real-world physical address for construction teams.

---
