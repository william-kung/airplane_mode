// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Rental Income Tracking", {
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
	refresh(frm) {
		if (frm.doc.status == "Received" && frm.doc.docstatus == 0) {
			frappe.msgprint({
				title: __("Reminder"),
				message: __('Please be reminded to press Confirm Receipt to generate a receipt and send it to the customer by email.'),
			})
			frm.page.set_primary_action("Confirm Receipt", ()=>{
				frappe.msgprint({
					title: __("Confirmation"),
					message: __("Are you sure the payment was received? A receipt will be generated and sent to the customer by email.  This cannot be undone."
					),
					primary_action: {
						'label': __("Confirm"),
						'server_action': 'airplane_mode.shop_lease.doctype.airport_rental_income_tracking.airport_rental_income_tracking.send_receipt_email',
						action(){
							frm.save("Submit");
						}
					}
				})
			})
		}
		frm.page.set_indicator(`${frm.doc.status}`, get_status_color(frm.doc.status));
	}
});

function get_status_color(status) {
	const colors = {
		"Pending": "orange",
		"Overdue": "red",
		"Received": "gray",  
	};
	return colors[status] || "gray";

}