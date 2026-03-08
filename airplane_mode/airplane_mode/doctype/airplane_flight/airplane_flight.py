# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, add_to_date




class AirplaneFlight(Document):
	def before_submit(self):
		self.status = "Completed"

	def validate(self):
		start = get_datetime(self.date_of_departure)
		if start and self.duration:
			self.flight_end = add_to_date(start, seconds=self.duration)


	def on_update(self):
		if self.is_ticket_related():
			frappe.enqueue(
				'airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.push_to_ticket',
				queue='short',
				flight = self
			)


	def is_ticket_related(self):
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
			return True
		else:
			return False
			# if ticket related fields are changed push changes to ticket.
			
def push_to_ticket(flight):
	frappe.db.set_value(
		'Airplane Ticket',
		{'flight': flight.name},
		{
			'source_gate_number': flight.source_gate_number,
			'source_airport_code': flight.source_airport_code,
			'destination_airport_code': flight.destination_airport_code,
			'destination_gate_number': flight.destination_gate_number,
			'departure_date': flight.date_of_departure,
			'departure_time': flight.time_of_departure,
			'duration_of_flight': flight.duration,
		}
	)
