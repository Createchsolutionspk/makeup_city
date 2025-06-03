import frappe
from frappe import _

@frappe.whitelist()
def get_pos_profile(user=frappe.session.user):
	return frappe.db.sql("""
		SELECT pos.warehouse from `tabPOS Profile` pos
		inner join `tabPOS Profile User` pou ON pou.parent=pos.name
		where pou.user='%s' limit 1
	"""%user, as_dict=1)


