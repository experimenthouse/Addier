# Addier

A Python-based double-entry accounting system

## Introduction

Addier is a Python script that uses accounting information stored in YAML files to produce a balance sheet, profit and loss statement, journal, and individual journal entry pages in HTML format.

It was inspired by the lack of decent free _and_ open-source options. Many of the existing solutions are outdated, difficult to use, not cross-platform, or simply not free and open-source.

By contrast, Addier aims to be simple to use and free and open-source. It also encourages corporate transparency by making it easy to publish the resulting accounts.

## Structure

Addier has the following directory structure:

```
| - addier.py
| - config.yaml
| - journal
    | - YYYY-MM-DD-*.yaml
| - style.css
| - templates
    | - entry.html
    | - footer.html
    | - header.html
    | - journal.html
    | - summary.html
```

## Running the script

Change into the directory and run `python3 addier.py` to see it in action. A directory called `accounts` will be created in the same directory containing:

- `summary.html` — the accounts summary (balance sheet, profit and loss statement)
- `journal.html` — a list of all journal entries
- `entries/*.html` — a file for each journal entry

## Configuration

The `config.yaml` file stores the account settings. The structure of the file is thus:

```
business_name: # the name of the business
business_information: # a place to store business information such as registration numbers
  - # each line of business information gets a separate list item
base_url: # the base URL for where the accounts will be uploaded
functional_currency: # the ISO 4217 code of the currency in which the accounts are to be prepared
accounts: # each account is a separate list item that specifies the name and type of account
  -
    name: # the name of the account
    type: # 'Asset', 'Liability', 'Income', 'Expense' or 'Equity'
currencies: # which currencies are used
  -
    name: # the name of the currency (eg 'United States dollar')
    code: # the ISO 4217 code of the currency (eg 'USD')
    symbol: # the currency symbol (eg '$')
```

Most of this information is not crucial and Addier should be able to run just fine without it. However, it is _very_ important to ensure that the currency code used for `functional_currency` matches a currency code in the currencies list. ISO 4217 codes are recommended to avoid error.

It is also vital that the name and type of account are specified accurately. The type must be one of the five listed: 'Asset', 'Liability', 'Income', 'Expense' or 'Equity'. The name of the account is used in the journal entries, so make sure it is spelt correctly.

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
```

### note

In some cases a journal entry may benefit from a note. This is optional.
