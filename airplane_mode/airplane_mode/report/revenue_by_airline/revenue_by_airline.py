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
	chart = get_chart(data)
	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
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
            (Ticket.docstatus == 1)  # 0 for draft; 1 for submitted; 2 for cancelled
        )
        .select(
            Airline.name.as_("airline"), 
            revenue
        )
        .groupby(Airline.name)
    )

    return query.run(as_dict=1)


def get_chart(data):
    if not data:
        return None

    # Filter out airlines with 0 revenue for a cleaner chart
    labels = [d.airline for d in data if d.revenue > 0]
    values = [d.revenue for d in data if d.revenue > 0]
    

    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}]
        },
        "type": "donut",
        "height": 250,
        "colors": ["#7cd6fd", "#743ee2", "#ff5858", "#ffa00a", "#1ed173"]
    }

def get_report_summary(data):
    if not data:
        return None

    total_revenue = sum(d.get("revenue", 0) for d in data)
    
    return [
        {
            "value": total_revenue,
            "indicator": "Green",
            "label": _("Total Revenue"),
            "datatype": "Currency",
        }
    ]