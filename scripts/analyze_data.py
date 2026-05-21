
import pandas as pd
import numpy as np

# --- Load Data ---
df = pd.read_csv('data/sales_service_data.csv')

# --- Basic Inspection ---
print("Shape:", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())

# --- Fix Data Types ---
df['OrderDate']       = pd.to_datetime(df['OrderDate'])
df['TicketOpenDate']  = pd.to_datetime(df['TicketOpenDate'])
df['TicketCloseDate'] = pd.to_datetime(df['TicketCloseDate'])

# --- Engineer New Features ---
df['Month']          = df['OrderDate'].dt.to_period('M')
df['DaysToClose']    = (df['TicketCloseDate'] - df['TicketOpenDate']).dt.days
df['ClosedWithin7']  = df['DaysToClose'] <= 7

# --- KPI 1: Monthly Revenue ---
monthly_revenue = df.groupby('Month')['Revenue'].sum().reset_index()
monthly_revenue.columns = ['Month', 'TotalRevenue']
print("\nMonthly Revenue:\n", monthly_revenue)

# --- KPI 2: Revenue by Category ---
category_revenue = df.groupby('Category')['Revenue'].sum().reset_index()
category_revenue.columns = ['Category', 'TotalRevenue']
print("\nRevenue by Category:\n", category_revenue)

# --- KPI 3: Revenue by Region ---
region_revenue = df.groupby('Region')['Revenue'].sum().reset_index()
print("\nRevenue by Region:\n", region_revenue)

# --- KPI 4: Billing Status Breakdown ---
billing_summary = df['BillingStatus'].value_counts().reset_index()
billing_summary.columns = ['BillingStatus', 'Count']
print("\nBilling Status:\n", billing_summary)

# --- KPI 5: Ticket Closure Rate within 7 Days ---
closure_rate = df['ClosedWithin7'].mean() * 100
print(f"\nTickets Closed Within 7 Days: {closure_rate:.1f}%")

# --- Save cleaned data ---
df.to_csv('data/cleaned_data.csv', index=False)
print("\nCleaned data saved!")