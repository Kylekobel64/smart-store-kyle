# smart-store-kyle

Starter files to initialize the smart sales project.

-----
## Project Setup Guide (2-Windows)

Run all commands from a PowerShell terminal in the root project folder.

### Step 2A - Create a Local Project Virtual Environment

```shell
py -m venv .venv
```

### Step 2B - Activate the Virtual Environment

```shell
.venv\Scripts\activate
```

### Step 2C - Install Packages

```shell
py -m pip install --upgrade -r requirements.txt
```

### Step 2D - Optional: Verify .venv Setup

```shell
py -m datafun_venv_checker.venv_checker
```

### Step 2E - Run the initial project script

```shell
py scripts/data_prep.py
```

-----

## Initial Package List

- pip
- loguru
- ipykernel
- jupyterlab
- numpy
- pandas
- matplotlib
- seaborn
- plotly
- pyspark==4.0.0.dev1
- pyspark[sql]
- git+https://github.com/denisecase/datafun-venv-checker.git#egg=datafun_venv_checker
  
  Data Cleaning Process (using Python pandas)
1. Initial Data Inspection and Profiling
df.info(): Check data types and identify missing values.
df.describe(): Get summary statistics for numerical columns.
df.head() and df.sample(): Inspect the structure and sample of the data.
2. Handle Missing Data
Identify missing values: df.isnull().sum()
Drop missing values: df.dropna()
Fill missing values: df.fillna(value)
3. Remove Duplicates
Identify duplicates: df.duplicated()
Drop duplicates: df.drop_duplicates()
4. Filter or Handle Outliers
Identify outliers: df.describe() and box plot visualization.
Filter outliers: df[df['column'] < upper_bound]
5. Data Type Conversion and Standardization
Convert data types: df.astype()
Parse dates: pd.to_datetime(df['column'])
6. Standardize and Format Data
Apply string formatting: df['column'].str.lower() and df['column'].str.strip()
Rename columns: df.rename(columns={'old_name': 'new_name'})
7. Column Management
Drop unnecessary columns: df.drop(columns=['column'])
Reorder columns: df = df[['col1', 'col2', ...]]
8. Data Integration and Aggregation
Merge data: pd.merge(df1, df2, on='key_column')
Aggregate data: df.groupby().agg()
9. Final Quality Checks
Check data consistency, completeness, and final structure.