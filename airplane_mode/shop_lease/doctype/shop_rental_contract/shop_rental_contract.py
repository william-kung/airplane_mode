# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopRentalContract(Document):
	def validate(self):
		self.validate_rent_amount()

	def validate_rent_amount(self):
		rate = self.rent_per_square_meter
		area = self.area

		rent_amount = rate * area
		if self.rent_amount != rent_amount:
			frappe.throw(
				title="Error",
				msg="Please check Rent Amount."
			)