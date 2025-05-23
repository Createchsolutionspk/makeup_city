import frappe
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    # Initialize an empty condition for pos_opening_shift
    pos_opening_condition = ""

    # Add conditions based on filters
    if filters.get("pos_opening"):
        pos_opening_condition += "AND si.posa_pos_opening_shift = %(pos_opening)s\n"
    if filters.get("location"):
        pos_opening_condition += "AND si.set_warehouse = %(location)s\n"
    if filters.get("pos_profile"):
        pos_opening_condition += "AND si.pos_profile = %(pos_profile)s\n"

    data = frappe.db.sql(f"""
        SELECT 
            si.posting_date AS "Posting Date",
            si.set_warehouse AS "Location",
            si.pos_profile,
            si.posa_pos_opening_shift AS "POS Opening Shift",
            pos_closing.period_start_date AS "Period Start Date",
            pos_closing.name AS "POS Closing Shift",
            pos_closing.period_end_date AS "Closing End Date",
            sip.mode_of_payment AS "Mode of Payment",
            mop.type AS "Payment Type",
            SUM(sip.amount) AS "Total Payment Amount",
            SUM(CASE WHEN mop.type = 'Cash' THEN si.change_amount ELSE 0 END) AS "Total Change Amount",
            (SUM(sip.amount) - SUM(CASE WHEN mop.type = 'Cash' THEN si.change_amount ELSE 0 END)) AS "Net Amount",
            GROUP_CONCAT(DISTINCT sip.account) AS "Accounts",
            COUNT(sip.parent) AS "Invoice Count"
        FROM 
            `tabSales Invoice Payment` AS sip
        JOIN 
            `tabSales Invoice` AS si ON sip.parent = si.name
        LEFT JOIN 
            `tabMode of Payment` AS mop ON sip.mode_of_payment = mop.name
        LEFT JOIN 
            `tabPOS Opening Shift` AS pos ON pos.name = si.posa_pos_opening_shift
        LEFT JOIN (
            SELECT 
                pos_opening_shift,
                period_start_date,
                MAX(period_end_date) AS period_end_date,
                name
            FROM `tabPOS Closing Shift`
            GROUP BY pos_opening_shift
        ) pos_closing ON pos_closing.pos_opening_shift = si.posa_pos_opening_shift

        WHERE 
            si.docstatus = 1
            AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
            {pos_opening_condition}
        GROUP BY 
            si.posting_date, si.set_warehouse, si.posa_pos_opening_shift, sip.mode_of_payment, mop.type
        ORDER BY 
            si.posting_date, sip.mode_of_payment
    """, filters, as_dict=1)

    columns = [
        {"label": "Posting Date", "fieldname": "Posting Date", "fieldtype": "Date", "width": 100},
        {"label": "Location", "fieldname": "Location", "fieldtype": "Link", "options": "Warehouse", "width": 120},
        {"label": "POS Profile", "fieldname": "pos_profile", "fieldtype": "Link", "options": "POS Profile", "width": 180},
        {"label": "POS Opening Shift", "fieldname": "POS Opening Shift", "fieldtype": "Link", "options": "POS Opening Shift", "width": 180},
        {"label": "POS Opening Date", "fieldname": "Period Start Date", "fieldtype": "Date", "width": 120},
        {"label": "POS Closing Shift", "fieldname": "POS Closing Shift", "fieldtype": "Link", "options": "POS Closing Shift", "width": 180},
        {"label": "POS Closing Date", "fieldname": "Closing End Date", "fieldtype": "Date", "width": 120},
        {"label": "Mode of Payment", "fieldname": "Mode of Payment", "fieldtype": "Link", "options": "Mode of Payment", "width": 150},
        {"label": "Payment Type", "fieldname": "Payment Type", "fieldtype": "Data", "width": 100},
        {"label": "Total Payment Amount", "fieldname": "Total Payment Amount", "fieldtype": "Currency", "width": 150},
        {"label": "Total Change Amount", "fieldname": "Total Change Amount", "fieldtype": "Currency", "width": 150},
        {"label": "Net Amount", "fieldname": "Net Amount", "fieldtype": "Currency", "width": 130},
        {"label": "Accounts", "fieldname": "Accounts", "fieldtype": "Data", "width": 200},
        {"label": "Invoice Count", "fieldname": "Invoice Count", "fieldtype": "Int", "width": 120}
    ]

    return columns, data
