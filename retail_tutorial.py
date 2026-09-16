import pandas as pd

pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda value: f'{value:,.2f}')

def demo_pandas_fundamentals():
    print("\n" + "=" * 70)
    print("STEP 2: PANDAS FUNDAMENTALS")
    print("=" * 70)

    daily_sales = pd.Series(
        [1250.50, 2100.00, 1850.75, 3200.20, 4100.00],
        index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        name='Daily_Sales_USD'
    )
    print("\nDaily sales Series:")
    print(daily_sales)
    print(f"Total weekly sales: ${daily_sales.sum():,.2f}")

    toy_orders = pd.DataFrame({
        'OrderID': [1001, 1002, 1003, 1004],
        'Quantity': [15, 8, 25, 2],
        'UnitPrice': [12.50, 45.00, 12.50, 350.00],
        'CustomerType': ['B2C', 'B2B', 'B2C', 'B2B']
    })
    toy_orders['LineTotal'] = toy_orders['Quantity'] * toy_orders['UnitPrice']
    print("\nOrders with vectorized line totals:")
    print(toy_orders)

    large_b2b_orders = toy_orders[
        (toy_orders['CustomerType'] == 'B2B') &
        (toy_orders['LineTotal'] >= 500)
    ]
    print("\nB2B orders worth $500 or more:")
    print(large_b2b_orders)
#Guided Practice: 1. Friday sales amount:4100.00
#2. OrderID1004：2 * 350.00 = 700.00
#3. OrderID1004(700); Order1002：8*45=360, less than 500
#4. If change to ">=600", Order1004 remains

def load_and_inspect_data():
    print("\n" + "=" * 70)
    print("STEP 3: LOAD AND INSPECT RETAIL DATA")
    print("=" * 70)

    df_2009 = pd.read_csv('Retail 2009-10.csv')
    df_2010 = pd.read_csv('Retail 2010-11.csv')

    print(f"2009-10 records: {len(df_2009):,}")
    print(f"2010-11 records: {len(df_2010):,}")
    print(f"Columns: {df_2009.columns.tolist()}")
    print("\nFirst three rows from 2009-10:")
    print(df_2009.head(3))

    print("\nMissing Customer IDs:")
    print(f"2009-10: {df_2009['Customer ID'].isna().sum():,}")
    print(f"2010-11: {df_2010['Customer ID'].isna().sum():,}")

    return df_2009, df_2010
#