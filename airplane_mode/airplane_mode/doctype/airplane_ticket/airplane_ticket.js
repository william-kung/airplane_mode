// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        if (frm.doc.status !== "Booked") {
            frm.add_custom_button("Accept", ()=>{
                // console.log("button pressed");
                console.log(frm.doc.passenger);
                // for (d in frm.doc) {
                //     console.log(d);
                // }
                // // status => Booked
                // frm.set_value("status", "Booked");
                // frm.save();
                // save the form
            })
        }
	},
    status(frm) {
        frm.refresh();
    }
});
