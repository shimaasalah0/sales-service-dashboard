import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# So we get the same data every time we run it
np.random.seed(42)
random.seed(42)

# --- Settings ---
NUM_ROWS = 1000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

# --- Reference Lists ---
regions = ['North', 'South', 'East', 'West']

categories = ['Spare Parts', 'Service Contract', 'Time & Materials', 'Equipment']

products = {
    'Spare Parts':        ['Filter Unit', 'Pump Seal', 'Control Board', 'Valve Kit'],
    'Service Contract':   ['Basic Plan', 'Premium Plan', 'Enterprise Plan'],
    'Time & Materials':   ['On-site Repair', 'Remote Support', 'Inspection Visit'],
    'Equipment':          ['Sensor Unit', 'Motor Assembly', 'Display Panel']
}

billing_statuses = ['Billed', 'Pending', 'Overdue']

# --- Helper: random date between two dates ---
def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# --- Build each row ---
rows = []

for i in range(NUM_ROWS):
    order_id       = f'ORD-{1000 + i}'
    customer_id    = f'CUST-{random.randint(1, 150):03d}'
    region         = random.choice(regions)
    category       = random.choice(categories)
    product        = random.choice(products[category])
    quantity       = random.randint(1, 10)
    unit_price     = round(random.uniform(50, 2000), 2)
    revenue        = round(quantity * unit_price, 2)
    order_date     = random_date(START_DATE, END_DATE)
    billing_status = random.choice(billing_statuses)

    # Ticket open = same as order date
    ticket_open    = order_date
    # Ticket close = 1 to 14 days later (some will exceed 7 days — realistic)
    ticket_close   = ticket_open + timedelta(days=random.randint(1, 14))

    rows.append({
        'OrderID':         order_id,
        'CustomerID':      customer_id,
        'Region':          region,
        'Category':        category,
        'ProductName':     product,
        'Quantity':        quantity,
        'UnitPrice':       unit_price,
        'Revenue':         revenue,
        'OrderDate':       order_date.strftime('%Y-%m-%d'),
        'BillingStatus':   billing_status,
        'TicketOpenDate':  ticket_open.strftime('%Y-%m-%d'),
        'TicketCloseDate': ticket_close.strftime('%Y-%m-%d'),
    })

# --- Create DataFrame ---
df = pd.DataFrame(rows)

# --- Save to CSV ---
df.to_csv('sales_service_data.csv', index=False)

print("Dataset created successfully!")
print(f"Shape: {df.shape}")
print(df.head())