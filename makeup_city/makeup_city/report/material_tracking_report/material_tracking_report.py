import frappe



def execute(filters=None):
    columns = [
        {"label": "MR Date", "fieldname": "mr_date", "fieldtype": "Date", "width": 100},
        {"label": "Material Request No", "fieldname": "material_request_no", "fieldtype": "Link", "options": "Material Request", "width": 150},
        {"label": "MR Quantity", "fieldname": "mr_quantity", "fieldtype": "Float", "width": 120},
        
        {"label": "Stock Entry Transit Date", "fieldname": "transit_date", "fieldtype": "Date", "width": 120},
        {"label": "Stock Entry in Transit", "fieldname": "stock_entry_transit", "fieldtype": "Link", "options": "Stock Entry", "width": 150},
        {"label": "Transit Quantity", "fieldname": "transit_quantity", "fieldtype": "Float", "width": 120},
        
        {"label": "Stock Entry Receiving Date", "fieldname": "receiving_date", "fieldtype": "Date", "width": 120},
        {"label": "Stock Entry Receiving", "fieldname": "stock_entry_receiving", "fieldtype": "Link", "options": "Stock Entry", "width": 150},
        {"label": "Receiving Quantity", "fieldname": "receiving_quantity", "fieldtype": "Float", "width": 120},
        
        {"label": "PO Date", "fieldname": "po_date", "fieldtype": "Date", "width": 100},
        {"label": "PO No", "fieldname": "po_no", "fieldtype": "Link", "options": "Purchase Order", "width": 150},
        {"label": "PO Quantity", "fieldname": "po_quantity", "fieldtype": "Float", "width": 120},

        {"label": "GRN Date", "fieldname": "grn_date", "fieldtype": "Date", "width": 100},
        {"label": "GRN No", "fieldname": "grn_no", "fieldtype": "Link", "options": "Purchase Receipt", "width": 150},
        {"label": "GRN Quantity", "fieldname": "grn_quantity", "fieldtype": "Float", "width": 120},
    ]

    data = get_data(filters)  # You will fill this later with your logic

    return columns, data


def get_data(filters=None):
    filters = filters or {}
    
    conditions = []
    values = {}

    # Filter on warehouse if provided
    if filters.get("set_warehouse"):
        conditions.append("mr.set_warehouse = %(set_warehouse)s")
        values["set_warehouse"] = filters.get("set_warehouse")

    where_clause = " AND ".join(conditions)
    if where_clause:
        where_clause = " AND " + where_clause

    query = f"""
        SELECT
            mr.transaction_date AS mr_date,
            mr.name AS material_request_no,
            mr.custom_total_qty AS mr_quantity,
            
            se.posting_date AS transit_date,
            se.name AS stock_entry_transit,
            se.custom_total_qty AS transit_quantity,

            NULL AS receiving_date,
            NULL AS stock_entry_receiving,
            NULL AS receiving_quantity,

            NULL AS po_date,
            NULL AS po_no,
            NULL AS po_quantity,

            NULL AS grn_date,
            NULL AS grn_no,
            NULL AS grn_quantity

        FROM
            `tabMaterial Request` mr

        LEFT JOIN
            `tabStock Entry Detail` sei ON sei.material_request = mr.name

        LEFT JOIN
            `tabStock Entry` se ON se.name = sei.parent

        WHERE
            mr.docstatus = 1
            AND se.docstatus = 1
            {where_clause}
		GROUP BY
			se.name
        ORDER BY
            mr.transaction_date ASC
    """

    data = frappe.db.sql(query, values, as_dict=True)
    return data


