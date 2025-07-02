import frappe
from frappe import _
from frappe.utils import add_days, add_months, cint, cstr, flt, formatdate, get_first_day, getdate
from six import itervalues

from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
	get_dimension_with_children,
)
from erpnext.accounts.report.utils import convert_to_presentation_currency, get_currency
from erpnext.accounts.utils import get_fiscal_year
from erpnext.accounts.report.financial_statements import get_cost_centers_with_children, apply_additional_conditions

def get_additional_conditions(from_date, ignore_closing_entries, filters):
	additional_conditions = []

	accounting_dimensions = get_accounting_dimensions(as_list=False)

	if ignore_closing_entries:
		additional_conditions.append("ifnull(voucher_type, '')!='Period Closing Voucher'")

	if from_date:
		additional_conditions.append("posting_date >= %(from_date)s")

	if filters:
		if filters.get("project"):
			if not isinstance(filters.get("project"), list):
				filters.project = frappe.parse_json(filters.get("project"))

			additional_conditions.append("project in %(project)s")

		if filters.get("cost_center"):
			filters.cost_center = get_cost_centers_with_children(filters.cost_center)
			additional_conditions.append("cost_center in %(cost_center)s")

		if filters.get("include_default_book_entries"):
			additional_conditions.append(
				"(finance_book in (%(finance_book)s, %(company_fb)s, '') OR finance_book IS NULL)"
			)
		else:
			additional_conditions.append("(finance_book in (%(finance_book)s, '') OR finance_book IS NULL)")

	if accounting_dimensions:
		for dimension in accounting_dimensions:
			if filters.get(dimension.fieldname):
				if frappe.get_cached_value("DocType", dimension.document_type, "is_tree"):
					filters[dimension.fieldname] = get_dimension_with_children(
						dimension.document_type, filters.get(dimension.fieldname)
					)
					additional_conditions.append("{0} in %({0})s".format(dimension.fieldname))
				else:
					additional_conditions.append("{0} in %({0})s".format(dimension.fieldname))

	return " and {}".format(" and ".join(additional_conditions)) if additional_conditions else ""

def get_accounting_entries(
	doctype,
	from_date,
	to_date,
	accounts,
	filters,
	ignore_closing_entries,
	period_closing_voucher=None,
	ignore_opening_entries=False,
):
	gl_entry = frappe.qb.DocType(doctype)
	query = (
		frappe.qb.from_(gl_entry)
		.select(
			gl_entry.account,
			gl_entry.debit,
			gl_entry.credit,
			gl_entry.debit_in_account_currency,
			gl_entry.credit_in_account_currency,
			gl_entry.account_currency,
			gl_entry.cost_center
		)
		.where(gl_entry.company == filters.company)
	)

	if doctype == "GL Entry":
		query = query.select(gl_entry.posting_date, gl_entry.is_opening, gl_entry.fiscal_year)
		query = query.where(gl_entry.is_cancelled == 0)
		query = query.where(gl_entry.posting_date <= to_date)

		if ignore_opening_entries:
			query = query.where(gl_entry.is_opening == "No")
	else:
		query = query.select(gl_entry.closing_date.as_("posting_date"))
		query = query.where(gl_entry.period_closing_voucher == period_closing_voucher)

	query = apply_additional_conditions(doctype, query, from_date, ignore_closing_entries, filters)
	query = query.where(gl_entry.account.isin(accounts))

	entries = query.run(as_dict=True)

	return entries

def set_gl_entries_by_account(
	company,
	from_date,
	to_date,
	root_lft,
	root_rgt,
	filters,
	gl_entries_by_account,
	ignore_closing_entries=False,
	ignore_opening_entries=False,
	root_type=None,
):
	"""Returns a dict like { "account": [gl entries], ... }"""
	gl_entries = []

	account_filters = {
		"company": company,
		"is_group": 0,
		"lft": (">=", root_lft),
		"rgt": ("<=", root_rgt),
	}

	if root_type:
		account_filters.update(
			{
				"root_type": root_type,
			}
		)

	accounts_list = frappe.db.get_all(
		"Account",
		filters=account_filters,
		pluck="name",
	)

	if accounts_list:
		# For balance sheet
		ignore_closing_balances = frappe.db.get_single_value(
			"Accounts Settings", "ignore_account_closing_balance"
		)
		if not from_date and not ignore_closing_balances:
			last_period_closing_voucher = frappe.db.get_all(
				"Period Closing Voucher",
				filters={
					"docstatus": 1,
					"company": filters.company,
					"posting_date": ("<", filters["period_start_date"]),
				},
				fields=["posting_date", "name"],
				order_by="posting_date desc",
				limit=1,
			)
			if last_period_closing_voucher:
				gl_entries += get_accounting_entries(
					"Account Closing Balance",
					from_date,
					to_date,
					accounts_list,
					filters,
					ignore_closing_entries,
					last_period_closing_voucher[0].name,
				)
				from_date = add_days(last_period_closing_voucher[0].posting_date, 1)
				ignore_opening_entries = True

		gl_entries += get_accounting_entries(
			"GL Entry",
			from_date,
			to_date,
			accounts_list,
			filters,
			ignore_closing_entries,
			ignore_opening_entries=ignore_opening_entries,
		)

		if filters and filters.get("presentation_currency"):
			convert_to_presentation_currency(gl_entries, get_currency(filters))

		for entry in gl_entries:
			gl_entries_by_account.setdefault(entry.account, []).append(entry)

		return gl_entries_by_account