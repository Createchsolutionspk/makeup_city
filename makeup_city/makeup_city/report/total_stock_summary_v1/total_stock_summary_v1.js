// Copyright (c) 2026, Createch Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total Stock Summary V1"] = {
	filters: [
		{
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			width: "80",
			reqd: 1,
			options: ["Warehouse", "Company"],
			default: "Warehouse",
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			width: "80",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("Company"),
			depends_on: "eval: doc.group_by != 'Company'",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
			width: "80"
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
			width: "80"
		},
		{
			fieldname: "show_zero_stock",
			label: __("Show Zero Stock"),
			fieldtype: "Check",
			width: "80"
		}
	],
};
