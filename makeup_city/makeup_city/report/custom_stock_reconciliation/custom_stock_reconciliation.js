// Copyright (c) 2025, Createch Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Custom Stock Reconciliation"] = {
	"filters": [
		{
			"fieldname": "Stock_Reconciliation",
			"label": "ID",
			"fieldtype": "Link",
			"options": "Stock Reconciliation",
			"width": 200
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200
		},
		{
			"fieldname": "cost_center",
			"label": "Cost Center",
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 200
		},
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		}
	]
};

