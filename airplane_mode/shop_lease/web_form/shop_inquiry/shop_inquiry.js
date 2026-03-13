frappe.ready(function () {
	// validate if phone number or email exists
	frappe.web_form.validate = () => {
		let data = frappe.web_form.get_values();
		if (data.email == "" || data.phone_number == '') {
			frappe.msgprint(_("Please provide either email or phone number."))
			return false;
		}
	};

	// set airport_shop field
	const url_params = new URLSearchParams(window.location.search);
	if (url_params.has('airport_shop')) {
		frappe.web_form.set_value('airport_shop', url_params.get('airport_shop'));
	}

	// TODO: lookup location based on user's IP and set phone country code
	$.getJSON('https://ipapi.co/json/', function (data) {
		if (data && data.country_calling_code) {
			const prefix = data.country_calling_code + "-";  // e.g. "+886"
			const field = frappe.web_form.get_field('phone_number');
			if (field && field.$wrapper) {
				field.set_value(prefix);
				// Manually trigger a change event so Frappe's internal listeners pick up the new value
				field.$input.trigger('change');
			}
		}
	}).fail(function () {
		console.log("Phone country code lookup failed. Defaulting to manual entry.");
	});

})



