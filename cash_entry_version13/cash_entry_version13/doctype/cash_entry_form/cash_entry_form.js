// Copyright (c) 2024, abdul basit ali and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Entry Form', {
	// refresh: function(frm) {

	// }
	setup(frm) {
		frm.set_query("cashbank", function() {
			return {
				filters: [
					['Account', 'account_type', 'in', 'Cash, Bank']
				]
			};
		});
	},
});
