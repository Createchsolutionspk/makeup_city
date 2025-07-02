frappe.query_reports["Cost Center Wise PNL"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		// {
		// 	"fieldname":"finance_book",
		// 	"label": __("Finance Book"),
		// 	"fieldtype": "Link",
		// 	"options": "Finance Book"
		// },
		// {
		// 	"fieldname":"filter_based_on",
		// 	"label": __("Filter Based On"),
		// 	"fieldtype": "Select",
		// 	"options": ["Date Range", "Fiscal Year"],
		// 	"default": ["Date Range"],
		// 	"reqd": 1,
		// 	// "read_only": 1,
		// 	on_change: function() {
		// 		let filter_based_on = frappe.query_report.get_filter_value('filter_based_on');
		// 		frappe.query_report.toggle_filter_display('from_fiscal_year', filter_based_on === 'Date Range');
		// 		frappe.query_report.toggle_filter_display('to_fiscal_year', filter_based_on === 'Date Range');
		// 		frappe.query_report.toggle_filter_display('period_start_date', filter_based_on === 'Fiscal Year');
		// 		frappe.query_report.toggle_filter_display('period_end_date', filter_based_on === 'Fiscal Year');
		//
		// 		frappe.query_report.refresh();
		// 	}
		// },
		{
			"fieldname":"period_start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "depends_on": "eval:doc.filter_based_on == 'Date Range'"
		},
		{
			"fieldname":"period_end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "depends_on": "eval:doc.filter_based_on == 'Date Range'"
		},
		// {
		// 	"fieldname":"from_fiscal_year",
		// 	"label": __("Start Year"),
		// 	"fieldtype": "Link",
		// 	"options": "Fiscal Year",
		// 	"default": frappe.defaults.get_user_default("fiscal_year"),
		// 	"reqd": 1,
		// 	"depends_on": "eval:doc.filter_based_on == 'Fiscal Year'"
		// },
		// {
		// 	"fieldname":"to_fiscal_year",
		// 	"label": __("End Year"),
		// 	"fieldtype": "Link",
		// 	"options": "Fiscal Year",
		// 	"default": frappe.defaults.get_user_default("fiscal_year"),
		// 	"reqd": 1,
		// 	"depends_on": "eval:doc.filter_based_on == 'Fiscal Year'"
		// },
		{
			"fieldname": "periodicity",
			"label": __("Periodicity"),
			"fieldtype": "Select",
			"options": [
				{ "value": "Monthly", "label": __("Monthly") },
				{ "value": "Quarterly", "label": __("Quarterly") },
				{ "value": "Half-Yearly", "label": __("Half-Yearly") },
				{ "value": "Yearly", "label": __("Yearly") }
			],
			"default": "Yearly",
			"hidden": 1,
			"reqd": 1
		},
		// Note:
		// If you are modifying this array such that the presentation_currency object
		// is no longer the last object, please make adjustments in cash_flow.js
		// accordingly.


		// {
		// 	"fieldname": "presentation_currency",
		// 	"label": __("Currency"),
		// 	"fieldtype": "Select",
		// 	"options": erpnext.get_presentation_currency_list()
		// },
		{
			"fieldname": "cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"get_query": function() {
				return {
					"filters": {
						company: frappe.query_report.get_filter_value("company"),
						is_group: 1,
						disabled: 0
					}
				}
			}
		},
		// {
		// 	"fieldname": "project",
		// 	"label": __("Project"),
		// 	"fieldtype": "MultiSelectList",
		// 	get_data: function(txt) {
		// 		return frappe.db.get_link_options('Project', txt);
		// 	}
		// },
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"hidden": 1,
			"default": 1
		},
	]
};