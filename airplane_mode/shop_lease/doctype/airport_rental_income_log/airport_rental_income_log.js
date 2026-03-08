// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Rental Income Log", {
    refresh(frm){
        
    },
	status(frm) {
        if (frm.doc.status == "Received") {
            frm.set_value('payment_received_date', new Date());
        } else {
            frm.set_value('payment_received_date', null);
        }
	},
});