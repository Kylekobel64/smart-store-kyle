import pandas as pd
import sqlite3
from pathlib import Path

# Paths
DB_PATH = Path("data/dw/smart_sales.db")
OUTPUT_PATH = Path("data/prepared/olap_cube_output.csv")

def create_olap_cube():
    conn = sqlite3.connect(DB_PATH)

    # Query to join tables and get relevant fields
    query = """
        SELECT
            s.TransactionID,
            s.SaleDate,
            c.Region,
            c.CustomerID,
            p.ProductID,
            p.Category,
            s.SaleAmount
        FROM sale s
        JOIN customer c ON s.CustomerID = c.CustomerID
        JOIN product p ON s.ProductID = p.ProductID
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Parse date and extract time dimensions
    df["SaleDate"] = pd.to_datetime(df["SaleDate"])
    df["Year"] = df["SaleDate"].dt.year
    df["Month"] = df["SaleDate"].dt.month
    df["DayOfWeek"] = df["SaleDate"].dt.day_name()

    # Convert SaleAmount to numeric (in case it's string in db)
    df["SaleAmount"] = pd.to_numeric(df["SaleAmount"], errors='coerce')

    # Define dimensions and metrics
    dimensions = ["Year", "Month", "Region", "Category"]
    metrics = {
        "SaleAmount": ["sum", "mean", "count"]
    }

    # Create the OLAP-style cube
    cube = df.groupby(dimensions).agg(metrics)
    cube.columns = ['_'.join(col).strip() for col in cube.columns.values]
    cube = cube.reset_index()

    # Save to CSV
    cube.to_csv(OUTPUT_PATH, index=False)
    print(f"OLAP cube saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    create_olap_cube()