# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		total_add_on_amount = 0
		clean_list = remove_duplicate(self)
		has_duplicate(clean_list, self)
		for i in clean_list:
			total_add_on_amount += i.amount
		self.total_amount = self.flight_price + total_add_on_amount


def remove_duplicate(self):
	items = self.add_ons
	seen_names = set()
	unique_items = []

	for i in items:
		if i.item not in seen_names:
			unique_items.append(i)
			seen_names.add(i.item)
	print(unique_items)

	return unique_items


def has_duplicate(clean_list, self):
	if len(clean_list) < len(self.add_ons):
		self.add_ons = clean_list

		frappe.msgprint(
			msg="Duplicated items are removed.",
			title="Notice",
			indicator="blue",
		)
