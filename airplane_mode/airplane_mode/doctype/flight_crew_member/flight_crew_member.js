// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Flight Crew Member", {
	refresh(frm) {
        frm.add_custom_button('Check Flights', () => {
            frappe.route_options = {"crew_name": frm.doc.name}
            frappe.set_route("query-report", "Flights by Crew Member")
        })
	}
});
