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