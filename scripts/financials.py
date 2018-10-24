#!/usr/bin/env python3

import argparse
import yaml
import pathlib
import decimal
import datetime
import os

decimal.getcontext().prec = 10

parser = argparse.ArgumentParser()
parser.add_argument('--data', help='path to data directory', required=True)
args = parser.parse_args()

script_path = os.path.dirname(os.path.realpath(__file__))
config_path = script_path + '/../config'

# Configuration
config = {}
with open(config_path + '/tax.yaml') as f:
  config['tax'] = yaml.safe_load(f.read())

# Find current tax year
today = datetime.date.today()
config['current_tax'] = next(x for x in config['tax'] if x['start_date'] <= today and x['end_date'] >= today)

# Data
total_sales = decimal.Decimal(0.00)
total_payments = decimal.Decimal(0.00)

data_directory = str(args.data)
data_path = pathlib.Path(data_directory)
invoice_files = list(data_path.glob('data/invoices/*.yaml'))

for invoice_file in invoice_files:
    fp = invoice_file.open()
    invoice_data = yaml.safe_load(fp.read())
    fp.close()

    if invoice_data['issue_date'] >= config['current_tax']['start_date'] and invoice_data['issue_date'] <= config['current_tax']['end_date'] and invoice_data['issue_date'] <= today:
        print(invoice_data['number'])

        total_sales += decimal.Decimal(invoice_data['total'])

        print(invoice_data['total'])

        # Subtract any payments from accounts receivable
        if 'payments' in invoice_data:
            for payment in invoice_data['payments']:
                print(payment['amount'])
                total_payments += decimal.Decimal(payment['amount'])

        print()

print("Total sales: %.2f" % total_sales)
print("Total payments: %.2f" % total_payments)

# Calculate tax and national insurance
