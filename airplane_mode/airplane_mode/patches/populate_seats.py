import frappe


def execute():
	tickets = []
	tickets = frappe.db.get_all("Airplane Ticket", pluck="name")
	for t in tickets:
		ticket = frappe.get_doc("Airplane Ticket", t)
		ticket.assign_seat()
		# use ticket.db_update() instead of ticket.save() to bypass validations
		ticket.db_update()
