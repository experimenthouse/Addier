# Addier

A Python-based double-entry accounting system

## Introduction

Addier uses accounting information stored in YAML files and processed by a Python script to compile a balance sheet, profit and loss statement, list of journal entries, and individual entry pages in HTML format.

## Setting up

The repository consists of:

- `addier.py` — the script
- `config.yaml` - an example config file
- `journal/2018-01-01-entry.yaml` — an example journal entry
- `templates/*.html` — the template files for the accounts

Also included is the directory `example`, which contains a more detailed `config.yaml` and journal entries for a better example.

## Running the script

Change into the directory and run `python3 addier.py` to see it in action. A directory called `accounts` will be created in the same directory containing:

- `summary.html` — the accounts summary (balance sheet, profit and loss statement)
- `journal.html` — a list of all journal entries
- `entries/*.html` — a file for each journal entry

## Configuration

`config.yaml` can be modified to customise the accounts. This is standard YAML and should be self-explanatory for the most part, but this is outlined below.

### business_name

The name of your business! This will be inserted into every page for a consistent header.

### business_information

Each list item represents a line that will be inserted into every page header. This could be the registration number, telephone number and email address for the business, for example:

```
business_information:
  - "Registration number: 1234567890"
  - "Phone: +1 234 567 890"
  - "Email: example@example.com"
```

### functional_currency

The currency used for the accounts, in code form. It is recommended that [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) codes be used. This code must correspond with a currency in the config file (see below).

It is planned to have a separate option to compile accounts in a different currency for filing. Some businesses may use one currency as their functional currency, but be required to file annual accounts in a different currency (eg a British business that uses United States Dollars, but is required to file in Pounds Sterling).

### accounts

A list of accounts with names and types. The name is arbitrary, but must be used consistently between the config file and the journal entries. No check is performed on this, but it is planned. The account type must be either "Asset", "Liability", "Income", "Expense" or "Equity". Read up on accounting practices to determine which accounts should be which. The format is:

```
accounts:
  -
    name: 
    type:
   -
    name: 
    type:
 ```
 
### currencies
 
A list of currencies. Support for multiple currencies is planned, but for now just one is required. A name, code and symbol is required (eg "Australian Dollar", "AUD", and "$"). As above, it is recommended that the ISO 4217 code be used. The currency list is in the following format:

```
currencies:
  -
    name:
    code:
    symbol:
```

## Journal entries

Separate YAML files (.yaml) are required for each journal entry. These should be in the file name format `YYYY-MM-DD-name.yaml`. The journal entries have a date, narration, list of debited accounts, list of credited accounts, and an optional note.

### date

Use the YYYY-MM-DD format for the date.

### narration

This is a brief description of the journal entry. This could be something like "Wages paid".

### debit and credit

`debit` and `credit` are lists of accounts to be debited or credited, including account name and amount. It may be tempting to think of each entry as including a "from" and "to" component, but the reality is much more complicated:

- asset accounts are debited when increased, and credited when decreased
- liability accounts are credited when increased, and debited when decreased
- income accounts are debited when increased, and credited when decreased
- expense accounts are credited when increased, and debited when decreased
- equity accounts are credited when increased, and debited when decreased

Two or more accounts may be increased or decreased, credited or debited at the same time, so long as they are balanced. The below is an example of a business receiving partial payment for sale of goods. Both the sales revenue account (income) _and_ cash account (asset) are increased, but the sales revenue is credited and the cash account is debited. Also included is the decrease (credit) in the inventory account (asset), the increase (debit) in accounts receivable account (asset), and the increase (debit) in the cost of goods sold account (expense). Note that the entry balances for a total of 250.00 in both debits and credits.

```
debit:
  -
    account: Cash
    amount: 100.00
  -
    account: Accounts receivable
    amount: 50.00
  -
    account: Cost of goods sold
    amount: 100.00
credit:
  -
    account: Inventory
    amount: 150.00
  -
    account: Sales revenue
    amount: 100.00
    
### note

In some cases a journal entry may benefit from a note. This is optional.
