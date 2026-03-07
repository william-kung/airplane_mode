# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import random

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt
from frappe.model.naming import getseries


class AirplaneTicket(Document):

	def validate(self):
		self.process_add_ons()

	def on_submit(self):
		self.only_boarded()

	def before_insert(self):
		self.if_flight_full()
		self.assign_seat()

	def autoname(self):
		self.prefix()
		index = getseries(self.prefix, 3)
		self.name = f"{self.prefix}{index}"
	
	def on_update(self):
		# if flight is changed, change doc id too.
		if self.get_doc_before_save():
			old_doc = self.get_doc_before_save() 
			if old_doc.flight != self.flight:
				self.prefix()
				index = getseries(self.prefix, 3)
				new_name = f"{self.prefix}{index}"
				frappe.rename_doc(self.doctype, old_doc.name, new_name)

	def prefix(self):
		flight = self.flight
		source_airport_code = self.source_airport_code
		destination_airport_code = self.destination_airport_code
		self.prefix = f'{flight}-{source_airport_code}-to-{destination_airport_code}-'
		

	def assign_seat(self):
		number = random.randint(0, 99)
		letter = random.choice("ABCDE")
		self.seat = f"{number}{letter}"

	def process_add_ons(self):
		seen_names = set()
		unique_items = []
		total_add_on_amount = 0
		has_duplicates = False

		for d in self.add_ons:
			if d.item not in seen_names:
				seen_names.add(d.item)
				unique_items.append(d)
				total_add_on_amount += d.amount
			else:
				has_duplicates = True

		# Update the document if duplicates were found
		if has_duplicates:
			self.add_ons = unique_items
			frappe.msgprint(
				msg=_("Duplicated items were removed."),
				title=_("Notice"),
				indicator="blue",
			)

		# Final calculation
		self.total_amount = flt(self.flight_price) + flt(total_add_on_amount)

	def only_boarded(self):
		if self.status != "Boarded":
			frappe.throw(_("Status must be 'Boarded' before submission."))
		pass

	def if_flight_full(self):
		# Get plane capacity
		flight = self.flight
		airplane = frappe.db.get_value("Airplane Flight", flight, "airplane")
		capacity = frappe.db.get_value("Airplane", airplane, "capacity")
		sold_count = frappe.db.count(self.doctype, {'flight': self.flight})
		if sold_count >= capacity:
			frappe.throw(f"The flight is full.")
