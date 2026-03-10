# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.model.naming import getseries
import frappe



class AirportShop(Document):
	def autoname(self):
		airport_code = self.airport_code
		shop_number = self.shop_number
		self.name = f"S-{airport_code}-{shop_number}"
