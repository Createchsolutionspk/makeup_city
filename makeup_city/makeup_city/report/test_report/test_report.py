# Copyright (c) 2025, Createch Solutions and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	data = frappe.db.sql("""
		SELECT
			name AS item_code,
			item_name,
			item_group,
			brand
		FROM
			`tabItem`
		WHERE
			disabled = 0
		ORDER BY
			item_name ASC limit 1000
	""", as_dict=1, debug=1)
	frappe.msgprint(str(data))
	return columns, data