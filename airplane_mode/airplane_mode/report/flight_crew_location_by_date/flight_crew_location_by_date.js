// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.query_reports["Flight Crew Location by Date"] = {
	"filters": [
		{
			"fieldname": "reference_date",
			"label": __("Target Datetime"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		},
	],
};
