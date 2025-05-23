from frappe import _
import frappe
from frappe.utils import nowtime
from erpnext.stock.stock_ledger import NegativeStockError, get_previous_sle, get_valuation_rate

@frappe.whitelist()
def get_item_stock_qty(item_code, warehouse, posting_date, posting_time):
	posting_time = nowtime()
	previous_sle = get_previous_sle(
		{
			"item_code": item_code,
			"warehouse": warehouse,
			"posting_date": posting_date,
			"posting_time": posting_time,
		}
	)

	# get actual stock at source warehouse
	actual_qty = previous_sle.get("qty_after_transaction") or 0
	return actual_qty

def validate(self, method=None):
	if self.stock_entry_type == "Material Transfer":
		has_material_req = bool(self.items[0].material_request and self.items[0].material_request_item)
		if not has_material_req:
			return
		for item in self.items[1:]:
			if not bool(item.material_request and item.material_request_item):
				frappe.throw(_(f"<span style='font-weight: bold;'>Row {item.idx}:</span> Item <span style='font-weight: bold;'>{item.item_code}</span> is not linked to Material Request Items."))
