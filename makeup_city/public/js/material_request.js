frappe.ui.form.on('Material Request', {
	refresh(frm) {
		if (frm.is_new() || frm.is_dirty()) {
			if (frm.doc.material_request_type == "Material Transfer" && !(frappe.session.user=="Administrator")) {
				frm.set_query('set_from_warehouse', ()=> {
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
							frm.set_value('set_warehouse', r.message[0]?.warehouse);
							frm.refresh_field("set_warehouse");

							frm.set_query("set_warehouse", () => {
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
			frm.set_query('custom_request_from', () => {
				return {
					filters: {
						custom_type: 'Request'
					}
				};
			});	
		}
		
	},

	onload: function(frm) {
		if (frm.doc.docstatus == 1) {
			setTimeout(() => {
				frappe.call('frappe.client.get', {
					doctype: 'User',
					name: frappe.session.user
				}).then(response => {
					const roles = response.message.roles.map(role => role.role);
		
					if (roles.includes('branch user')) {
						frm.remove_custom_button('Pick List', 'Create');
						frm.remove_custom_button('Material Transfer', 'Create');
						frm.remove_custom_button('Material Transfer (In Transit)', 'Create');
						frm.remove_custom_button('Stop');
					} else {
						console.log('Access Denied for Branch User');
					}
				});
			}, 10);
		}
    },

	set_warehouse: function(frm) {
		if (frm.doc.material_request_type === "Material Transfer") {
			if(frm.doc.items) {
				const posting_date = frm.doc.transaction_date;
				const posting_time = frm.doc.custom_transaction_time;
				for (let idx in frm.doc.items) {
					let item = frm.doc.items[idx];
					if (!item.item_code) {
						return;
					};
					const warehouse = frm.doc.set_warehouse ? frm.doc.set_warehouse : item.warehouse;
					set_actual_qty(item.doctype, item.name, item.item_code, warehouse, posting_date, posting_time);
					// frm.refresh_field("items");
				}
			};

		}
	}
});

frappe.ui.form.on('Material Request Item', {
	item_code: function(frm, cdt, cdn) {
		if (frm.doc.material_request_type === "Material Transfer") {
			let item = frappe.get_doc(cdt, cdn);
			
			if (!item.warehouse) {
				return;
			};

			const posting_date = frm.doc.transaction_date, posting_time = frm.doc.custom_transaction_time;
			const warehouse = frm.doc.set_warehouse ? frm.doc.set_warehouse : item.warehouse;
			set_actual_qty(cdt, cdn, item.item_code, warehouse, posting_date, posting_time);
			frm.refresh_field("items");
		}
	}
})


let set_actual_qty = function(cdt, cdn, item_code, warehouse, posting_date, posting_time) {
	frappe.call({
		method: "makeup_city.events.stock_entry.get_item_stock_qty",
		args: {
		"item_code": item_code,
		"warehouse": warehouse,
		"posting_date": posting_date,
		"posting_time": posting_time
		},
		callback: (r) => {
			if(r.message >= 0) {
				frappe.model.set_value(cdt, cdn, "custom_target_actual_qty", r.message);
			}
		}
	})
}