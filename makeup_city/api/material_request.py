import frappe
from frappe.utils import add_days, getdate

def get_past_60_days_sales_qty(item_code, warehouse, posting_date=None):
	"""
	Get total sales quantity of an item in a cost center for the past 60 days before posting_date.
	
	Args:
	    item_code (str): Item Code
	    warehouse (str): Cost Center
	    posting_date (str or datetime.date, optional): Reference posting date. Defaults to today.
	
	Returns:
	    float: Total sold quantity in the last 60 days
	"""
	if not posting_date:
		posting_date = getdate()
	else:
		posting_date = getdate(posting_date)

	start_date = add_days(posting_date, -60)

	sales_qty = frappe.db.sql("""
		SELECT IFNULL(SUM(si_item.qty), 0) as total_qty
		FROM `tabSales Invoice Item` si_item
		INNER JOIN `tabSales Invoice` si
			ON si.name = si_item.parent
		WHERE si.docstatus = 1
			AND si.posting_date BETWEEN %s AND %s
			AND si_item.item_code = %s
			AND si_item.warehouse = %s
	""", (start_date, posting_date, item_code, warehouse), as_dict=True)

	total_qty = sales_qty[0].total_qty if sales_qty else 0

	return total_qty
