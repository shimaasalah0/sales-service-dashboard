
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Setup ---
df = pd.read_csv('data/cleaned_data.csv')
df['OrderDate']      = pd.to_datetime(df['OrderDate'])
df['Month']          = df['OrderDate'].dt.to_period('M').astype(str)

sns.set_theme(style='whitegrid')
os.makedirs('visuals', exist_ok=True)

# --- Chart 1: Monthly Revenue Trend ---
monthly = df.groupby('Month')['Revenue'].sum().reset_index()

plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly, x='Month', y='Revenue', marker='o', color='steelblue')
plt.title('Monthly Revenue Trend 2024', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Total Revenue (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visuals/monthly_revenue.png')
plt.close()
print("Chart 1 saved: monthly_revenue.png")

# --- Chart 2: Revenue by Category ---
category = df.groupby('Category')['Revenue'].sum().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(data=category, x='Category', y='Revenue', palette='Blues_d')
plt.title('Revenue by Category', fontsize=14, fontweight='bold')
plt.xlabel('Category')
plt.ylabel('Total Revenue (USD)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('visuals/revenue_by_category.png')
plt.close()
print("Chart 2 saved: revenue_by_category.png")

# --- Chart 3: Revenue by Region ---
region = df.groupby('Region')['Revenue'].sum().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(data=region, x='Region', y='Revenue', palette='Greens_d')
plt.title('Revenue by Region', fontsize=14, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Total Revenue (USD)')
plt.tight_layout()
plt.savefig('visuals/revenue_by_region.png')
plt.close()
print("Chart 3 saved: revenue_by_region.png")

# --- Chart 4: Billing Status Breakdown ---
billing = df['BillingStatus'].value_counts().reset_index()
billing.columns = ['BillingStatus', 'Count']

plt.figure(figsize=(6, 6))
plt.pie(billing['Count'], labels=billing['BillingStatus'],
        autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c', '#f39c12'],
        startangle=140)
plt.title('Billing Status Breakdown', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('visuals/billing_status.png')
plt.close()
print("Chart 4 saved: billing_status.png")

# --- Chart 5: Ticket Closure Rate by Region ---
ticket = df.groupby('Region').agg(
    TotalTickets  = ('DaysToClose', 'count'),
    ClosedWithin7 = ('ClosedWithin7', 'sum')
).reset_index()
ticket['ClosureRate'] = (ticket['ClosedWithin7'] / ticket['TotalTickets'] * 100).round(1)

plt.figure(figsize=(8, 5))
sns.barplot(data=ticket, x='Region', y='ClosureRate', palette='Oranges_d')
plt.axhline(y=70, color='red', linestyle='--', label='Target: 70%')
plt.title('Ticket Closure Rate Within 7 Days by Region', fontsize=14, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Closure Rate (%)')
plt.legend()
plt.tight_layout()
plt.savefig('visuals/ticket_closure_rate.png')
plt.close()
print("Chart 5 saved: ticket_closure_rate.png")

print("\nAll charts saved to visuals/ folder!")