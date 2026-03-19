// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt


frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        // Add the button to the 'Actions' menu
        frm.add_custom_button(__("Assign Seat"), () => {
            // Call a helper function to keep the 'refresh' trigger clean
            show_seat_dialog(frm);
        }, __("Actions"));
        frm.page.set_indicator(`${frm.doc.status}`, get_status_color(frm.doc.status));
    }
});

function get_status_color(status) {
	const colors = {
		"Booked": "gray",
		"Checked-In": "purple",
		"Boarded": "green",  
	};
	return colors[status] || "gray";
}

function show_seat_dialog(frm) {
    let d = new frappe.ui.Dialog({
        title: __('Select Seat'),
        fields: [
            {
                label: __('Seat Number'),
                fieldname: 'seat_no',
                fieldtype: 'Data',
                reqd: 1 // V16 best practice: ensure data exists before assignment
            },
        ],
        size: 'small',  // small, large, extra-large
        primary_action_label: __('Assign'),
        primary_action(values) {
            // 1. Set value using API to ensure 'dirty' flag is set
            frm.set_value('seat', values.seat_no);
            
            // 2. Close dialog
            d.hide();
            
            // 3. Optional: Provide feedback (V16 UI enhancement)
            frappe.show_alert({
                message: __("Seat {0} assigned", [values.seat_no]),
                indicator: 'green'
            });
        }
    });

    d.show();
}
