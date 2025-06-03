import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = [
        {"label": "Employee Name", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Employee ID", "fieldname": "customer_name", "fieldtype": "Data", "width": 250},
        {"label": "Monthly Limit", "fieldname": "monthly_limit", "fieldtype": "Currency", "width": 200},
        {"label": "Availed Discount", "fieldname": "availed_discount", "fieldtype": "Currency", "width": 200},
        {"label": "Remaining Limit", "fieldname": "remaining_limit", "fieldtype": "Currency", "width": 200},
    ]

    conditions = """
        si.docstatus = 1 AND si.customer_group = 'Employee'
    """

    if filters and filters.get("customer"):
        conditions += " AND si.customer = %(customer)s"

    data = frappe.db.sql(f"""
        SELECT
            si.customer,
            si.customer_name,
            c.custom_monthly_employee_discount_limit AS monthly_limit,
            SUM(
                IFNULL(si.discount_amount, 0) + (
                    SELECT SUM(IFNULL(sii.discount_amount, 0))
                    FROM `tabSales Invoice Item` sii
                    WHERE sii.parent = si.name
                )
            ) AS availed_discount
        FROM `tabSales Invoice` si
        LEFT JOIN `tabCustomer` c ON c.name = si.customer
        WHERE {conditions}
        GROUP BY si.customer, si.customer_name, c.custom_monthly_employee_discount_limit
    """, filters, as_dict=True)

    for row in data:
        row["remaining_limit"] = flt(row.monthly_limit) - flt(row.availed_discount)

    return columns, data
