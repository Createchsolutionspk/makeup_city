// Copyright (c) 2026, Createch Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Branch Wise Sales and Stock"] ={
    "filters": [
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1,
            "default": ""
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "reqd": 1,
            "default": "Today"
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "reqd": 1,
            "default": "Today"
        },
        {
            "fieldname": "warehouse",
            "label": "Warehouse",
            "fieldtype": "Link",
            "options": "Warehouse"
        },
        {
            "fieldname": "item_code",
            "label": "Item",
            "fieldtype": "MultiSelectList",
            "get_data": "function(txt) { return frappe.db.get_link_options('Item', txt); }"
        },
        {
            "fieldname": "cost_center",
            "label": "Cost Center",
            "fieldtype": "Link",
            "options": "Cost Center"
        }
    ]
}
