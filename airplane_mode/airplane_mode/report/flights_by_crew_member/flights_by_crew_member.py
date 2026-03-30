# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_to_date
from datetime import timedelta



def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Crew"),
			"fieldname": "crew_name",
			"fieldtype": "Link",
            "options": "User",
            "width": 190
		},
		{
			"label": _("Flight"),
			"fieldname": "flight",
			"fieldtype": "Link",
			"options": "Airplane Flight"
		},
		{
			"label": _("Departure Time"),
			"fieldname": "departure_time",
			"fieldtype": "Datetime",
		},
		{
			"label": _("From"),
			"fieldname": "source_code",
			"fieldtype": "Data",
            "width": 70
		},
		{
			"label": _("To"),
			"fieldname": "destination_code",
			"fieldtype": "Data",
            "width": 70
		}
	]


def get_data(filters) -> list[dict]:
    filters = filters or {}

    # identify user permission
    user = frappe.session.user
    roles = frappe.get_roles(user)
    management_roles = ["Fleet Manager", "Airport Authority Personnel", "System Manager"]
    is_management = any(item in management_roles for item in roles)


    CrewDetail = frappe.qb.DocType("Flight Crew Member Detail")
    Flights = frappe.qb.DocType("Airplane Flight")
    HasRole = frappe.qb.DocType('Has Role')
    User = frappe.qb.DocType('User')


    # Initialize the query
    query = (
        frappe.qb.from_(HasRole)
        .where(HasRole.role == "Flight Crew Member")
        .inner_join(User).on(HasRole.parent == User.name)
        .where(
            (HasRole.parenttype == "User") &
            (User.enabled == 1)
        )
        .inner_join(CrewDetail).on(User.name == CrewDetail.flight_crew_member)
        .inner_join(Flights).on(CrewDetail.parent == Flights.name)
        .select(
            CrewDetail.flight_crew_member.as_("crew_name"),
            CrewDetail.parent.as_("flight"),
            Flights.source_airport_code.as_("source_code"),
            Flights.destination_airport_code.as_("destination_code"),
            Flights.date_of_departure.as_("departure_time"),
            Flights.duration.as_("duration")
        )
    )

    # Apple role filter
    if not is_management:
        query = query.where(CrewDetail.flight_crew_member == user)

    # Apply Filter conditionally to avoid errors
    if filters.get("crew_name"):
        query = query.where(CrewDetail.flight_crew_member == filters.get("crew_name"))

    # Apply Ordering
    query = (
        query.orderby(Flights.date_of_departure, order=frappe.qb.desc)
        .orderby(CrewDetail.flight_crew_member, order=frappe.qb.asc)
    )

    # Execute query
    data = query.run(as_dict=1)

    # 3. Data Processing
    # In V16, prefer using frappe.utils for date manipulations
    for row in data:
        if row.get("departure_time") and row.get("duration"):
            # Assuming duration is in seconds
            row["arrival_time"] = add_to_date(row["departure_time"], seconds=row["duration"])
        else:
            row["arrival_time"] = None

    return data

