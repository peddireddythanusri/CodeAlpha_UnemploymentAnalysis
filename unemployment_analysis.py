# ============================================================
# CodeAlpha Data Science Internship - Task 2
# Unemployment Analysis with Python
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

REAL_DATASET = "Unemployment_Rate_upto_11_2020.csv"
SAMPLE_DATASET = "sample_unemployment_data.csv"

# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------
if os.path.exists(REAL_DATASET):
    file_name = REAL_DATASET
    print(f"Using dataset: {REAL_DATASET}")
else:
    file_name = SAMPLE_DATASET
    print(f"\nWARNING: {REAL_DATASET} was not found.")
    print(f"Running with the included educational sample dataset: {SAMPLE_DATASET}")
    print("For your final internship submission, replace it with the real dataset.\n")

df = pd.read_csv(file_name)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

print("=" * 65)
print("UNEMPLOYMENT ANALYSIS WITH PYTHON")
print("=" * 65)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nStatistical Summary:")
print(df.describe(include="all"))

# ------------------------------------------------------------
# 2. DATA CLEANING
# ------------------------------------------------------------
df = df.dropna().copy()
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
df = df.dropna(subset=["Date"])

# Convert numeric columns safely
numeric_columns = [
    "Estimated Unemployment Rate (%)",
    "Estimated Employed",
    "Estimated Labour Participation Rate (%)"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Estimated Unemployment Rate (%)"])

print("\nData cleaned successfully.")
print("Cleaned dataset shape:", df.shape)

# Create output folder
os.makedirs("images", exist_ok=True)

# ------------------------------------------------------------
# 3. OVERALL UNEMPLOYMENT TREND
# ------------------------------------------------------------
monthly = (
    df.groupby("Date")["Estimated Unemployment Rate (%)"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(10, 6))
plt.plot(
    monthly["Date"],
    monthly["Estimated Unemployment Rate (%)"],
    marker="o"
)
plt.title("Average Unemployment Rate in India Over Time")
plt.xlabel("Date")
plt.ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/01_unemployment_trend.png", dpi=300)
plt.show()

# ------------------------------------------------------------
# 4. STATE-WISE UNEMPLOYMENT ANALYSIS
# ------------------------------------------------------------
state_avg = (
    df.groupby("Region")["Estimated Unemployment Rate (%)"]
    .mean()
    .sort_values(ascending=False)
)

top_states = state_avg.head(10)

plt.figure(figsize=(11, 6))
plt.bar(top_states.index, top_states.values)
plt.title("Top States by Average Unemployment Rate")
plt.xlabel("State")
plt.ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("images/02_statewise_unemployment.png", dpi=300)
plt.show()

# ------------------------------------------------------------
# 5. COVID-19 IMPACT ANALYSIS
# ------------------------------------------------------------
df["Period"] = df["Date"].apply(
    lambda x: "Pre-COVID" if x.month <= 3 else "COVID / Recovery Period"
)

covid_comparison = (
    df.groupby("Period")["Estimated Unemployment Rate (%)"]
    .mean()
)

plt.figure(figsize=(7, 5))
plt.bar(covid_comparison.index, covid_comparison.values)
plt.title("Impact of COVID-19 on Unemployment")
plt.xlabel("Period")
plt.ylabel("Average Unemployment Rate (%)")
plt.tight_layout()
plt.savefig("images/03_covid_impact.png", dpi=300)
plt.show()

# ------------------------------------------------------------
# 6. EMPLOYMENT VS UNEMPLOYMENT
# ------------------------------------------------------------
plt.figure(figsize=(8, 6))
plt.scatter(
    df["Estimated Employed"],
    df["Estimated Unemployment Rate (%)"],
    alpha=0.7
)
plt.title("Employment vs Unemployment Rate")
plt.xlabel("Estimated Employed")
plt.ylabel("Estimated Unemployment Rate (%)")
plt.tight_layout()
plt.savefig("images/04_employment_vs_unemployment.png", dpi=300)
plt.show()

# ------------------------------------------------------------
# 7. AREA-WISE ANALYSIS
# ------------------------------------------------------------
if "Area" in df.columns:
    area_avg = (
        df.groupby("Area")["Estimated Unemployment Rate (%)"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    plt.bar(area_avg.index.astype(str), area_avg.values)
    plt.title("Average Unemployment Rate by Area")
    plt.xlabel("Area")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.tight_layout()
    plt.savefig("images/05_area_analysis.png", dpi=300)
    plt.show()

# ------------------------------------------------------------
# 8. KEY INSIGHTS
# ------------------------------------------------------------
highest_state = state_avg.index[0]
highest_rate = state_avg.iloc[0]

peak_row = monthly.loc[
    monthly["Estimated Unemployment Rate (%)"].idxmax()
]

print("\n" + "=" * 65)
print("KEY INSIGHTS")
print("=" * 65)
print(f"1. Highest average unemployment rate: {highest_state} ({highest_rate:.2f}%)")
print(
    "2. Peak average unemployment month: "
    f"{peak_row['Date'].strftime('%B %Y')} "
    f"({peak_row['Estimated Unemployment Rate (%)']:.2f}%)"
)
print(
    "3. Average Pre-COVID unemployment rate: "
    f"{covid_comparison.get('Pre-COVID', float('nan')):.2f}%"
)
print(
    "4. Average COVID / Recovery unemployment rate: "
    f"{covid_comparison.get('COVID / Recovery Period', float('nan')):.2f}%"
)

print("\nAnalysis completed successfully!")
print("Graphs have been saved inside the images folder.")
