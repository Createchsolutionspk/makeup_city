# Copyright (c) 2025, Createch Solutions and contributors
# For license information, please see license.txt


from operator import itemgetter
from typing import Any, TypedDict

import frappe
from frappe import _
from frappe.query_builder import Order
from frappe.query_builder.functions import Coalesce
from frappe.utils import add_days, cint, date_diff, flt, getdate
from frappe.utils.nestedset import get_descendants_of

import erpnext
from erpnext.stock.doctype.inventory_dimension.inventory_dimension import get_inventory_dimensions
from erpnext.stock.doctype.warehouse.warehouse import apply_warehouse_filter
from erpnext.stock.report.stock_ageing.stock_ageing import FIFOSlots, get_average_age
from erpnext.stock.utils import add_additional_uom_columns
from erpnext.stock.report.stock_balance.stock_balance import StockBalanceReport

def execute(filters=None):
	return StockBalanceReport(filters).run()