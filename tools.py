import os, datetime
import pandas as pd
import matplotlib.pyplot as plt
from langchain.tools import tool, Tool

DATA_PATH = os.getenv("DATA_PATH", "data/sales.csv")

def _load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    # Normalize column names to lower-case for simpler prompts
    df.columns = [c.lower() for c in df.columns]
    return df

DATA = _load_data()

def query_data(expression: str):
    """Return dataframe rows that match a pandas query string. Limit to 50 rows."""
    try:
        df = DATA.query(expression).copy()
        return df.head(50).to_dict(orient="records")
    except Exception as e:
        return {"error": f"Query error: {e}"}

@tool
def quick_stats(column: str, metric: str) -> dict:
    """
    Compute 'sum' or 'avg' over a numeric column.
    Args:
        column: column name (str)
        metric: 'sum' or 'avg'
    """
    try:
        if metric == "sum":
            val = float(DATA[column].sum())
        elif metric == "avg":
            val = float(DATA[column].mean())
        else:
            return {"error": "Metric must be 'sum' or 'avg'"}
        return {metric: val}
    except Exception as e:
        return {"error": f"Stats error: {e}"}

def plot_timeseries(column: str):
    """Group by date and plot the sum of a numeric column over time. Saves a PNG and returns its path."""
    try:
        os.makedirs("charts", exist_ok=True)
        plt.figure()
        DATA.groupby("date")[column].sum().plot()
        path = f"charts/{column}_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
        plt.title(f"{column} over time")
        plt.xlabel("date")
        plt.ylabel(column)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        return path
    except Exception as e:
        return f"Chart error: {e}"

def save_log(text: str):
    """Save chat transcript to logs/ and return the file path."""
    os.makedirs("logs", exist_ok=True)
    fname = f"logs/{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(text)
    return fname

tools = [
    quick_stats,
    Tool(name="query_data", func=query_data, description="Run pandas .query(...) on the dataset with a boolean expression string. Returns up to 50 rows."),
    Tool(name="plot_timeseries", func=plot_timeseries, description="Plot a date-indexed timeseries for a numeric column and return the saved PNG path."),
    Tool(name="save_log", func=save_log, description="Save a transcript string to logs/ and return the path.")
]
