# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import random

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class AirplaneTicket(Document):
	def validate(self):
		self.process_add_ons()

	def on_submit(self):
		self.only_boarded()

	def before_insert(self):
		self.assign_seat()

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
