// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.query_reports["Airport Shop Occupancy Report"] = {
	"filters": [
		{
			"fieldname": "reference_date",
			"label": __("As at Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		}
	]
};
