# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

from frappe.website.website_generator import WebsiteGenerator
from frappe.model.naming import getseries
import frappe



class AirportShop(WebsiteGenerator):
	def autoname(self):
		airport_code = self.airport_code
		shop_number = self.shop_number
		self.name = f"S-{airport_code}-{shop_number}"
