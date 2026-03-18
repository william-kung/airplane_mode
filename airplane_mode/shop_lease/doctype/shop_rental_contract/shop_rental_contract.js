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
        };
        frm.add_custom_button(__("Add Income Tracking Record"),()=>{
            frappe.new_doc("Airport Rental Income Tracking", {
                "shop_rental_contract": frm.doc.name
            });
        })
	},
    calculate_rent_amount(frm){      
        const rent_per_square_meter = frm.doc.rent_per_square_meter;
        const area = frm.doc.area;
        const rent_amount = rent_per_square_meter * area;
        frm.set_value("rent_amount", rent_amount);
    },
    effective_date(frm){
        if (!frm.doc.expiry_date) {
            const d = new Date(frm.doc.effective_date);
            d.setYear(d.getFullYear() + 1);
            d.setDate(d.getDate() - 1)
            frm.set_value("expiry_date", d);
        }
    },

    
    
});
