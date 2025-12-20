import pandas as pd
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

df = pd.read_csv("data/processed/earthquakes_cleaned.csv")

password = quote_plus("Admin@12345")

engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost/earthquake_db"
)

df.to_sql(
    name="earthquakes",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data loaded into MySQL successfully")
print("Rows inserted:", len(df))

