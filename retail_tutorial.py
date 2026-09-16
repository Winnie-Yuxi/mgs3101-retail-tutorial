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
#1. 2009‑10：541,909rows；2010‑11：519,879rows
#2. InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, Customer ID, Country
#3. InvoiceDate is read as string, need to convert to datetime
#4. An empty Customer ID indicates that the guest has completed the checkout. If the rows with empty Customer IDs are directly deleted, all these genuine transactions will be discarded, and the calculated total sales will be smaller than the actual business sales.

def clean_and_prepare_data(df_2009, df_2010):
    print("\n" + "=" * 70)
    print("STEP 4: CLEAN AND PREPARE DATA")
    print("=" * 70)

    df_combined = pd.concat([df_2009, df_2010], ignore_index=True)
    df_combined.columns = df_combined.columns.str.strip().str.replace(' ', '_')
    print(f"Combined raw records: {len(df_combined):,}")

    is_cancellation = (
        df_combined['Invoice'].astype(str).str.startswith('C') |
        (df_combined['Quantity'] < 0)
    )
    df_cancelled = df_combined[is_cancellation].copy()
    print(f"Cancellation or return rows: {len(df_cancelled):,}")

    df_clean = df_combined[
        (~is_cancellation) &
        (df_combined['Quantity'] > 0) &
        (df_combined['Price'] > 0)
    ].copy()

    df_clean['Is_Registered'] = df_clean['Customer_ID'].notna()
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'], dayfirst=True)
    df_clean['Revenue'] = df_clean['Quantity'] * df_clean['Price']

    print(f"Valid completed sales: {len(df_clean):,}")
    print(f"Guest checkout rows retained: {(~df_clean['Is_Registered']).sum():,}")
    print(f"Net revenue: ${df_clean['Revenue'].sum():,.2f}")

    return df_clean, df_cancelled
#1. ~ in the "is_cancellation" section represents the negation operation, keeping the rows that are not cancellations / returns
#2. Quantity > 0 excludes returns; Price > 0 excludes the 0-yuan free records to ensure that all are actual sales.
#3. If negative refund rows are mixed in, the total revenue will be negatively deducted, resulting in incorrect revenue statistics.
#4. .copy() creates an independent copy to avoid the "SettingWithCopyWarning" warning when making subsequent modifications and to prevent modifying the original parent data.

def make_recommendations(df_clean, df_cancelled):
    print("\n" + "=" * 70)
    print("STEP 5: THREE DATA‑BACKED RECOMMENDATIONS")
    print("=" * 70)

    total_revenue = df_clean['Revenue'].sum()
    guest_revenue = df_clean.loc[~df_clean['Is_Registered'], 'Revenue'].sum()
    guest_share = guest_revenue / total_revenue * 100
    return_rate = len(df_cancelled) / (len(df_clean) + len(df_cancelled)) * 100

    print(
        f"1. Guest checkout conversion: Guest sales generated ${guest_revenue:,.2f} "
        f"({guest_share:.1f}% of clean revenue). Offer a registration incentive "
        "after checkout to capture customer information for follow‑up marketing."
    )
    print(
        f"2. Return monitoring: {len(df_cancelled):,} rows ({return_rate:.1f}% of "
        "all raw transactions) were cancellations or returns. Review frequent "
        "returns to identify potential product or fulfillment problems."
    )
    print(
        f"3. Revenue protection: Clean sales total ${total_revenue:,.2f}. Keep the "
        "positive‑quantity and positive‑price checks in future reports so zero‑price "
        "or negative transactions do not distort revenue."
    )

def main():
    print("MGS 3101 RETAIL PANDAS TUTORIAL")
    demo_pandas_fundamentals()
    df_2009, df_2010 = load_and_inspect_data()
    df_clean, df_cancelled = clean_and_prepare_data(df_2009, df_2010)
    make_recommendations(df_clean, df_cancelled)


if __name__ == '__main__':
    main()    