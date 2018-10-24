# 125 Accounts

125 Accounts is a simple accounts package for self-employed service providers
in the UK.

The name refers to a sketch in Monty Python and the Holy Grail where King Arthur
attempts to count to three. Hopefully this software will be more reliable at
counting.

## Dependencies

 * Python 3.x (development is done in 3.5.x). Python 2 is not supported and is
 unlikely to work, even with major modifications. This is intentional.
 * [PyYAML](http://pyyaml.org/)
 * [Jinja2](http://jinja.pocoo.org/)
 * [WeasyPrint](http://weasyprint.org/)

## Known limitations

There are a few known limitations with the software as it currently stands.

* The tax brackets only go up to £150,000.
* The personal allowance (effectively a 0% tax rate) doesn't take into account the tapering for incomes over £100,000.
* No support for VAT or other taxes.
