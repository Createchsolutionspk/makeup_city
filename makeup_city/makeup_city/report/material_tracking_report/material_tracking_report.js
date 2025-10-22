frappe.query_reports["Material Tracking Report"] = {
    "filters": [
        {
            "fieldname": "set_warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "reqd": 0,
            "default": ""
        }
    ]
}
