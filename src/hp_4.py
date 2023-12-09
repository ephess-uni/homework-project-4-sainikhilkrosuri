# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
   new_date = []
   for date_str in old_dates:
      dt = datetime.strptime(date_str, "%Y-%m-%d")
      format_date = dt.strftime("%d %b %Y")
      new_date.append(format_date)
   return new_date


def date_range(start, n):
    st_date = datetime.strptime(start, "%Y-%m-%d")
    list_date = [st_date + timedelta(days=i) for i in range(n)]
    return list_date


def add_date_range(values, start_date):
    date_value_list = []
    date_list = date_range(start_date, len(values))
    for i, value in enumerate(values):
        date_value_list.append((date_list[i], value))
    return date_value_list


def fees_report(infile, outfile):
   late_fee_dict = defaultdict(float)
   with open(infile, 'r') as file:
      reader = DictReader(file)
      for row in reader:
         due_date = datetime.strptime(row['date_due'], "%m/%d/%Y")
         return_date = datetime.strptime(row['date_returned'], "%m/%d/%Y")
         if return_date > due_date:
            late_day = (return_date - due_date).days
            late_fee = round(late_day * 0.25, 2)
            late_fee_dict[row['patron_id']] += late_fee
         else:
            late_fee_dict[row['patron_id']] = 0.00
   with open(outfile, 'w', newline='') as file:
      cols = ['patron_id', 'late_fees']
      late_fee_list = []
      for key, value in late_fee_dict.items():
         late_fee_list.append({'patron_id': key, 'late_fees': "{:.2f}".format(value)})
      writer = DictWriter(file, cols)
      writer.writeheader()
      writer.writerows(late_fee_list)

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
