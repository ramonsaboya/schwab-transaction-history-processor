import re

def process_transactions(
  pages,
  page_string,
  page_continued_string,
  table_header_string,
  get_transaction_from_entry_func
):
  page_amount = len(pages)

  transactions = []

  idx = 0
  while idx < page_amount:
    page = pages[idx]
    raw_page_text = re.sub(r" +", " ", page.extract_text(extraction_mode="layout"))
    if page_string in raw_page_text:
      page_text = raw_page_text.split(page_string)[1]
      transactions = get_transactions_from_page(page_text, table_header_string, get_transaction_from_entry_func)
      break
    idx += 1
  
  idx += 1
  while idx < page_amount:
    continued_page = pages[idx]
    raw_page_text = re.sub(r" +", " ", continued_page.extract_text(extraction_mode="layout"))
    if page_continued_string in raw_page_text:
      page_text = raw_page_text.split(page_continued_string)[1]
      transactions.extend(
        get_transactions_from_page(page_text, table_header_string, get_transaction_from_entry_func)
      )
    else:
      break
    idx += 1

  return transactions

def get_transactions_from_page(page_text, table_header_string, get_transaction_from_entry_func):
  table = page_text.split('\n')
  
  header_idx = 0
  while table[header_idx] != table_header_string:
    header_idx += 1
  row_idx = header_idx + 2

  transactions = []

  while row_idx < len(table):
    if table[row_idx].startswith(' Total '):
      break

    if len(table[row_idx].split(' ')) >= 7:
      transactions.append(get_transaction_from_entry_func(table, row_idx))
    row_idx += 1

  return transactions
