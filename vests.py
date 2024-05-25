import re

from schwab_pdf_base import process_transactions

def process_vests(pages):
  return process_transactions(
    pages,
    'Transaction Detail - Transfers',
    'Transaction Detail - Transfers (continued)',
    'Date Date Transaction Description Quantity Unit Price Total Amount',
    get_vest_from_entry
  )

def get_vest_from_entry(table, idx):
  values = table[idx].split(' ')

  date_parts = values[0].split('/')
  date = f"{date_parts[2]}/{date_parts[0]}/{date_parts[1]}"
  amount = float(values[-3])
  total = float(values[-1].replace(',', ''))
  unit_price = total/amount
  
  return {
    "date": date,
    "type": "B",
    "amount": amount,
    "total": total,
    "fees": 0.0,
    "unit_price": unit_price
  }