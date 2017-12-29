# -*- coding: utf-8 -*-

import yaml
import os
import datetime

if not os.path.exists("accounts"):
    os.makedirs("accounts")
if not os.path.exists("accounts/entries"):
    os.makedirs("accounts/entries")

pages = [
  {
    "name": "Summary of Accounts",
    "short": "Summary",
    "url": "summary.html"
  },
  {
    "name": "Journal",
    "short": "Journal",
    "url": "journal.html"
  }
]

page_links = ""

for page in pages:
    page_links += (
        "<a class='page-link' href='../{0}'>{1}</a>"
        .format(page["url"], page["short"]))

with open("config.yaml", "r") as config_file:
    config = yaml.load(config_file)

for currency in config["currencies"]:
    if currency["code"] == config["functional_currency"]:
        func_cur_name = currency["name"]
        func_cur_code = currency["code"]
        func_cur_symb = currency["symbol"]

business_name = config["business_name"]
business_information = ""

for line in config["business_information"]:
    business_information += line + "<br>\n"

header = open("templates/header.html").read()
header = header.replace("{ business_name }", business_name)
header = header.replace(
    "{ business_information }",
    business_information)
header = header.replace("{ functional_currency }", func_cur_name)
footer = open("templates/footer.html").read()

account_types = {
    "Asset": [],
    "Liability": [],
    "Income": [],
    "Expense": [],
    "Equity": []
}

account_values = {}

for account in config["accounts"]:
    account_types[account["type"]].append(account["name"])
    account_values[account["name"]] = 0

journal_entries = ""
journal_row_head = (
    "<tbody class='entry-row'>"
        "<tr>"
            "<td rowspan='{0}'>{1}</td>"
            "<td rowspan='{0}'>{2}</td>"
            "<td>{3}</td>{4}{5}{6}"
        "</tr>")
journal_row_dr = "<tr><td>{0}</td>{1}</tr>"
journal_row_cr = "<tr><td class='credit-row'>{0}</td>{1}</tr>"
debit = "<td>{0:,.2f}</td><td></td>"
credit = "<td></td><td class='journal-entry-amount'>{0:,.2f}</td>"
debit_accounts = account_types["Asset"] + account_types["Expense"]
credit_accounts = (
    account_types["Liability"] +
    account_types["Income"] +
    account_types["Equity"])

all_entries = []

for entry_file in os.listdir("journal"):
    if entry_file.endswith(".yaml"):
        all_entries.append(entry_file)

pl_start = (datetime.datetime.strptime(
    all_entries[0][:10], "%Y-%m-%d").strftime(
        "%A %d %B %Y").lstrip("0").replace(" 0", " "))

pl_end = (datetime.datetime.strptime(
    all_entries[-1][:10], "%Y-%m-%d").strftime(
        "%A %d %B %Y").lstrip("0").replace(" 0", " "))

for entry_file in os.listdir("journal"):
    journal_entry = ""
    if entry_file.endswith(tuple([".yml", ".yaml"])):
        entry_url = "entries/" + entry_file.rsplit('.', 1)[0] + ".html"
        with open("journal/" + entry_file, "r") as journal_file:
            entry = yaml.load(journal_file)
        debit_total = 0
        credit_total = 0
        for account in entry["debit"]:
            debit_total += account["amount"]
        for account in entry["credit"]:
            credit_total += account["amount"]
        for account in entry["debit"]:
            journal_row_amount = debit.format(account["amount"])
            if entry["debit"].index(account) == 0:
                rowspan = str(len(entry["debit"] + entry["credit"]))
                balance_check = "<td rowspan='{0}' class='{1}'>{2}</td>"
                if debit_total == credit_total:
                    balance_check = balance_check.format(
                        rowspan,
                        "balanced",
                        "Balanced")
                else:
                    balance_check = balance_check.format(
                        rowspan,
                        "unbalanced",
                        "Unbalanced")
                entry_link = (
                    "<td rowspan='{0}'>"
                        "<a href='{1}'>View</a>"
                    "</td>".format(rowspan, entry_url))
                journal_entry += journal_row_head.format(
                    rowspan,
                    entry["date"],
                    entry["narration"],
                    account["account"],
                    journal_row_amount,
                    balance_check,
                    entry_link)
            else:
                journal_entry += journal_row_dr.format(
                    account["account"],
                    journal_row_amount)
            if account["account"] in debit_accounts:
                account_values[account["account"]] += account["amount"]
            elif account["account"] in credit_accounts:
                account_values[account["account"]] -= account["amount"]
        for account in entry["credit"]:
            journal_row_amount = credit.format(account["amount"])
            journal_entry += journal_row_cr.format(
                account["account"],
                journal_row_amount)
            if account["account"] in debit_accounts:
                account_values[account["account"]] -= account["amount"]
            elif account["account"] in credit_accounts:
                account_values[account["account"]] += account["amount"]
        journal_entry += "</tbody>"
        journal_entries += journal_entry
        entry_date = datetime.datetime.strptime(
            "2018-01-01", "%Y-%m-%d").strftime(
                "%A %d %B %Y").lstrip("0").replace(" 0", " ")
        entry_page = open("templates/entry.html").read()
        entry_page = entry_page.replace("{ header }", header)
        entry_page = entry_page.replace(
            "{ page_name }",
            entry["narration"] + " (%s)" % entry_date)
        entry_page = entry_page.replace("{ journal_entry }", journal_entry.replace(entry_link, ""))
        if "note" in entry:
            entry_page = entry_page.replace(
                "{ entry_note }",
                "<p><strong>Note: </strong>%s</p>" % entry["note"])
        else:
            entry_page = entry_page.replace("{ entry_note }", "")
        entry_page = entry_page.replace("{ page_links }", page_links)
        entry_page = entry_page.replace("{ footer }", footer)
        open("accounts/" + entry_url, "w").write(entry_page)

