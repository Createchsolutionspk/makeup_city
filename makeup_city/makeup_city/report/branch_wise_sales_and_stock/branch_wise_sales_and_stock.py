import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters)


def get_columns():
	return [
		# {"label": _("Date"), "fieldname": "date", "fieldtype": "Data", "width": 200},
		{"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 160},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 220},
		{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 220},
		{"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
		{"label": _("Sales"), "fieldname": "sales", "fieldtype": "Float", "width": 100},
		{"label": _("Stock Balance"), "fieldname": "stock_balance", "fieldtype": "Float", "width": 120},
		{"label": _("Cost Center"), "fieldname": "cost_center", "fieldtype": "Link", "options": "Cost Center", "width": 150},
	]


def get_conditions(filters):
	conditions = "WHERE si.docstatus = 1"

	if filters.get("company"):
		conditions += " AND si.company = %(company)s"
	if filters.get("from_date"):
		conditions += " AND si.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND si.posting_date <= %(to_date)s"
	if filters.get("warehouse"):
		conditions += " AND sii.warehouse = %(warehouse)s"
	if filters.get("item_code"):
		item_codes = filters["item_code"]
		if isinstance(item_codes, str):
			item_codes_str = ", ".join(f"'{i}'" for i in item_codes)
			conditions += f" AND sii.item_code IN ({item_codes_str})"
	if filters.get("cost_center"):
		conditions += " AND sii.cost_center = %(cost_center)s"

	return conditions


def get_data(filters=None):
	conditions = get_conditions(filters)

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	# Fetch sales data grouped by item + warehouse
	sales_data = frappe.db.sql(f"""
		SELECT
			sii.item_code,
			sii.item_name,
			sii.description,
			sii.warehouse,
			sii.cost_center,
			SUM(
				CASE WHEN si.is_return = 0 AND sii.is_free_item = 0 THEN sii.qty ELSE 0 END
			) AS sales
		FROM `tabSales Invoice` si
		INNER JOIN `tabSales Invoice Item` sii ON si.name = sii.parent
		{conditions}
			AND si.is_return = 0
		GROUP BY sii.item_code, sii.warehouse, sii.cost_center
	""", filters, as_dict=1)

	if not sales_data:
		return []

	# Fetch stock balance for each item+warehouse combo in one query
	item_warehouse_pairs = {(r.item_code, r.warehouse) for r in sales_data}
	stock_map = _get_stock_map(item_warehouse_pairs, to_date)

	# Build rows
	# date_label = f"{from_date} to {to_date}" if from_date and to_date else ""
	data = []
	for row in sales_data:
		key = (row.item_code, row.warehouse)
		data.append({
			# "date": date_label,
			"item_code": row.item_code,
			"item_name": row.item_name,
			"description": row.description,
			"warehouse": row.warehouse,
			"sales": row.sales,
			"stock_balance": stock_map.get(key, 0),
			"cost_center": row.cost_center,
		})

	return data


def _get_stock_map(item_warehouse_pairs, to_date):
	"""Return {(item_code, warehouse): stock_qty} for all pairs in one query."""
	if not item_warehouse_pairs:
		return {}

	# Build IN clause for (item_code, warehouse) pairs
	pair_conditions = " OR ".join(
		f"(item_code = '{item}' AND warehouse = '{wh}')"
		for item, wh in item_warehouse_pairs
	)

	date_filter = f"AND posting_date <= '{to_date}'" if to_date else ""

	rows = frappe.db.sql(f"""
		SELECT
			item_code,
			warehouse,
			SUM(actual_qty) AS stock_balance
		FROM `tabStock Ledger Entry`
		WHERE is_cancelled = 0
			{date_filter}
			AND ({pair_conditions})
		GROUP BY item_code, warehouse
	""", as_dict=1)

	return {(r.item_code, r.warehouse): r.stock_balance for r in rows}