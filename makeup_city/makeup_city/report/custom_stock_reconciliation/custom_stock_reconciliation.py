
import frappe
from frappe import _
from frappe.utils import getdate


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	return [
		{"label": "ID", "fieldname": "id", "fieldtype": "Link", "options": "Stock Reconciliation", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": "Cost Center", "fieldname": "cost_center", "fieldtype": "Link", "options": "Cost Center", "width": 150},

		# Child Table Fields
		{"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
		{"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 120},
		{"label": "Current Qty", "fieldname": "current_qty", "fieldtype": "Float", "width": 100},
		{"label": "Quantity", "fieldname": "qty", "fieldtype": "Float", "width": 100},
		{"label": "Qty Diff", "fieldname": "quantity_difference", "fieldtype": "Float", "width": 100},
		{"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
		{"label": "Current Amount", "fieldname": "current_amount", "fieldtype": "Currency", "width": 120},
		{"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
		{"label": "Amount Diff", "fieldname": "amount_difference", "fieldtype": "Currency", "width": 120},
	]


# Copyright (c) 2025, Createch Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	return [
		{"label": "ID", "fieldname": "id", "fieldtype": "Link", "options": "Stock Reconciliation", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{"label": "Cost Center", "fieldname": "cost_center", "fieldtype": "Link", "options": "Cost Center", "width": 150},

		# Child Table Fields
		{"label": "Item Code (Stock Reconciliation Item)", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
		{"label": "Item Group (Stock Reconciliation Item)", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 120},
		{"label": "Current Qty (Stock Reconciliation Item)", "fieldname": "current_qty", "fieldtype": "Float", "width": 100},
		{"label": "Quantity (Stock Reconciliation Item)", "fieldname": "qty", "fieldtype": "Float", "width": 100},
		{"label": "Quantity Difference (Stock Reconciliation Item)", "fieldname": "quantity_difference", "fieldtype": "Float", "width": 100},
		{"label": "Warehouse (Stock Reconciliation Item)", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
		{"label": "Current Amount (Stock Reconciliation Item)", "fieldname": "current_amount", "fieldtype": "Currency", "width": 120},
		{"label": "Amount (Stock Reconciliation Item)", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
		{"label": "Amount Difference (Stock Reconciliation Item)", "fieldname": "amount_difference", "fieldtype": "Currency", "width": 120},
	]


def get_data(filters):
	conditions = []
	values = {}

	if filters.get("Stock_Reconciliation"):
		conditions.append("sr.name = %(stock_reconciliation)s")
		values["stock_reconciliation"] = filters["Stock_Reconciliation"]

	if filters.get("item_code"):
		conditions.append("sri.item_code = %(item_code)s")
		values["item_code"] = filters["item_code"]

	if filters.get("cost_center"):
		conditions.append("sr.cost_center = %(cost_center)s")
		values["cost_center"] = filters["cost_center"]

	if filters.get("from_date"):
		conditions.append("sr.posting_date >= %(from_date)s")
		values["from_date"] = getdate(filters["from_date"])

	if filters.get("to_date"):
		conditions.append("sr.posting_date <= %(to_date)s")
		values["to_date"] = getdate(filters["to_date"])

	where_clause = " AND ".join(conditions)
	if where_clause:
		where_clause = "WHERE " + where_clause

	query = f"""
		SELECT
			sr.name AS id,
			sr.docstatus,
			CASE sr.docstatus
				WHEN 0 THEN 'Draft'
				WHEN 1 THEN 'Submitted'
				WHEN 2 THEN 'Cancelled'
			END AS status,
			sr.posting_date,
			sr.cost_center,

			sri.item_code,
			sri.item_group,
			sri.current_qty,
			sri.qty,
			sri.quantity_difference,
			sri.warehouse,
			sri.current_amount,
			sri.amount,
			sri.amount_difference

		FROM `tabStock Reconciliation` sr
		INNER JOIN `tabStock Reconciliation Item` sri ON sr.name = sri.parent
		{where_clause}
		ORDER BY sr.posting_date DESC, sr.name DESC
	"""

	return frappe.db.sql(query, values, as_dict=True)

