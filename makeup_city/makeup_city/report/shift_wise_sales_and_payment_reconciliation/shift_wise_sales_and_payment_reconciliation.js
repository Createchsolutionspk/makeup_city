// Copyright (c) 2025, Createch Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Shift Wise Sales and Payment Reconciliation"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: "pos_opening",
			label: "POS Opening Shift",
			fieldtype: "Link",
			options: "POS Opening Shift",
		},
		{
			fieldname: "pos_profile",
			label: "POS Profile",
			fieldtype: "Link",
			options: "POS Profile",
		}
	]
};
