frappe.ui.form.on('Stock Entry', {
	refresh(frm) {
		if (frm.is_dirty() || frm.is_new()) {
			set_source_warehouse(frm);
			set_warehouses(frm);
		}

		if (!frm.is_new() && frm.doc.docstatus === 0) {
            frm.add_custom_button("Submit in Background", () => {
                frappe.call({
                    method: "makeup_city.utils.submit_se_in_background",
                    args: { docname: frm.doc.name },
                    freeze: true,
                    freeze_message: "Queuing submission…",
                    callback: (r) => {
                        if (!r.exc) {
                            frappe.msgprint("Stock Entry submission has been queued in the background.");
                        }
                    }
                });
            });
			frm.change_custom_button_type('Submit in Background', null, 'warning');
        }
	},
	custom_stock_transfer_entry(frm) {
		set_source_warehouse(frm);
	},
	stock_entry_type(frm) {
		set_warehouses(frm);
	}
});

let set_source_warehouse = function(frm) {
	if (frm.doc.custom_stock_transfer_entry == 'Shop to Shop Transfer' || 
		frm.doc.custom_stock_transfer_entry == 'Shop to Warehouse Transfer') {
		setTimeout(() => {
			frappe.call('frappe.client.get', {
				doctype: 'User',
				name: frappe.session.user
			}).then(response => {
				const roles = response.message.roles.map(role => role.role);
	
				if (roles.includes('branch user')) {
					let branch_user = true;
					if (branch_user) {
						frappe.call({
							method: "makeup_city.api.client.get_pos_profile",
							args: {
								user: frappe.session.user
							},
							callback: function(r) {
								if (r.message) {
									frm.set_value('from_warehouse', r.message[0]?.warehouse);
									frm.refresh_field("from_warehouse");
									frm.set_df_property('from_warehouse', 'read_only', 1);
				
									frm.set_query("from_warehouse", () => {
										return {
											filters: {
												name: r.message[0]?.warehouse
											}
										}
									});
								}
							}
						});	
					}
				}
			});
		}, 10);
	}
}

let set_warehouses = function(frm) {
	if (frm.doc.stock_entry_type == "Material Transfer" && !(frappe.session.user == "Administrator") && frm.doc.custom_stock_transfer_entry !== "Shop to Warehouse Transfer" && frm.doc.custom_stock_transfer_entry !== "Shop to Shop Transfer") {
		frm.set_query('from_warehouse', ()=> {
			return {
				filters: {
					parent_warehouse: "Warehouse - MC"
				}
			}
		});
		frappe.call({
			method: "makeup_city.api.client.get_pos_profile",
			args: {
				user: frappe.session.user
			},
			callback: function(r) {
				if (r.message) {
					frm.set_value('to_warehouse', r.message[0]?.warehouse);
					frm.refresh_field("to_warehouse");

					frm.set_query("to_warehouse", () => {
						return {
							filters: {
								name: r.message[0]?.warehouse
							}
						}
					})
				}
			}
		});	
	}
}