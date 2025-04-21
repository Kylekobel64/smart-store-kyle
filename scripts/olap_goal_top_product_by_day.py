import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

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
    df["SaleAmount"] = pd.to_numeric(df["SaleAmount"], errors="coerce")
    return df.dropna(subset=["SaleAmount"])

def get_top_n_products_by_day(df: pd.DataFrame, top_n=3) -> pd.DataFrame:
    grouped = (
        df.groupby(["DayOfWeek", "ProductName"])["SaleAmount"]
        .sum()
        .reset_index()
    )
    
    # Rank products within each day
    grouped["Rank"] = grouped.groupby("DayOfWeek")["SaleAmount"].rank(method="dense", ascending=False)
    
    # Keep only top N
    return grouped[grouped["Rank"] <= top_n]

def plot_top_products(top_df: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_df, x="DayOfWeek", y="SaleAmount", hue="ProductName", dodge=True)
    plt.title("Top N Selling Products by Day of the Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Total Sales Amount (USD)")
    plt.xticks(rotation=45)
    plt.legend(title="Product", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def main():
    df = fetch_sales_data()
    df = preprocess_data(df)
    top_n_df = get_top_n_products_by_day(df, top_n=3)
    plot_top_products(top_n_df)

if __name__ == "__main__":
    main()
