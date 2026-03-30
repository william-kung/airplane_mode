// Copyright (c) 2026, DDR and contributors
// For license information, please see license.txt

frappe.query_reports["Flights by Crew Member"] = {
    filters: [
        {
            "fieldname": "crew_name",
            "label": __("Crew Member"),
            "fieldtype": "Link",
            "options": "User",
            "mandatory": 0,
            get_query: ()=> {
                return {
                	query: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.get_crew_member_list",
                };
            }
        },
    ],
};