// Copyright (c) 2026, Createch Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Person Summary"] = {
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
            fieldname: "sales_person",
            label: "Sales Person",
            fieldtype: "Link",
            options: "Sales Person"
        },
        {
            fieldname: "warehouse",
            label: "Warehouse",
            fieldtype: "Link",
            options: "Warehouse"
        },
        {
            fieldname: "cost_center",
            label: "Parent Cost Center",
            fieldtype: "Link",
            options: "Cost Center",
            get_query: function() { 
				return { 
					filters: { 
						'is_group': 1 
					} 
				} 
			}
        }
    ]
};
