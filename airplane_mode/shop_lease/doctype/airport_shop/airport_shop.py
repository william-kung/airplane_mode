# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

from frappe.website.website_generator import WebsiteGenerator
from frappe.model.naming import getseries
import frappe



class AirportShop(WebsiteGenerator):
	def autoname(self):
		if not self.airport_code:
			self.airport_code = frappe.db.get_value("Airport", self.airport, "code")
		airport_code = self.airport_code
		shop_number = self.shop_number
		self.name = f"S-{airport_code}-{shop_number}"

	def validate(self):
		if self.area <= 0:
			frappe.throw("Area must be greater than 0")
