// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Rental Contract", {
	refresh(frm) {
        if(!frm.doc.rent_per_square_meter) {
            frappe.db.get_single_value("Airport Shop Rental Settings", "standard_rate")
            .then(val => {
                const standard_rate = val;
                frm.set_value("rent_per_square_meter", standard_rate);
            });
        }
	},
    calculate_rent_amount(frm){      
        const rent_per_square_meter = frm.doc.rent_per_square_meter;
        const area = frm.doc.area;
        const rent_amount = rent_per_square_meter * area;
        frm.set_value("rent_amount", rent_amount);
    }
});