account_tables = {
    "Asset": "",
    "Liability": "",
    "Income": "",
    "Expense": "",
    "Equity": ""
}
account_totals = {
    "Asset": 0,
    "Liability": 0,
    "Income": 0,
    "Expense": 0,
    "Equity": 0
}
account_header = (
    "<tr class='header-row'>"
        "<th>{0}</th>"
        "<th class='symb-cell'>{1}</th>"
        "<th>{2:,.2f}</th>"
    "</tr>")
account_row = (
    "<tr>"
        "<td>{0}</td>"
        "<td class='symb-cell'>{1}</td>"
        "<td>{2:,.2f}</td>"
    "</tr>")

for account in config["accounts"]:
    name = account["name"]
    symb = func_cur_symb
    value = account_values[account["name"]]
    account_tables[account["type"]] += account_row.format(
        name,
        symb,
        value)
    account_totals[account["type"]] += value

retained_earnings = (
    account_totals["Asset"] -
    account_totals["Liability"])

balance_sheet = account_header.format(
    "Assets",
    func_cur_symb,
    account_totals["Asset"])
balance_sheet += account_tables["Asset"]

balance_sheet += account_header.format(
    "Liabilities",
    func_cur_symb,
    account_totals["Liability"])
balance_sheet += account_tables["Liability"]

balance_sheet += account_header.format(
    "Equity",
    func_cur_symb,
    (account_totals["Equity"] + retained_earnings))
balance_sheet += account_tables["Equity"]

balance_sheet += account_row.format(
    "Retained earnings",
    func_cur_symb,
    retained_earnings)

profit = account_totals["Income"] - account_totals["Expense"]

pl_statement = account_header.format(
    "Income",
    func_cur_symb,
    account_totals["Income"])
pl_statement += account_tables["Income"]

pl_statement += account_header.format(
    "Expenses",
    func_cur_symb,
    account_totals["Expense"])
pl_statement += account_tables["Expense"]

pl_statement += account_header.format(
    "Profit",
    func_cur_symb,
    profit)

now = datetime.datetime.now().strftime(
    "%A %d %B %Y").lstrip("0").replace(" 0", " ")

for page in pages:
    page_links = ""
    for _page in pages:
        page_links += "<a class='page-link"
        if page["name"] == _page["name"]:
            page_links += " current-page"
        page_links += "' href='{0}'>{1}</a>".format(_page["url"], _page["short"])
    output = open("templates/" + page["url"]).read()
    output = output.replace("{ header }", header)
    output = output.replace("{ page_name }", page["name"])
    output = output.replace("{ page_links }", page_links)
    output = output.replace("{ footer }", footer)
    output = output.replace("{ current_date }", now)
    output = output.replace("{ pl_start }", pl_start)
    output = output.replace("{ pl_end }", pl_end)
    output = output.replace("{ balance_sheet }", balance_sheet)
    output = output.replace("{ pl_statement }", pl_statement)
    output = output.replace("{ journal_entries }", journal_entries)
    open("accounts/" + page["url"], "w").write(output)
