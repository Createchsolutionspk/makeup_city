// Copyright (c) 2025, Createch Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Sales Payment Wise Summary Extended"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
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
			fieldname: "location",
			label: "Location",
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			fieldname: "pos_profile",
			label: "POS Profile",
			fieldtype: "Link",
			options: "POS Profile",
		}
	]
};
