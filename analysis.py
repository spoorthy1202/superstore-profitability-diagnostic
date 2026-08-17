"""
Superstore Profitability Diagnostic
-------------------------------------
Business question: Where is this company losing money despite growing
sales, and what should leadership do about it?

Run: python analysis.py
Outputs: three PNG charts + printed summary tables
"""

import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/superstore.csv"
CHARTS_DIR = "charts"


def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    assert df.isna().sum().sum() == 0, "Unexpected missing values"
    return df


def profit_by_subcategory(df):
    sub = df.groupby("Sub_Category").agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Sales", "count")
    ).sort_values("Profit")
    sub["Margin_%"] = (sub["Profit"] / sub["Sales"] * 100).round(1)
    return sub


def margin_by_discount_band(df):
    df = df.copy()
    df["DiscBand"] = pd.cut(
        df["Discount"], bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.5, 1],
        labels=["0%", "0-10%", "10-20%", "20-30%", "30-50%", "50%+"],
    )
    band = df.groupby("DiscBand", observed=True).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum")
    )
    band["Margin_%"] = (band["Profit"] / band["Sales"] * 100).round(1)
    return band


def margin_by_region(df):
    reg = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    reg["Margin_%"] = (reg["Profit"] / reg["Sales"] * 100).round(1)
    return reg


def make_charts(df):
    sub = df.groupby("Sub_Category")["Profit"].sum().sort_values()
    colors = ["#d64545" if v < 0 else "#3f7fd1" for v in sub.values]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(sub.index, sub.values, color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title("Total Profit by Sub-Category", fontsize=13, weight="bold")
    ax.set_xlabel("Profit ($)")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/chart1_profit_by_subcategory.png")
    plt.close()

    band = margin_by_discount_band(df)
    colors2 = ["#3f7fd1" if v >= 0 else "#d64545" for v in band["Margin_%"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(band.index.astype(str), band["Margin_%"], color=colors2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Profit Margin % by Discount Band", fontsize=13, weight="bold")
    ax.set_ylabel("Profit Margin (%)")
    ax.set_xlabel("Discount Band")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/chart2_margin_by_discount.png")
    plt.close()

    reg = margin_by_region(df)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(reg.index, reg["Margin_%"], color="#3f7fd1")
    ax.set_title("Profit Margin % by Region", fontsize=13, weight="bold")
    ax.set_ylabel("Profit Margin (%)")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_DIR}/chart3_margin_by_region.png")
    plt.close()


if __name__ == "__main__":
    df = load_data()
    print("=== Profit by Sub-Category ===")
    print(profit_by_subcategory(df).round(0))
    print("\n=== Margin by Discount Band ===")
    print(margin_by_discount_band(df).round(0))
    print("\n=== Margin by Region ===")
    print(margin_by_region(df).round(0))
    make_charts(df)
    print("\nCharts saved to current directory.")