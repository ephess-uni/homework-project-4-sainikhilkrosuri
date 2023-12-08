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
   late_fees = defaultdict(float)
   with open(infile, 'r') as file:
      reader = DictReader(file)
      for row in reader:
         if 'return_date' in row:
            patron_id = row['patron_id']
            return_date = row['return_date']

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

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
