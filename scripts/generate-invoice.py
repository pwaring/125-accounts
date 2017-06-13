#!/usr/bin/env python3

import argparse
import decimal
import sys

import yaml
import jinja2
import weasyprint

decimal.getcontext().prec = 2

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
# Invoice items must sum to total
invoice_items_total = decimal.Decimal(0.00)
for item in invoice_data['items']:
    invoice_items_total += decimal.Decimal(item['cost'])

invoice_total = decimal.Decimal(invoice_data['total'])

if invoice_total != invoice_items_total:
    invoice_total = '{0:f}'.format(invoice_total)
    invoice_items_total = '{0:f}'.format(invoice_items_total)
    print("Invoice total (" + invoice_total + ") does not equal sum of items (" + invoice_items_total + ")")
    sys.exit(1)

template_environment = jinja2.Environment(loader = jinja2.FileSystemLoader('../templates/'))
template = template_environment.get_template('invoice.html')
html_data = template.render(supplier = supplier_data, invoice = invoice_data, client = client_data)

weasyprint.HTML(string = html_data).write_pdf(data_directory + 'output/invoices/' + invoice_number + '.pdf')
