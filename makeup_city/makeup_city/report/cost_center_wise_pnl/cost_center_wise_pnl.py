# Copyright (c) 2023, Mohammad Ali and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

from erpnext.accounts.report.financial_statements import (
	get_filtered_list_for_consolidated_report,
	get_period_list,
	filter_accounts,
	get_appropriate_currency,
	calculate_values,
	accumulate_values_into_parents,
	prepare_data,
	filter_out_zero_value_rows,
	get_accounts
)
from makeup_city.makeup_city.report.financial_statements import set_gl_entries_by_account


def execute(filters=None):
	period_list = get_period_list(
		filters.from_fiscal_year,
		filters.to_fiscal_year,
		filters.period_start_date,
		filters.period_end_date,
		filters.filter_based_on,
		filters.periodicity,
		company=filters.company,
	)
	filters_copy = filters.copy()

	income = get_data(
		filters.company,
		"Income",
		"Credit",
		period_list,
		filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)

	expense = get_data(
		filters.company,
		"Expense",
		"Debit",
		period_list,
		filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)

	net_profit_loss = get_net_profit_loss(
		income, expense, period_list, filters.company, filters.presentation_currency
	)

	data = []
	data.extend(income or [])
	data.extend(expense or [])
	if net_profit_loss:
		data.append(net_profit_loss)

	columns = get_columns(filters_copy)

	data = get_total_by_cost_center(data, filters_copy)
	# chart = get_chart_data(filters, columns, income, expense, net_profit_loss)
	#
	# currency = filters.presentation_currency or frappe.get_cached_value(
	# 	"Company", filters.company, "default_currency"
	# )
	# report_summary = get_report_summary(
	# 	period_list, filters.periodicity, income, expense, net_profit_loss, currency, filters
	# )

	return columns, data #, None, chart, report_summary


def get_data(
	company,
	root_type,
	balance_must_be,
	period_list,
	filters=None,
	accumulated_values=1,
	only_current_fiscal_year=True,
	ignore_closing_entries=False,
	ignore_accumulated_values_for_fy=False,
	total=True,
):

	accounts = get_accounts(company, root_type)
	if not accounts:
		return None

	accounts, accounts_by_name, parent_children_map = filter_accounts(accounts)

	company_currency = get_appropriate_currency(company, filters)

	gl_entries_by_account = {}
	for root in frappe.db.sql(
		"""select lft, rgt from tabAccount
			where root_type=%s and ifnull(parent_account, '') = ''""",
		root_type,
		as_dict=1,
	):

		set_gl_entries_by_account(
			company,
			period_list[0]["year_start_date"] if only_current_fiscal_year else None,
			period_list[-1]["to_date"],
			root.lft,
			root.rgt,
			filters,
			gl_entries_by_account,
			ignore_closing_entries=ignore_closing_entries,
		)

	calculate_values(
		accounts_by_name,
		gl_entries_by_account,
		period_list,
		accumulated_values,
		ignore_accumulated_values_for_fy,
	)
	accumulate_values_into_parents(accounts, accounts_by_name, period_list)
	out = prepare_data(accounts, balance_must_be, period_list, company_currency)
	out = filter_out_zero_value_rows(out, parent_children_map)

	if out and total:
		add_total_row(out, root_type, balance_must_be, period_list, company_currency)

	return out


def add_total_row(out, root_type, balance_must_be, period_list, company_currency):
	total_row = {
		"account_name": _("Total {0} ({1})").format(_(root_type), _(balance_must_be)),
		"account": _("Total {0} ({1})").format(_(root_type), _(balance_must_be)),
		"currency": company_currency,
		"opening_balance": 0.0,
		"total_row": 0,
		"root_type": root_type
	}

	for row in out:
		if not row.get("parent_account"):
			for period in period_list:
				total_row.setdefault(period.key, 0.0)
				total_row[period.key] += row.get(period.key, 0.0)
				row[period.key] = row.get(period.key, 0.0)

			total_row.setdefault("total", 0.0)
			total_row["total"] += flt(row["total"])
			total_row["opening_balance"] += row["opening_balance"]
			row["total"] = ""

	if "total" in total_row:
		total_row['total_row'] = 1
		out.append(total_row)

		# blank row after Total
		out.append({})


