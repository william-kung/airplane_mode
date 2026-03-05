// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
        if (frm.doc.website) {
            frm.sidebar.add_user_action(__('Visit Website'), () => {
                window.open(frm.doc.website, '_blank');
            });
        }
	}
});