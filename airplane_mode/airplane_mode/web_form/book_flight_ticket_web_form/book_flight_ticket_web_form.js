frappe.ready(function() {
	
    // frappe.web_form.on('trigger_field', (field, value) => {
    //     if (value) {
    //         // Fetch data from the reference DocType
    //         frappe.call({
    //             method: 'frappe.client.get_value',
    //             args: {
    //                 doctype: 'Reference DocType',
    //                 filters: { 'name': value },
    //                 fieldname: ['target_field_in_reference']
    //             },
    //             callback: function(r) {
    //                 if (r.message) {
    //                     // Update the Web Form field
    //                     frappe.web_form.set_value('target_field', r.message.target_field_in_reference);
    //                 }
    //             }
    //         });
    //     } else {
    //         // Clear the field if the trigger is empty
    //         frappe.web_form.set_value('target_field', '');
    //     }
    // });
})

