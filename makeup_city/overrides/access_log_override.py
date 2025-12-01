import frappe
from frappe.utils import cstr
from frappe.query_builder import Interval
from frappe.query_builder.functions import Now

from frappe.core.doctype.access_log.access_log import AccessLog

class CustomAccessLog(AccessLog):
	@staticmethod
	def clear_old_logs(days=30):
		table = frappe.qb.DocType("Error Log")
		frappe.db.delete(table, filters=(table.modified < (Now() - Interval(days=days))))