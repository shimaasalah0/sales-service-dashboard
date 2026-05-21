
import pandas as pd

# --- Load Cleaned Data ---
df = pd.read_csv('data/cleaned_data.csv')

# Fix date types
df['OrderDate']       = pd.to_datetime(df['OrderDate'])
df['TicketOpenDate']  = pd.to_datetime(df['TicketOpenDate'])
df['TicketCloseDate'] = pd.to_datetime(df['TicketCloseDate'])

# --- Pivot 1: Monthly Revenue ---
monthly_revenue = df.groupby(df['OrderDate'].dt.to_period('M'))['Revenue'].sum().reset_index()
monthly_revenue.columns = ['Month', 'TotalRevenue']
monthly_revenue['Month'] = monthly_revenue['Month'].astype(str)

# --- Pivot 2: Revenue by Category ---
category_revenue = df.groupby('Category')['Revenue'].sum().reset_index()
category_revenue.columns = ['Category', 'TotalRevenue']

# --- Pivot 3: Revenue by Region ---
region_revenue = df.groupby('Region')['Revenue'].sum().reset_index()
region_revenue.columns = ['Region', 'TotalRevenue']

# --- Pivot 4: Billing Status Summary ---
billing_summary = df['BillingStatus'].value_counts().reset_index()
billing_summary.columns = ['BillingStatus', 'Count']

# --- Pivot 5: Ticket Closure by Region ---
ticket_summary = df.groupby('Region').agg(
    TotalTickets   = ('DaysToClose', 'count'),
    ClosedWithin7  = ('ClosedWithin7', 'sum'),
    AvgDaysToClose = ('DaysToClose', 'mean')
).reset_index()
ticket_summary['ClosureRate%'] = (ticket_summary['ClosedWithin7'] / ticket_summary['TotalTickets'] * 100).round(1)

# --- Write to Excel ---
try:
    with pd.ExcelWriter('excel/service_dashboard.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer,               sheet_name='Raw Data',        index=False)
        monthly_revenue.to_excel(writer,  sheet_name='Monthly Revenue', index=False)
        category_revenue.to_excel(writer, sheet_name='By Category',     index=False)
        region_revenue.to_excel(writer,   sheet_name='By Region',       index=False)
        billing_summary.to_excel(writer,  sheet_name='Billing Status',  index=False)
        ticket_summary.to_excel(writer,   sheet_name='Ticket Closure',  index=False)
    print("Excel file created successfully!")
except Exception as e:
    print(f"ERROR: {e}")