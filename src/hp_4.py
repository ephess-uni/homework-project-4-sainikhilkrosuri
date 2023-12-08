# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
   new_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_format = date_obj.strftime('%d %b %Y--%d %b %Y')
        new_dates.append(new_format)
    return new_dates


def date_range(start, n):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]


def add_date_range(values, start_date):
    date_values = []
    for value in values:
        date_values.append((start_date, value))
        start_date += timedelta(days=1)
    return date_values


def fees_report(infile, outfile):
    # Define a dictionary to store late fees per patron ID
    late_fees = defaultdict(float)

    # Read the input CSV file using DictReader
    with open(infile, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            patron_id = row['patron_id']
            return_date = row['return_date']
            due_date = row['due_date']

            # Calculate late fees if the book is returned after the due date
            if return_date > due_date:
                # Calculate days late and charge a fee of $0.50 per day
                days_late = (datetime.strptime(return_date, '%Y-%m-%d') - datetime.strptime(due_date, '%Y-%m-%d')).days
                late_fee = days_late * 0.50
                late_fees[patron_id] += late_fee

    # Write the summary report to the output file using DictWriter
    with open(outfile, 'w', newline='') as output_file:
        fieldnames = ['patron_id', 'late_fee']
        writer = DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for patron_id, fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fee': fee})

# The rest of your code remains unchanged


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
