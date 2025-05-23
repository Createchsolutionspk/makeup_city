import frappe
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    # Build dynamic WHERE conditions
    conditions = ["si.docstatus = 1", "si.posting_date BETWEEN %(from_date)s AND %(to_date)s"]
    
    if filters.get("pos_opening"):
        conditions.append("si.posa_pos_opening_shift = %(pos_opening)s")
    if filters.get("pos_profile"):
        conditions.append("si.pos_profile = %(pos_profile)s")

    condition_str = " AND ".join(conditions)

    # Step 1: Fetch distinct MOPs
    mop_list = frappe.db.sql(f"""
        SELECT DISTINCT sip.mode_of_payment, mop.type
        FROM `tabSales Invoice Payment` AS sip
        JOIN `tabSales Invoice` AS si ON sip.parent = si.name
        LEFT JOIN `tabMode of Payment` AS mop ON mop.name = sip.mode_of_payment
        WHERE {condition_str}
    """, filters, as_dict=True)

    # Step 2: Dynamic MOP Columns
    mop_columns = []
    for idx, mop in enumerate(mop_list, start=1):
        mop_columns.extend([
            {"label": f"Mode of Payment {idx}", "fieldname": f"mode_of_payment_{idx}", "fieldtype": "Data", "width": 150},
            {"label": f"Type {idx}", "fieldname": f"mop_type_{idx}", "fieldtype": "Data", "width": 100},
            {"label": f"Account {idx}", "fieldname": f"mop_account_{idx}", "fieldtype": "Link", "options": "Account", "width": 180},
            {"label": f"Amount {idx}", "fieldname": f"mop_amount_{idx}", "fieldtype": "Currency", "width": 130},
            {"label": f"Change Amount {idx}", "fieldname": f"mop_change_{idx}", "fieldtype": "Currency", "width": 130},
            {"label": f"Net Amount {idx}", "fieldname": f"mop_net_{idx}", "fieldtype": "Currency", "width": 140}
        ])

    # Step 3: Fetch relevant data
    invoices = frappe.db.sql(f"""
        SELECT
            si.name AS invoice,
            si.posting_date,
            si.set_warehouse,
            si.pos_profile,
            si.posa_pos_opening_shift,
            si.grand_total,
            si.change_amount,
            sip.account,
            sip.mode_of_payment,
            sip.amount,
            mop.type,
            pos_closing.period_start_date,
            pos_closing.name AS closing_shift,
            pos_closing.period_end_date
        FROM `tabSales Invoice` AS si
        JOIN `tabSales Invoice Payment` AS sip ON sip.parent = si.name
        LEFT JOIN `tabMode of Payment` AS mop ON mop.name = sip.mode_of_payment
        LEFT JOIN `tabPOS Opening Shift` AS pos ON pos.name = si.posa_pos_opening_shift
        LEFT JOIN (
            SELECT pos_opening_shift, period_start_date, MAX(period_end_date) AS period_end_date, name
            FROM `tabPOS Closing Shift`
            GROUP BY pos_opening_shift
        ) pos_closing ON pos_closing.pos_opening_shift = si.posa_pos_opening_shift
        WHERE {condition_str}
    """, filters, as_dict=True)

    # Step 4: Aggregate per POS Opening Shift
    summary = {}
    for row in invoices:
        key = row.posa_pos_opening_shift
        if key not in summary:
            summary[key] = {
                "pos_profile": row.pos_profile,
                "set_warehouse": row.set_warehouse,
                "posa_pos_opening_shift": row.posa_pos_opening_shift,
                "pos_opening_date": row.period_start_date,
                "pos_closing": row.closing_shift,
                "pos_closing_date": row.period_end_date,
                "grand_total": 0.0,
                "total_net_amount": 0.0
            }

        summary[key]["grand_total"] += flt(row.grand_total)

        for idx, mop in enumerate(mop_list, start=1):
            if mop.mode_of_payment == row.mode_of_payment:
                summary[key][f"mode_of_payment_{idx}"] = row.mode_of_payment
                summary[key][f"mop_type_{idx}"] = row.type
                summary[key][f"mop_account_{idx}"] = row.account
                summary[key][f"mop_amount_{idx}"] = summary[key].get(f"mop_amount_{idx}", 0.0) + flt(row.amount)
                summary[key][f"mop_change_{idx}"] = summary[key].get(f"mop_change_{idx}", 0.0) + (flt(row.change_amount) if row.type == "Cash" else 0.0)

                # Net amount logic
                net_amt = flt(row.amount)
                if row.type == "Cash":
                    net_amt -= flt(row.change_amount)
                summary[key][f"mop_net_{idx}"] = summary[key].get(f"mop_net_{idx}", 0.0) + net_amt

                # Total net amount
                summary[key]["total_net_amount"] += net_amt

    # Step 5: Columns
    columns = [
        {"label": "POS Profile", "fieldname": "pos_profile", "fieldtype": "Link", "options": "POS Profile", "width": 150},
        {"label": "Warehouse", "fieldname": "set_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 120},
        {"label": "POS Opening Shift", "fieldname": "posa_pos_opening_shift", "fieldtype": "Link", "options": "POS Opening Shift", "width": 150},
        {"label": "POS Opening Date", "fieldname": "pos_opening_date", "fieldtype": "Datetime", "width": 110},
        {"label": "POS Closing Shift", "fieldname": "pos_closing", "fieldtype": "Link", "options": "POS Closing Shift", "width": 150},
        {"label": "POS Closing Date", "fieldname": "pos_closing_date", "fieldtype": "Datetime", "width": 110},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 120}
    ] + mop_columns + [
        {"label": "Total Net Amount", "fieldname": "total_net_amount", "fieldtype": "Currency", "width": 140},
        {"label": "Difference (Grand Total - Net)", "fieldname": "difference", "fieldtype": "Currency", "width": 150}
    ]

    # Step 6: Add Difference Field
    for row in summary.values():
        row["difference"] = flt(row["grand_total"]) - flt(row.get("total_net_amount", 0.0))

    return columns, list(summary.values())
