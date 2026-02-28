# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def before_submit(self):
		self.status = "Completed"
