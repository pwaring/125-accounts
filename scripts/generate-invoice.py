#!/usr/bin/env python3

import argparse
import yaml
import jinja2
import weasyprint

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

template_environment = jinja2.Environment(loader = jinja2.FileSystemLoader('../templates/'))
template = template_environment.get_template('invoice.html')
html_data = template.render(supplier = supplier_data, invoice = invoice_data, client = client_data)

weasyprint.HTML(string = html_data).write_pdf(data_directory + 'output/invoices/' + invoice_number + '.pdf')
