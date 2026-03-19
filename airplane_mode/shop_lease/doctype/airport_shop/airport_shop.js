// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
	refresh(frm) {
        frm.add_custom_button(__('Check Availability'), function() {
            frappe.route_options = {'airport_shop': frm.doc.name}
            frappe.set_route('query-report', 'Shop Lease by Date')
        }, __("Actions"));
        frm.add_custom_button(__('Add New Shop Lease'), function() {
            frappe.new_doc('Shop Rental Contract', {
                airport_shop: frm.doc.name
            });
        }, __("Actions"));
    }
});
