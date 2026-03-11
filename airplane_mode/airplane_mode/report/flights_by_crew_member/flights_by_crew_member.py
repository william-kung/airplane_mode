# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_datetime
from datetime import timedelta

def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Crew"),
			"fieldname": "crew_name",
			"fieldtype": "Data",
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
		},
		{
			"label": _("To"),
			"fieldname": "destination_code",
			"fieldtype": "Data",
		}
	]


# def get_data(filters: dict | None = None) -> list[list]:
def get_data() -> list[list]:


	# crew = filters.get('crew_name') if filters and filters.get('crew_name') else "C-Susanna-Wong-001"

	CrewsOnBoard = frappe.qb.DocType("Flight Crew On Board")
	Flights = frappe.qb.DocType("Airplane Flight")
	query = (frappe.qb.from_(CrewsOnBoard).inner_join(Flights).on(Flights.name == CrewsOnBoard.parent)
		.select(
			CrewsOnBoard.flight_crew_member.as_("crew_name"),
			CrewsOnBoard.parent.as_("flight"),
			Flights.source_airport_code.as_("source_code"),
			Flights.destination_airport_code.as_("destination_code"),
			Flights.date_of_departure.as_("departure_time"),
			Flights.duration.as_("duration")
		)
		.orderby(CrewsOnBoard.flight_crew_member, order=frappe.qb.asc)
		.orderby(Flights.date_of_departure, order=frappe.qb.asc)
		.run(as_dict=1)
	)
	for row in query:
		departure_time = get_datetime(row["departure_time"])
		duration_delta = timedelta(seconds=row["duration"] or 0)
		row["arrival_time"] = departure_time + duration_delta
	return query