def get_total_by_cost_center(data, filters):
	account_list = []
	gl_entries = []
	for d in data:
		if d.get('account') and frappe.db.exists('Account', {'name': d.get('account'), 'is_group': 0}):
			account_list.append(d.get('account'))

	if account_list:
		additional_conditions = [
			"ifnull(gle.voucher_type, '')!='Period Closing Voucher' and ifnull(gle.cost_center, '')!=''"]

		if filters.period_start_date:
			additional_conditions.append("gle.posting_date >= %(from_date)s")

		additional_conditions.append("gle.account in ({})".format(", ".join(frappe.db.escape(d) for d in account_list)))
		additional_conditions = " and {}".format(" and ".join(additional_conditions)) if additional_conditions else ""

		gl_filters = {
			"company": filters.company,
			"from_date": filters.period_start_date,
			"to_date": filters.period_end_date,
		}

		gl_entries = frappe.db.sql(
			"""
			select acct.root_type, gle.name, gle.posting_date, gle.account, gle.debit, gle.credit, gle.cost_center, gle.is_opening, gle.fiscal_year,
				gle.debit_in_account_currency, gle.credit_in_account_currency, gle.account_currency from `tabGL Entry` as gle inner join `tabAccount` acct on gle.account = acct.name
			where gle.company=%(company)s
			{additional_conditions}
			and gle.posting_date <= %(to_date)s
			and gle.is_cancelled = 0""".format(
				additional_conditions=additional_conditions
			),
			gl_filters,
			as_dict=True
		)

	account_list_total_by_cost_center = frappe._dict()
	cost_center_income_expense_total = frappe._dict()
	for entry in gl_entries:
		account_list_total_by_cost_center.setdefault(entry.account, {}).setdefault(entry.cost_center, 0.0)
		cost_center_income_expense_total.setdefault(entry.root_type, {}).setdefault(entry.cost_center, 0.0)
		if entry.root_type == 'Expense':
			account_list_total_by_cost_center[entry.account][entry.cost_center] += flt(entry.debit) - flt(entry.credit)
			cost_center_income_expense_total[entry.root_type][entry.cost_center] += flt(entry.debit) - flt(entry.credit)
		else:
			account_list_total_by_cost_center[entry.account][entry.cost_center] += flt(entry.credit)- flt(entry.debit)
			cost_center_income_expense_total[entry.root_type][entry.cost_center] += flt(entry.credit)- flt(entry.debit)

	for d in data:
		if d.get('account') and frappe.db.exists('Account', {'name': d.get('account'), 'is_group': 0}):
			for account, cost_centers in account_list_total_by_cost_center.items():
				if d.get('account') == account:
					for cost_center, amount in cost_centers.items():
						d[cost_center] = amount
						cost_center_perc = "{0}_perc".format(frappe.scrub(cost_center))
						d[cost_center_perc] = flt((amount / d.get('total')) * 100, precision=2) if d.get('total') else None
						

	lft, rgt = frappe.get_value("Cost Center", filters.get("cost_center"), ["lft", "rgt"])
	cost_center_filters = {
		"company": filters.get("company"),
		"lft": [">=", lft],
		"rgt": ["<=", rgt],
		"is_group": 0
	}

	cost_centers = frappe.get_all("Cost Center", filters=cost_center_filters, fields=["name"], order_by="name")

	for d in data:
		if d.get('total_row') and d.get('root_type'):
			for cst_cntr in cost_centers:
				cst_cntr = cst_cntr.get('name')
				d[cst_cntr] = flt(cost_center_income_expense_total.get(d.get('root_type')).get(cst_cntr))

		if d.get('profit_row'):
			for cst_cntr in cost_centers:
				cst_cntr = cst_cntr.get('name')
				if cost_center_income_expense_total.get('Income') and cost_center_income_expense_total.get('Expense'):
					d[cst_cntr] = flt(cost_center_income_expense_total.get('Income').get(cst_cntr)) - flt(cost_center_income_expense_total.get('Expense').get(cst_cntr))

	return data

