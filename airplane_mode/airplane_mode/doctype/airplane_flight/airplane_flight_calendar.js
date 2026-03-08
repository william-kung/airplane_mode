frappe.views.calendar["Airplane Flight"] = {
	field_map: {
		"start": "start",
		"end": "end",
		"id": "name",
		"title": "title",
		"allDay": "allDay"
	},
	get_events_method: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.get_events"
};
