import frappe
from frappe.model.naming import make_autoname


def execute():

	tickets = frappe.db.get_all("Airplane Ticket", pluck="name")
	for t in tickets:
		ticket = frappe.get_doc("Airplane Ticket", t)
		rename_doc(ticket)


def rename_doc(ticket):
	flight_text = new_flight_name(ticket.flight)
	source_code = ticket.source_airport_code
	destination_code = ticket.destination_airport_code
	prefix = f"{flight_text}-{source_code}-to-{destination_code}-"
	new_doc_name = make_autoname(f"{prefix}.###")
	frappe.rename_doc("Airplane Ticket", ticket.name, new_doc_name, force=True)


def new_flight_name(original_flight):
	mapping = {
		"AirAsia-668": "AirAsia-668-02-2026-00010",
		"Nippon Airline-757": "Nippon Airline-757-02-2026-00012",
		"IndiGo-276": "IndiGo-276-02-2026-00011",
		"Cathay Pacific-344": "Cathay Pacific-344-02-2026-00016",
	}
	return mapping.get(original_flight, original_flight)
