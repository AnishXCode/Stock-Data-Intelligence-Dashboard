import pandas as pd 
from db import Session, engine
from models import Stocks
import models

def getAllStocks():
    try:
        import certifi
        import requests
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.nseindia.com/",
        }

        response = requests.get(url, headers=headers, verify=certifi.where())
        response.raise_for_status()

        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        df.columns = df.columns.str.strip().str.upper()
        df = df[df["SERIES"] == "EQ"] 
        df = df.dropna(subset=["SYMBOL"])

        print(f"Fetched {len(df)} companies from NSE.")
        print(df.head(11))
        return df
    except Exception as e:
        print(f"Fetching data failed: {e}")
        return []

def storeCompanies(df: pd.DataFrame, Session):
    try:
        rows = []
        for _, row in df.iterrows():
            rows.append(Stocks(
                name = str(row.get("NAME OF COMPANY", "")).strip(),
                symbol = str(row.get("SYMBOL", "")).strip(),
                series = str(row.get("SERIES", "")).strip(),
                date_listing = str(row.get("DATE OF LISTING", "")).strip(),
            ))
        
        with Session() as session:
            session.query(Stocks).delete()
            session.bulk_save_objects(rows)
            session.commit()
        
        print(f"Stored {len(rows)} companies in Stocks table")
    except Exception as e:
        print(f"Failed to store data into database: {e}")


def initDatabase():
    try: 
        models.Base.metadata.create_all(bind=engine)

        data = getAllStocks()
        storeCompanies(data, Session)

        print("Successfully initialized Database")
    except Exception as e:
        print(f"Database initialization failed: {e}")

initDatabase()
