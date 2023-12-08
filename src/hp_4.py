# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
   new_dates = []
   for date_str in old_dates:
      dt = datetime.strptime(date_str, "%Y-%m-%d")
      formatted_date = dt.strftime("%d %b %Y")
      new_dates.append(formatted_date)
   return new_dates


def date_range(start, n):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    date_list = [start_date + timedelta(days=i) for i in range(n)]
    return date_list


def add_date_range(values, start_date):
    date_values = []
    date_list = date_range(start_date, len(values))
    for i, value in enumerate(values):
        date_values.append((date_list[i], value))
    return date_values


def fees_report(infile, outfile):
   late_fees_dict = defaultdict(float)
   with open(infile, 'r') as file:
      reader = DictReader(file)
      for row in reader:
         date_due = datetime.strptime(row['date_due'], "%m/%d/%Y")
         date_returned = datetime.strptime(row['date_returned'], "%m/%d/%Y")
         if date_returned > date_due:
            days_late = (date_returned - date_due).days
            late_fee = round(days_late * 0.25, 2)
            late_fees_dict[row['patron_id']] += late_fee
         else:
            late_fees_dict[row['patron_id']] = 0.00
   with open(outfile, 'w', newline='') as file:
      cols = ['patron_id', 'late_fees']
      late_fees_list = []
      for key, value in late_fees_dict.items():
         late_fees_list.append({'patron_id': key, 'late_fees': "{:.2f}".format(value)})
         writer = DictWriter(file, cols)
         writer.writeheader()
         writer.writerows(late_fees_list)

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
