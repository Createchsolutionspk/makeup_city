# sales_person_summary.py

import frappe
from frappe import _
from frappe.utils import nowdate


def execute(filters=None):
    return get_columns(), get_data(filters)


def get_columns():
    return [
        {"label": _("Sales Person"),     "fieldname": "sales_person",  "fieldtype": "Data",     "width": 200},
        {"label": _("Total Qty"),         "fieldname": "total_qty",     "fieldtype": "Float",    "width": 120},
        {"label": _("Net Sales Total"),   "fieldname": "net_total",     "fieldtype": "Currency", "width": 150},
        {"label": _("Grand Total"),       "fieldname": "grand_total",   "fieldtype": "Currency", "width": 150},
        {"label": _("Total Sales Value"), "fieldname": "total_sales",   "fieldtype": "Currency", "width": 150},
    ]


def get_conditions(filters):
    conditions = "WHERE si.docstatus = 1"

    if filters.get("from_date"):
        conditions += " AND si.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND si.posting_date <= %(to_date)s"
    if filters.get("sales_person"):
        conditions += " AND sp.sales_person = %(sales_person)s"
    if filters.get("warehouse"):
        conditions += " AND si.set_warehouse = %(warehouse)s"
    if filters.get("cost_center"):
        cost_center_info = frappe.db.get_value(
            "Cost Center", filters["cost_center"], ["lft", "rgt"], as_dict=True
        )
        if cost_center_info:
            child_cost_centers = frappe.db.get_all(
                "Cost Center",
                filters={"lft": [">=", cost_center_info.lft], "rgt": ["<=", cost_center_info.rgt]},
                pluck="name"
            )
            if child_cost_centers:
                formatted_cc = ", ".join(f"'{cc}'" for cc in child_cost_centers)
                conditions += f" AND si.cost_center IN ({formatted_cc})"

    return conditions


def get_data(filters=None):
    conditions = get_conditions(filters)

    return frappe.db.sql(f"""
        SELECT
            sp.sales_person,
            SUM(si.total_qty)                                          AS total_qty,
            SUM(si.net_total)                                           AS net_total,
            SUM(si.grand_total)                                         AS grand_total,
            SUM(si.net_total * IFNULL(sp.allocated_percentage, 100) / 100) AS total_sales
        FROM `tabSales Invoice` si
        INNER JOIN `tabSales Team` sp           ON sp.parent = si.name
        {conditions}
        GROUP BY sp.sales_person
        ORDER BY total_sales DESC
    """, filters, as_dict=1, debug=1)