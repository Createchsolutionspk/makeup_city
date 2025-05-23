// Copyright (c) 2025, Createch Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total Stock Summary Customized"] = {
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
			fieldname: "item",
			label: __("Item"),
			fieldtype: "Link",
			width: "80",
			options: "Item",
			reqd: 1,
		},
	],
};
