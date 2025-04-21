Mimport pandas as pd
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
🔍 What this does:
Joins sale, customer, and product tables

Extracts time-based dimensions (year, month, day of week)

Groups data by dimensions like Region, Category, and Year

Aggregates SaleAmount using sum, mean, and count

Outputs the cube as a CSV for reporting or further analysis

Would you like to:

Add more dimensions or metrics?

Drill down to customer- or product-level?

Visualize the cube in a chart (e.g., using Plotly or Matplotlib)?

Just let me know how you'd like to expand it!







You said:
create a py code that will generate visuals and analyzation of top product by day of the week


ChatGPT said:
Here’s a Python script that connects to your existing SQLite database, analyzes sales to find the top-selling product by day of the week, and generates a bar chart for visualization using matplotlib and seaborn.

You can drop this into a script (e.g., analyze_top_product_by_day.py) and run it as long as your database and prepared CSVs are in place.

✅ Script: Analyze & Visualize Top Product by Day of Week
python
Copy
Edit
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set up paths
DB_PATH = Path("data/dw/smart_sales.db")

def fetch_sales_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT 
            s.SaleDate,
            s.SaleAmount,
            p.ProductName
        FROM sale s
        JOIN product p ON s.ProductID = p.ProductID
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df["SaleDate"] = pd.to_datetime(df["SaleDate"])
    df["DayOfWeek"] = df["SaleDate"].dt.day_name()
    df["SaleAmount"] = pd.to_numeric(df["SaleAmount"], errors='coerce')
    return df.dropna(subset=["SaleAmount"])

def get_top_products_by_day(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(["DayOfWeek", "ProductName"])["SaleAmount"].sum().reset_index()
    # Sort and take top product for each day
    top_products = grouped.sort_values(["DayOfWeek", "SaleAmount"], ascending=[True, False])
    top_by_day = top_products.groupby("DayOfWeek").first().reset_index()
    return top_by_day

def plot_top_products(top_df: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_df, x="DayOfWeek", y="SaleAmount", hue="ProductName", dodge=False)
    plt.title("Top-Selling Product by Day of the Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Total Sales Amount (USD)")
    plt.xticks(rotation=45)
    plt.legend(title="Product", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def main():
    sales_df = fetch_sales_data()
    clean_df = preprocess_data(sales_df)
    top_products = get_top_products_by_day(clean_df)
    plot_top_products(top_products)

if __name__ == "__main__":
    main()