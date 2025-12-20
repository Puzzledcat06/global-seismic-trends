import pandas as pd
import re

df = pd.read_csv("data/raw/earthquakes_raw.csv")

df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], unit="ms", errors="coerce")

df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

def extract_country(place):
    if pd.isna(place):
        return "Unknown"
    match = re.search(r",\s*([^,]+)$", place)
    return match.group(1) if match else "Unknown"

df["country"] = df["place"].apply(extract_country)

numeric_columns = [
    "mag", "depth_km", "nst", "dmin", "rms",
    "gap", "magError", "depthError", "magNst", "sig"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

text_columns = [
    "magType", "status", "type",
    "net", "sources", "types",
    "locationSource", "magSource"
]

for col in text_columns:
    df[col] = df[col].astype(str).str.lower().str.strip()

def depth_category(depth):
    if depth < 50:
        return "Shallow"
    elif depth <= 300:
        return "Intermediate"
    else:
        return "Deep"

df["depth_category"] = df["depth_km"].apply(depth_category)

def severity_level(mag):
    return "Strong" if mag >= 7 else "Normal"

df["severity"] = df["mag"].apply(severity_level)

df.to_csv("data/processed/earthquakes_cleaned.csv", index=False)
print("Cleaned data saved")
