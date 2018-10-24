#!/usr/bin/env python3

import argparse
import decimal
import sys
import datetime

import yaml
import jinja2
import weasyprint

decimal.getcontext().prec = 10

parser = argparse.ArgumentParser()
parser.add_argument('--data', help='path to data directory', required=True)
parser.add_argument('--number', help='Invoice number', type=int, required=True)
args = parser.parse_args()

data_directory = str(args.data)
invoice_number = str(args.number)

supplier_file = open(data_directory + 'data/supplier.yaml')
supplier_data = yaml.safe_load(supplier_file.read())
supplier_file.close()

invoice_file = open(data_directory + 'data/invoices/' + invoice_number + '.yaml')
invoice_data = yaml.safe_load(invoice_file.read())
invoice_file.close()

client_file = open(data_directory + 'data/clients/' + invoice_data['client'] + '.yaml')
client_data = yaml.safe_load(client_file.read())
client_file.close()

# Validate all data
# Invoice number must match filename
if str(invoice_number) != str(invoice_data['number']):
    sys.exit("Invoice number argument (" + str(invoice_number) + ") does not match invoice number in data (" + str(invoice_data['number']) + ")")

# Invoice items must sum to total
invoice_items_total = decimal.Decimal(0.00)
for item in invoice_data['items']:
    invoice_items_total += decimal.Decimal(item['cost'])

invoice_total = decimal.Decimal(0.00)
invoice_total += decimal.Decimal(invoice_data['total'])

if invoice_total != invoice_items_total:
    invoice_total = '{0:f}'.format(invoice_total)
    invoice_items_total = '{0:f}'.format(invoice_items_total)
    sys.exit("Invoice total (" + invoice_total + ") does not equal sum of items (" + invoice_items_total + ")")

# All validation checks complete, calculate some values which are not always specified
# Calculate due date from credit terms
if 'credit_days' in client_data and 'due_date' not in invoice_data:
    invoice_data['due_date'] = invoice_data['issue_date'] + datetime.timedelta(days = client_data['credit_days'])

template_environment = jinja2.Environment(loader = jinja2.FileSystemLoader('../templates/'))
template = template_environment.get_template('invoice.html')
html_data = template.render(supplier = supplier_data, invoice = invoice_data, client = client_data)

weasyprint.HTML(string = html_data).write_pdf(data_directory + 'output/invoices/' + invoice_number + '.pdf')
