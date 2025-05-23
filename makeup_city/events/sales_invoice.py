import frappe
from frappe import _
from erpnext.accounts.doctype.pricing_rule.pricing_rule import apply_pricing_rule
from frappe.utils import cint, flt


def validate(doc, method=None):
	for item in doc.items:
		tax_rate = frappe.get_value("Item Tax Template Detail", {"parent": item.get("item_tax_template")}, "tax_rate") or 0
		item.rate_wtax = flt(item.rate * (1 + tax_rate / 100), 2)
		item.tax_rate = tax_rate

def validate_apply_pricing_rule(doc):
	"""
	args = {
		"items": [{"doctype": "", "name": "", "item_code": "", "brand": "", "item_group": ""}, ...],
		"customer": "something",
		"customer_group": "something",
		"territory": "something",
		"supplier": "something",
		"supplier_group": "something",
		"currency": "something",
		"conversion_rate": "something",
		"price_list": "something",
		"plc_conversion_rate": "something",
		"company": "something",
		"transaction_date": "something",
		"campaign": "something",
		"sales_partner": "something",
		"ignore_pricing_rule": "something"
	}
	"""

	args = {
		"items": [],
		"customer": doc.customer,
		"customer_group": doc.customer_group,
		"territory": doc.territory,
		"currency": doc.currency,
		"conversion_rate": doc.conversion_rate,
		"price_list": doc.selling_price_list,
		"price_list_currency": doc.price_list_currency,
		"plc_conversion_rate": doc.plc_conversion_rate,
		"company": doc.company,
		"transaction_date": doc.posting_date,
		"campaign": doc.get("campaign"),
		"sales_partner": doc.get("sales_partner"),
		"ignore_pricing_rule": doc.ignore_pricing_rule,
		"doctype": doc.doctype,
		"name": doc.name,
		"is_return": cint(doc.is_return),
		"update_stock": cint(doc.update_stock),
		"conversion_factor": doc.get("conversion_factor", 1),
		"pos_profile": doc.pos_profile,
		"coupon_code": doc.get("coupon_code"),
		"is_internal_customer": doc.is_internal_customer,
	}

	for d in doc.items:
		args["items"].append({
			"doctype": d.doctype,
			"name": d.name,
			"child_docname": d.name,
			"item_code": d.item_code,
			"item_group": d.item_group,
			"brand": d.brand,
			"qty": d.qty,
			"stock_qty": d.stock_qty,
			"uom": d.uom,
			"stock_uom": d.stock_uom,
			"parenttype": d.parenttype,
			"parent": d.parent,
			"pricing_rules": d.pricing_rules,
			"is_free_item": d.is_free_item,
			"warehouse": d.warehouse,
			"serial_no": d.serial_no,
			"batch_no": d.batch_no,
			"price_list_rate": d.price_list_rate,
			"conversion_factor": d.conversion_factor or 1.0
		})
	# apply_pricing_rule(args, doc=doc)
