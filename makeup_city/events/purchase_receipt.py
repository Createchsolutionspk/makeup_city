import frappe
from frappe import _

def validate_duplicate_draft_grn(doc, method):
    if not doc.items:
        return

    # Collect unique Purchase Orders from the PR items
    purchase_orders = {d.purchase_order for d in doc.items if d.purchase_order}

    for po in purchase_orders:
        # Search for existing draft Purchase Receipts for the same PO (excluding current doc)
        draft_grns = frappe.db.sql("""
            SELECT pri.parent as grn_name
            FROM `tabPurchase Receipt Item` pri
            JOIN `tabPurchase Receipt` pr ON pr.name = pri.parent
            WHERE pri.purchase_order = %s
              AND pr.docstatus = 0
              AND pr.name != %s
            LIMIT 1
        """, (po, doc.name), as_dict=True)

        if draft_grns:
            frappe.throw(_(
                f"A draft Purchase Receipt ({draft_grns[0].grn_name}) already exists for Purchase Order {po}. "
                "Please submit or cancel it before creating a new one."
            ))
