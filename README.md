# Global Seismic Trends: Data-Driven Earthquake Insights

## Project Overview
This project focuses on analyzing global earthquake data to identify seismic patterns, trends, and high-risk zones using a complete data analytics pipeline. The solution integrates API-based data collection, data preprocessing, SQL-based analysis, and interactive visualization to provide meaningful insights for disaster management and geoscience research.

## Domain
- Disaster Management
- Geoscience
- Seismology

## Data Source
- **USGS Earthquake API**  
  https://earthquake.usgs.gov/fdsnws/event/1/query

## Technologies Used
- Python (Requests, Pandas, Regex)
- MySQL
- SQLAlchemy
- SQL
- Streamlit
- Plotly
- VS Code

## Project Structure
global-seismic-trends/
│
├── main.py
│
├── data/
│ ├── raw/
│ │ └── earthquakes_raw.csv
│ └── processed/
│ └── earthquakes_cleaned.csv
│
├── src/
│ ├── api_fetch.py
│ ├── data_cleaning.py
│ └── mysql_loader.py
│
├── sql/
│ └── analysis_queries.sql
│
├── dashboard/
│ └── app.py
│
├── requirements.txt
└── README.md


## File & Folder Description

### `main.py`
Acts as the **entry point** for the project.  
It orchestrates the complete data pipeline by sequentially running:
1. API data collection
2. Data cleaning and preprocessing
3. Loading cleaned data into MySQL  

This file does **not** run the Streamlit dashboard. Streamlit is intentionally kept separate as it is an interactive, long-running process.

---

### `src/api_fetch.py`
- Fetches global earthquake data from the USGS API
- Collects data from **2020 to present**
- Handles leap years and varying month lengths
- Saves raw data to `data/raw/earthquakes_raw.csv`

---

### `src/data_cleaning.py`
- Cleans and preprocesses raw earthquake data
- Converts timestamps to datetime format
- Uses regex to extract country information
- Creates derived columns such as year, depth category, and severity
- Saves cleaned data to `data/processed/earthquakes_cleaned.csv`

---

### `src/mysql_loader.py`
- Loads cleaned earthquake data into MySQL
- Uses SQLAlchemy for database connectivity
- Automatically creates and populates the `earthquakes` table

---

### `sql/analysis_queries.sql`
- Contains **30 analytical SQL queries**
- Covers:
  - Magnitude and depth analysis
  - Time-based trends
  - Country-wise seismic activity
  - Tsunami and severity analysis
  - Advanced seismic patterns

---

### `dashboard/app.py`
- Streamlit application for interactive visualization
- Connects directly to the MySQL database
- Provides filters and visual insights into earthquake trends

---

## Project Workflow

1. Data is collected from the USGS Earthquake API.
2. Raw data is cleaned, standardized, and enriched using Python.
3. Cleaned data is stored in a MySQL database.
4. SQL queries are executed for analytical insights.
5. An interactive Streamlit dashboard visualizes key trends.

---

## How to Run the Project

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt

Step 2: Run the Data Pipeline

This will fetch data, clean it, and load it into MySQL.

python main.py

Step 3: Run Streamlit Dashboard (Separately)

The Streamlit dashboard should be run independently from the data pipeline.

python -m streamlit run dashboard/app.py --server.address localhost --server.port 9000

Important Note

The Streamlit dashboard is intentionally kept separate from main.py to maintain modularity and prevent blocking behavior, as Streamlit is an interactive UI process.

Key Features

End-to-end data pipeline

Regex-based data extraction

SQL-driven analytical insights

Interactive visualization dashboard

Modular and maintainable project structure

Conclusion

This project demonstrates a complete data analytics workflow applied to global seismic data. The insights generated can support disaster management, risk assessment, and geoscience research through data-driven decision-making.
