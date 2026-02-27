import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


def execute():

	tickets = frappe.db.get_all("Airplane Ticket", pluck="name")
	for t in tickets:
		ticket = frappe.get_doc("Airplane Ticket", t)
		refactor_flight_field(ticket)


def refactor_flight_field(ticket):
	ticket.flight = new_flight_name(ticket.flight)
	ticket.db_update()
	# frappe.db.set_value("Airplane Ticket", ticket.name, flight_text)


def new_flight_name(original_flight):
	mapping = {
		"AirAsia-668": "AirAsia-668-02-2026-00010",
		"Nippon Airline-757": "Nippon Airline-757-02-2026-00012",
		"IndiGo-276": "IndiGo-276-02-2026-00011",
		"Cathay Pacific-344": "Cathay Pacific-344-02-2026-00016",
	}
	return mapping.get(original_flight, original_flight)
