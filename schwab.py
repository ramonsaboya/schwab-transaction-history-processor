import argparse
from exchange_rate import get_exchange_rate, load_exchange_rates
from pypdf import PdfReader

from sales import process_sales
from vests import process_vests

import os
import csv

def main(args):
  load_exchange_rates()

  files = os.listdir(args.files)

  pdf_files = [file for file in files if file.lower().endswith('.pdf')]

  transactions = []
  for pdf_file in pdf_files:
    pdf_path = os.path.join(args.files, pdf_file)
    pdf = PdfReader(pdf_path)
    print(f"Processing: {pdf_file}")
    transactions.extend(process_pdf(pdf))

  vest_list, sell_list = [], []
  for transaction in transactions:
    (vest_list, sell_list)[transaction['type'] == 'S'].append(transaction)

  vest_list_by_date = {}
  for vest in vest_list:
    date = vest['date']
    if date in vest_list_by_date:
      vest_list_by_date[date]['amount'] += vest['amount']
    else:
      vest_list_by_date[date] = vest
  vest_list = list(vest_list_by_date.values())

  transactions = vest_list + sell_list
  transactions.sort(key=lambda transaction: (transaction['date'], transaction['type'] != 'buy'))

  for transaction in transactions:
    date_parts = transaction['date'].split('/')
    transaction['date'] = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"

  csv_file = 'transactions.csv'
  with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    for t in transactions:
      exchange_rate = get_exchange_rate(t['date'])
      writer.writerow([
        t['type'],
        t['date'],
        'META',
        round(t['amount'], 2),
        round(t['unit_price']/exchange_rate, 2),
        round(t['fees']/exchange_rate, 2),
        0,
        round(t['unit_price'], 2),
        round(t['fees'], 2)
      ])

def process_pdf(pdf):
  pages = pdf.pages[1:]
  vests = process_vests(pages)
  sales = process_sales(pages)

  return vests + sales

if __name__ == '__main__':
  args = argparse.ArgumentParser()
  args.add_argument('files', type=str, help='Path to the CSV file')
  main(args.parse_args())
