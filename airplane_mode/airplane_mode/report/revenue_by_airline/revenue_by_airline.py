# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

# import frappe
from frappe import _
import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum, Coalesce


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
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "link",
			"options": "Airline",
			"width": 250,
		},
		{
			"label": _("Revenue"),
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"width": 180,

		},
	]


def get_data() -> list[dict]:

    # 1. Define DocTypes
    Airline = frappe.qb.DocType("Airline")
    Airplane = frappe.qb.DocType("Airplane")
    Flight = frappe.qb.DocType("Airplane Flight")
    Ticket = frappe.qb.DocType("Airplane Ticket")

    # Use Coalesce to turn NULL values into 0 for the report
    revenue = Coalesce(Sum(Ticket.total_amount), 0).as_("revenue")

    # 2. Build the query starting from Airline
    query = (
        frappe.qb.from_(Airline)
        .left_join(Airplane).on(Airplane.airline == Airline.name)
        .left_join(Flight).on(Flight.airplane == Airplane.name)
        .left_join(Ticket).on(
            (Ticket.flight == Flight.name) & 
            (Ticket.docstatus == 1)
        )
        .select(
            Airline.name.as_("airline"), 
            revenue
        )
        .groupby(Airline.name)
    )

    return query.run(as_dict=1)