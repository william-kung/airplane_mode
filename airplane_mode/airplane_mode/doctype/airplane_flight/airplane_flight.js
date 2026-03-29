// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	refresh(frm) {
        frm.page.set_indicator(`${frm.doc.status}`, get_status_color(frm.doc.status));
	},
	setup: (frm)=> {
        frm.set_query('flight_crew_member', 'crew_member', ()=> {
            return {
                query: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.get_crew_member_list"
            };
        });
    }
});

function get_status_color(status) {
	const colors = {
		"Scheduled": "green",
        "Completed": "gray",
        "Cancelled": "red", 
	};
	return colors[status] || "gray";
}