from frappe import _
import frappe
from makeup_city.events.stock_entry import get_item_stock_qty

def validate(self, method=None):
	if self.material_request_type == "Material Transfer":
		for item in self.items:
			item.custom_target_actual_qty = get_item_stock_qty(item.item_code, item.warehouse, self.transaction_date, None)
