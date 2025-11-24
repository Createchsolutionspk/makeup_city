import frappe

@frappe.whitelist()
def submit_se_in_background(docname):
    frappe.enqueue(
        "makeup_city.utils.process_se_submission",
        docname=docname,
        queue="long"
    )
    return "Queued"


def process_se_submission(docname):
    doc = frappe.get_doc("Stock Entry", docname)

    if doc.docstatus != 0:
        frappe.log_error(f"Stock Entry {docname} is already submitted or cancelled.")
        return

    try:
        doc.submit()
        frappe.db.commit()
        frappe.log_error(f"Stock Entry {docname} submitted successfully in background.")
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error submitting Stock Entry {docname}: {str(e)}")
        raise
