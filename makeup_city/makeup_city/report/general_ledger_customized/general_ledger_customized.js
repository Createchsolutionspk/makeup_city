frappe.query_reports["General Ledger Customized"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "MultiSelectList",
			options: "Account",
			get_data: function(txt) {
				// Only allow these 4 accounts
				const allowed_accounts = [
					"1207001003 - Cash at POS - MUC - MC",
					"1207001004 - Cash at POS - BLS - MC",
					"1207001005 - Cash at POS - ST London - MC",
					"1207003001 - Petty Cash-i - MC"
				];

				return allowed_accounts
					.filter(account => account.toLowerCase().includes(txt.toLowerCase()))
					.map(account => ({ value: account, description: account }));
			}
		},
		{
			fieldname: "cost_center",
			label: __("Cost Center"),
			fieldtype: "Link",
			options: "Cost Center",
		},
	],

	onload: function () {
		frappe.query_report.allow_refresh_on_load = false;

		frappe.call({
			method: "makeup_city.makeup_city.report.general_ledger_customized.general_ledger_customized.get_cost_center_for_user",
			args: {
				user: frappe.session.user,
			},
			callback: function (r) {
				if (r.message) {
					frappe.query_report.set_filter_value("cost_center", r.message);
				
					const costCenterFilter = frappe.query_report.get_filter("cost_center");
					if (costCenterFilter) {
						costCenterFilter.df.read_only = 1;
						costCenterFilter.refresh();
						costCenterFilter.set_input_disabled(true);
					}
				
					setTimeout(() => {
						frappe.query_report.refresh();
					}, 300);
				} else {
					frappe.msgprint(__("No Cost Center found for this user in POS Profile."));
					// Clear the cost_center filter explicitly
					frappe.query_report.set_filter_value("cost_center", "");
				}
			}
		});
	}
};
