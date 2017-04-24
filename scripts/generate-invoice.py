#!/usr/bin/env python3

import argparse
import yaml
import jinja2
import weasyprint

parser = argparse.ArgumentParser(description = 'Generate invoice')
parser.add_argument('invoice_number', type = int, help = 'Invoice number')
args = parser.parse_args()

invoice_number = str(args.invoice_number)

supplier_file = open('../data/supplier.yaml')
supplier_data = yaml.safe_load(supplier_file.read())
supplier_file.close()

invoice_file = open('../data/invoices/' + invoice_number + '.yaml')
invoice_data = yaml.safe_load(invoice_file.read())
invoice_file.close()

# TODO: Validation - does total match sum of items?

client_file = open('../data/clients/' + invoice_data['client'] + '.yaml')
client_data = yaml.safe_load(client_file.read())
client_file.close()

template_environment = jinja2.Environment(loader = jinja2.FileSystemLoader('../templates/'))
template = template_environment.get_template('invoice.html')
html_data = template.render(supplier = supplier_data, invoice = invoice_data, client = client_data)

weasyprint.HTML(string = html_data).write_pdf('../output/invoices/' + invoice_number + '.pdf')
