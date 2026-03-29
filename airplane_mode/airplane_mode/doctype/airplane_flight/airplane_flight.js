// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	refresh(frm) {
        frm.page.set_indicator(`${frm.doc.status}`, get_status_color(frm.doc.status));
	},
	onload(frm) {
        // Use onload or refresh to ensure the query is bound to the child table link
        frm.set_query("flight_crew_member", "crew_member", () => {
            // Collect existing names from the child table rows
            let existing_crew = (frm.doc.crew_member || [])
                .map(row => row.flight_crew_member)
                .filter(id => id);

            return {
                query: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.get_crew_member_list",
                filters: {
                    "existing_crew": existing_crew
                }
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