# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Sum

def execute(filters=None):
	if not filters:
		filters = {}
	columns = get_columns(filters)
	stock = get_total_stock(filters)
	return columns, stock

def get_columns(filters):
	columns = [
		_("Item") + ":Data:150",          # Changed from Link/Item
		_("Description") + ":Data:300",
		_("Current Qty") + ":Float:100",
	]

	if filters.get("group_by") == "Warehouse":
		columns.insert(0, _("Warehouse") + ":Data:150")  # Changed from Link/Warehouse
	else:
		columns.insert(0, _("Company") + ":Data:250")     # Changed from Link/Company

	return columns

def get_total_stock(filters):
	bin = frappe.qb.DocType("Bin")
	item = frappe.qb.DocType("Item")
	wh = frappe.qb.DocType("Warehouse")

	# Temporarily bypass user permissions
	original_ignore_permissions = frappe.flags.ignore_user_permissions
	frappe.flags.ignore_user_permissions = True

	try:
		query = (
			frappe.qb.from_(bin)
			.inner_join(item).on(bin.item_code == item.item_code)
			.inner_join(wh).on(wh.name == bin.warehouse)
			.where(bin.actual_qty != 0)
		)

		# Apply item filter
		if filters.get("item"):
			query = query.where(item.item_code == filters.get("item"))

		# Group by logic
		if filters.get("group_by") == "Warehouse":
			query = query.select(
				bin.warehouse
			).groupby(bin.warehouse)
		else:
			query = query.select(
				wh.company
			).groupby(wh.company)

		# Final select
		query = query.select(
			item.item_code,
			item.description,
			Sum(bin.actual_qty).as_("actual_qty")
		).groupby(item.item_code)

		return query.run()

	finally:
		# Reset permission bypass
		frappe.flags.ignore_user_permissions = original_ignore_permissions
