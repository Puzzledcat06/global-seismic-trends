import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("Admin@12345")

engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost:3306/earthquake_db"
)



st.set_page_config(page_title="Global Seismic Trends - All Queries", layout="wide")
st.title("🌍 Global Seismic Trends Dashboard")
st.markdown("### 📌 Select any SQL query to view and analyze the results")

# ----------------------------------
# ALL 30 QUERIES
# ----------------------------------
queries = {
    "1️⃣ Top 10 strongest earthquakes": """
        SELECT id, country, mag
        FROM earthquakes ORDER BY mag DESC LIMIT 10;
    """,
    "2️⃣ Top 10 deepest earthquakes": """
        SELECT id, country, depth_km
        FROM earthquakes ORDER BY depth_km DESC LIMIT 10;
    """,
    "3️⃣ Shallow (<50km) & strong (mag > 7.5)": """
        SELECT id, country, mag, depth_km
        FROM earthquakes WHERE depth_km < 50 AND mag > 7.5;
    """,
    "4️⃣ Average depth by country": """
        SELECT country, AVG(depth_km) AS avg_depth
        FROM earthquakes GROUP BY country ORDER BY avg_depth DESC;
    """,
    "5️⃣ Average magnitude by mag type": """
        SELECT magType, AVG(mag) AS avg_magnitude
        FROM earthquakes GROUP BY magType ORDER BY avg_magnitude DESC;
    """,
    "6️⃣ Year with highest earthquakes": """
        SELECT year, COUNT(*) AS total
        FROM earthquakes GROUP BY year ORDER BY total DESC;
    """,
    "7️⃣ Month with most earthquakes": """
        SELECT month, COUNT(*) AS total
        FROM earthquakes GROUP BY month ORDER BY total DESC;
    """,
    "8️⃣ Most active weekday": """
        SELECT day_of_week, COUNT(*) AS total
        FROM earthquakes GROUP BY day_of_week ORDER BY total DESC;
    """,
    "9️⃣ Earthquake count per hour": """
        SELECT HOUR(time) AS hour_of_day, COUNT(*) AS total
        FROM earthquakes GROUP BY hour_of_day ORDER BY hour_of_day;
    """,
    "🔟 Most active reporting network": """
        SELECT net, COUNT(*) AS total
        FROM earthquakes GROUP BY net ORDER BY total DESC;
    """,
    "11️⃣ Reviewed vs automatic events": """
        SELECT status, COUNT(*) AS total
        FROM earthquakes GROUP BY status;
    """,
    "12️⃣ Events by earthquake type": """
        SELECT type, COUNT(*) AS total
        FROM earthquakes GROUP BY type;
    """,
    "13️⃣ Count by data 'types' column": """
        SELECT types, COUNT(*) AS total
        FROM earthquakes GROUP BY types;
    """,
    "14️⃣ RMS & GAP reliability check": """
        SELECT country, AVG(rms) AS avg_rms, AVG(gap) AS avg_gap
        FROM earthquakes GROUP BY country;
    """,
    "15️⃣ High station coverage (nst > 50)": """
        SELECT id, country, nst
        FROM earthquakes WHERE nst > 50 ORDER BY nst DESC;
    """,
    "16️⃣ Tsunami events per year": """
        SELECT year, COUNT(*) AS tsunami_events
        FROM earthquakes WHERE tsunami = 1 GROUP BY year ORDER BY year;
    """,
    "17️⃣ Avg magnitude: tsunami vs non-tsunami": """
        SELECT tsunami, AVG(mag) AS avg_magnitude
        FROM earthquakes GROUP BY tsunami;
    """,
    "18️⃣ Highest average magnitude countries": """
        SELECT country, AVG(mag) AS avg_mag
        FROM earthquakes GROUP BY country ORDER BY avg_mag DESC LIMIT 5;
    """,
    "19️⃣ Countries with shallow & deep same month": """
        SELECT DISTINCT e1.country, e1.year, e1.month
        FROM earthquakes e1 JOIN earthquakes e2
        ON e1.country=e2.country AND e1.year=e2.year AND e1.month=e2.month
        WHERE e1.depth_category='Shallow' AND e2.depth_category='Deep';
    """,
    "20️⃣ Year-over-year growth": """
        SELECT year, COUNT(*) AS total,
        COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year) AS yoy_change
        FROM earthquakes GROUP BY year;
    """,
    "21️⃣ Top 3 seismic hotspots": """
        SELECT country, COUNT(*) AS frequency, AVG(mag) AS avg_mag
        FROM earthquakes GROUP BY country ORDER BY frequency DESC, avg_mag DESC LIMIT 3;
    """,
    "22️⃣ Avg depth near equator": """
        SELECT country, AVG(depth_km) AS avg_depth
        FROM earthquakes WHERE latitude BETWEEN -5 AND 5 GROUP BY country;
    """,
    "23️⃣ Shallow vs deep ratio": """
        SELECT country,
        SUM(depth_category='Shallow')/NULLIF(SUM(depth_category='Deep'),0) AS ratio
        FROM earthquakes GROUP BY country;
    """,
    "24️⃣ Lowest reliability events": """
        SELECT id, country, rms, gap
        FROM earthquakes ORDER BY rms DESC, gap DESC LIMIT 10;
    """,
    "25️⃣ Deep-focus (>300km) earthquakes": """
        SELECT country, COUNT(*) AS deep_quakes
        FROM earthquakes WHERE depth_km > 300 GROUP BY country ORDER BY deep_quakes DESC;
    """,
    "26️⃣ Yearly seismic activity by country": """
        SELECT country, year, COUNT(*) AS total
        FROM earthquakes GROUP BY country, year;
    """,
    "27️⃣ Avg magnitude by depth category": """
        SELECT depth_category, AVG(mag) AS avg_mag
        FROM earthquakes GROUP BY depth_category;
    """,
    "28️⃣ High significance (sig > 800)": """
        SELECT id, country, mag, sig
        FROM earthquakes WHERE sig > 800 ORDER BY sig DESC;
    """,
    "29️⃣ Consecutive quakes within 1hr": """
        SELECT e1.id AS quake1, e2.id AS quake2,
        ABS(TIMESTAMPDIFF(MINUTE, e1.time, e2.time)) AS time_diff_minutes
        FROM earthquakes e1 JOIN earthquakes e2
        ON e1.id <> e2.id WHERE ABS(TIMESTAMPDIFF(MINUTE, e1.time, e2.time)) <= 60;
    """,
    "30️⃣ Countries with frequent strong quakes (≥6)": """
        SELECT country, COUNT(*) AS strong_quakes
        FROM earthquakes WHERE mag >= 6 GROUP BY country ORDER BY strong_quakes DESC;
    """
}

# ----------------------------------
# UI: SELECT + RUN + DISPLAY
# ----------------------------------
selected = st.selectbox("🔍 Choose a query to run", queries.keys())
sql = queries[selected]

df = pd.read_sql(sql, engine)
st.write("### 📄 Query Result:")
st.dataframe(df, use_container_width=True)

# ----------------------------------
# AUTO-CHART SECTION
# ----------------------------------
numeric_cols = [c for c in df.columns if df[c].dtype != "object"]
if len(numeric_cols) >= 1:
    fig = px.bar(df, x=df.columns[0], y=numeric_cols[0], title=f"📊 Visualization: {selected}")
    st.plotly_chart(fig, use_container_width=True)
