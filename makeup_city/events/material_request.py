from frappe import _
import frappe
from frappe.utils import flt
from makeup_city.events.stock_entry import get_item_stock_qty

def validate(self, method=None):
	if self.material_request_type == "Material Transfer":
		for item in self.items:
			item.custom_target_actual_qty = get_item_stock_qty(item.item_code, item.warehouse, self.transaction_date, None)
	
	total_qty, total_amount = 0.0, 0.0
	for item in self.items:
		total_qty += flt(item.qty)
		item_tax_template = frappe.db.get_value("Item Tax", {"parenttype": "Item", "parent": item.item_code, "idx": 1}, "item_tax_template")
		tax_rate = frappe.db.get_value("Item Tax Template Detail", {"parenttype": "Item Tax Template", "parent": item_tax_template}, "tax_rate") or 0
		total_amount += flt(item.amount + item.amount*tax_rate/100)
	
	self.custom_total_qty = total_qty
	self.custom_total_amount = total_amount
		