// Copyright (c) 2025, Createch Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Wise Sales Register Extended V1"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "mode_of_payment",
			label: __("Mode of Payment"),
			fieldtype: "Link",
			options: "Mode of Payment",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			"reqd": 0,
			options: "Warehouse",
			get_query: function () {
				const company = frappe.query_report.get_filter_value("company");
				return {
					filters: { company: company },
				};
			},
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Link",
			options: "Brand",
		},
		{
			fieldname: "brand_type",
			label: __("Brand Type"),
			fieldtype: "Select",
			options: ["", "Purchased", "Internal", "Consignment", "External"],
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
		},
		{
			label: __("Group By"),
			fieldname: "group_by",
			fieldtype: "Select",
			options: ["", "Customer Group", "Customer", "Item Group", "Item", "Territory", "Invoice", "Group by Invoice", "Warehouse"],
		},
		{
			fieldname: "invoice",
			label: __("Invoice"),
			fieldtype: "Link",
			options: "Sales Invoice",
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();
		}
		return value;
	},
};
