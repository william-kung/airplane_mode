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
				const management_roles = ["Fleet Manager", "Airport Authority Personnel", "System Manager"]
				const is_management = frappe.user_roles.some(role => management_roles.includes(role));
				if (is_management) {
					return {
						query: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.get_crew_member_list",
					};
				} else {	
					return {
						query: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.get_crew_member_list",
						filters: {"name": frappe.session.user}
					};
            	}
			}
        },
    ],
	onload: function(report) {
        const management_roles = ["Fleet Manager", "Airport Authority Personnel", "System Manager"];
        const is_management = frappe.user_roles.some(role => management_roles.includes(role));

        if (!is_management) {
            // Disable the filter so they can't click the 'X' and search for others
            report.get_filter("crew_name").df.read_only = 1;
            report.get_filter("crew_name").refresh();
        }
    }
};