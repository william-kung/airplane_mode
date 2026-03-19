// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.query_reports["Flights by Crew Member"] = {
	filters: [
		{
			"fieldname": "crew_name",
			"label": __("Crew Member"),
			"options": "Flight Crew Member",
			"fieldtype": "Link",
			"mandatory": 0,
		},
	],
};
