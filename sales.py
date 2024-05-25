import re

from schwab_pdf_base import process_transactions

def process_sales(pages):
  return process_transactions(
    pages,
    'Transaction Detail - Purchases & Sales',
    'Transaction Detail - Purchases & Sales (continued)',
    'Settle DateTrade Dat Transaction Description Quantity Unit Price Interest Total Amount',
    get_sales_from_entry
  )

def get_sales_from_entry(table, idx):
  values = table[idx].split(' ')

  date_parts = values[1].split('/')
  date = f"{date_parts[2]}/{date_parts[0]}/{date_parts[1]}"
  amount = float(values[-4].replace('(', '').replace(')', ''))
  unit_price = float(values[-3].replace(',', ''))
  fees = float(values[-2].replace(',', ''))
  total = float(values[-1].replace(',', ''))

  return {
    "date": date,
    "type": "S",
    "amount": amount,
    "unit_price": unit_price,
    "fees": fees,
    "total": total
  }
