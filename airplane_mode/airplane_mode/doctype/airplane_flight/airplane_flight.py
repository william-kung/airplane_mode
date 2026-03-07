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
		# validate if the following ticket related fields are changed.  Avoid unnecessary DB operations.
		fields_to_check = [
			'source_gate_number',
			'source_airport_code',
			'destination_airport_code',
			'destination_gate_number',
			'date_of_departure',
			'time_of_departure',
			'duration',
		]
		old_doc = self.get_doc_before_save()
		if any(getattr(old_doc, field) != getattr(self, field) and # compare value before and after
			str(getattr(old_doc, field)) != str(getattr(self, field)) # compare string version of that value e.g. datetime, trigger action only if both are False.
			for field in fields_to_check): 
			# if ticket related fields are changed push changes to ticket.
			tickets = frappe.db.get_list(
				'Airplane Ticket', 
				pluck='name',
				filters={
					'flight': self.name
				})
			# Open and save Airplane Ticket doctype to trigger the update of all related fields.
			for t in tickets:
				doc = frappe.get_doc('Airplane Ticket', t)
				doc.save()
			frappe.msgprint(f"{len(tickets)} tickets was updated")
