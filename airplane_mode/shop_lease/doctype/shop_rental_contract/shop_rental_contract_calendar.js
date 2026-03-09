// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.views.calendar["Shop Rental Contract"] = {
    field_map: {
		"id": "name",
		"title": "airport_shop",
		"start": "effective_date",
		"end": "expiry_date",
		"status": "status",
		"allDay": 1
	},
    gantt: {
		order_by: "effective_date"
	}
};