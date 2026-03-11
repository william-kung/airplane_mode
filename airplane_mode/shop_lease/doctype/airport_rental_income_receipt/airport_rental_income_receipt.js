// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Rental Income Receipt", {
	shop_rental_contract(frm) {
		if (frm.doc.shop_rental_contract) {
			frm.call({
				method: "get_dates",
				doc: frm.doc,
				callback: function(r) {
					if (r.message) {
						frm.set_value("period_start", r.message.period_start);
						frm.set_value("period_end", r.message.period_end);
					}
				}
			});
		}
	},
	status(frm) {
        if (frm.doc.status == "Received") {
            frm.set_value('payment_received_date', frappe.datetime.now_date());
        } else {
            frm.set_value('payment_received_date', null);
        }
	},
});