def get_columns(filters):
	columns = [
		{
			"fieldname": "account",
			"label": _("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 300,
		}
	]

	lft, rgt = frappe.get_value("Cost Center", filters.get("cost_center"), ["lft", "rgt"])
	cost_center_filters = {
		"company": filters.get("company"),
		"lft": [">=", lft],
		"rgt": ["<=", rgt],
		"is_group": 0
	}

	cost_centers = frappe.get_all("Cost Center", filters=cost_center_filters, fields=["name"], order_by="name")
	for cs in cost_centers:
		columns.append(
			{
				"fieldname": cs.name,
				"label": cs.name,
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150
			}
		)
		columns.append(
			{
				"fieldname": "{0}_perc".format(frappe.scrub(cs.name)),
				"label": "% age",
				"fieldtype": "Percentage",
				"width": 80
			}
		)

	columns.append(
		{
			"fieldname": "total",
			"label": _("Total"),
			"fieldtype": "Currency",
			"width": 150
		}
	)

	return columns


def get_report_summary(
	period_list, periodicity, income, expense, net_profit_loss, currency, filters, consolidated=False
):
	net_income, net_expense, net_profit = 0.0, 0.0, 0.0

	# from consolidated financial statement
	if filters.get("accumulated_in_group_company"):
		period_list = get_filtered_list_for_consolidated_report(filters, period_list)

	for period in period_list:
		key = period if consolidated else period.key
		if income:
			net_income += income[-2].get(key)
		if expense:
			net_expense += expense[-2].get(key)
		if net_profit_loss:
			net_profit += net_profit_loss.get(key)

	if len(period_list) == 1 and periodicity == "Yearly":
		profit_label = _("Profit This Year")
		income_label = _("Total Income This Year")
		expense_label = _("Total Expense This Year")
	else:
		profit_label = _("Net Profit")
		income_label = _("Total Income")
		expense_label = _("Total Expense")

	return [
		{"value": net_income, "label": income_label, "datatype": "Currency", "currency": currency},
		{"type": "separator", "value": "-"},
		{"value": net_expense, "label": expense_label, "datatype": "Currency", "currency": currency},
		{"type": "separator", "value": "=", "color": "blue"},
		{
			"value": net_profit,
			"indicator": "Green" if net_profit > 0 else "Red",
			"label": profit_label,
			"datatype": "Currency",
			"currency": currency,
		},
	]


def get_net_profit_loss(income, expense, period_list, company, currency=None, consolidated=False):
	total = 0
	net_profit_loss = {
		"account_name": "'" + _("Profit for the year") + "'",
		"account": "'" + _("Profit for the year") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value("Company", company, "default_currency"),
		"profit_row": 1
	}

	has_value = False

	for period in period_list:
		key = period if consolidated else period.key
		total_income = flt(income[-2][key], 3) if income else 0
		total_expense = flt(expense[-2][key], 3) if expense else 0

		net_profit_loss[key] = total_income - total_expense

		if net_profit_loss[key]:
			has_value = True

		total += flt(net_profit_loss[key])
		net_profit_loss["total"] = total

	if has_value:
		has_value
		return net_profit_loss


def get_chart_data(filters, columns, income, expense, net_profit_loss):
	labels = [d.get("label") for d in columns[2:]]

	income_data, expense_data, net_profit = [], [], []

	for p in columns[2:]:
		if income:
			income_data.append(income[-2].get(p.get("fieldname")))
		if expense:
			expense_data.append(expense[-2].get(p.get("fieldname")))
		if net_profit_loss:
			net_profit.append(net_profit_loss.get(p.get("fieldname")))

	datasets = []
	if income_data:
		datasets.append({"name": _("Income"), "values": income_data})
	if expense_data:
		datasets.append({"name": _("Expense"), "values": expense_data})
	if net_profit:
		datasets.append({"name": _("Net Profit/Loss"), "values": net_profit})

	chart = {"data": {"labels": labels, "datasets": datasets}}

	if not filters.accumulated_values:
		chart["type"] = "bar"
	else:
		chart["type"] = "line"

	chart["fieldtype"] = "Currency"

	return chart
