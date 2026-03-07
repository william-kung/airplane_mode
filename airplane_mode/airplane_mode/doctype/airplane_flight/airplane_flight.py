# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _



class AirplaneFlight(WebsiteGenerator):
	def before_submit(self):
		self.status = "Completed"

	def on_update(self):
		self.push_changes_to_tickets()

	def push_changes_to_tickets(self):
		tickets = frappe.db.get_list(
			'Airplane Ticket', 
			pluck='name',
			filters={
				'flight': self.name
			})
		for t in tickets:
			doc = frappe.get_doc('Airplane Ticket', t)
			# doc.source_airport_code = self.source_airport_code
			# doc.source_gate_number = self.source_gate_number
			# doc.destination_airport_code = self.destination_airport_code
			# doc.destination_gate_number = self.destination_gate_number
			# doc.departure_date = self.date_of_departure
			# doc.departure_time = self.time_of_departure
			# doc.duration_of_flight = self.duration
			doc.save()
		frappe.msgprint(f"{len(tickets)} tickets was updated")
