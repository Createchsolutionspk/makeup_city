frappe.ui.form.on('Stock Reconciliation', {
    get_items: function (frm) {
		let fields = [
			{
				label: "Warehouse",
				fieldname: "warehouse",
				fieldtype: "Link",
				options: "Warehouse",
				reqd: 1,
				get_query: function () {
					return {
						filters: {
							company: frm.doc.company,
						},
					};
				},
			},
            {
				label: "Brand",
				fieldname: "brand",
				fieldtype: "Link",
				options: "Brand",
			},
			{
				label: "Item Code",
				fieldname: "item_code",
				fieldtype: "Link",
				options: "Item",
			},
			{
				label: __("Ignore Empty Stock"),
				fieldname: "ignore_empty_stock",
				fieldtype: "Check",
			},
		];

		frappe.prompt(
			fields,
			function (data) {
				frappe.call({
					method: "makeup_city.overrides.stock_reconciliation.get_items",
					args: {
						warehouse: data.warehouse,
						posting_date: frm.doc.posting_date,
						posting_time: frm.doc.posting_time,
						company: frm.doc.company,
                        brand: data.brand,
						item_code: data.item_code,
						ignore_empty_stock: data.ignore_empty_stock,
					},
                    freeze: true,
                    freeze_message: __("Wait while fetching items."),
					callback: function (r) {
                        if (r.exc || !r.message || !r.message.length) return;
                        console.log("r message")
						frm.clear_table("items");

						r.message.forEach((row) => {
							let item = frm.add_child("items");
							$.extend(item, row);

							item.qty = item.qty || 0;
							item.valuation_rate = item.valuation_rate || 0;
							item.use_serial_batch_fields = cint(
								frappe.user_defaults?.use_serial_batch_fields
							);
						});
						frm.refresh_field("items");
					},
				});
			},
			__("Get Items"),
			__("Update")
		);
	},
})