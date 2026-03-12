# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries
from frappe.utils import today
from frappe import _




class ShopTenantLead(Document):
	def autoname(self):
		date_str = today().replace("-", "")
		if not self.organisation_name or self.organisation_name == "":
			self.organisation_name = "NONE"
		organisation_code = str(self.organisation_name).replace(" ", "")[:8].upper()
		contact_code = str(self.contact_name).replace(" ", "")[:8].upper()
		prefix = f"LD-{date_str}-{organisation_code}-{contact_code}"
		index = getseries(prefix, 2)
		self.name = f"{prefix}-{index}"
	
	def validate(self):
		self.email = self.email.strip()
		self.phone_number = self.phone_number.strip()
		if (self.email == None or self.email == "") and (self.phone_number == None or self.phone_number == ""):
			frappe.throw(
				msg=_("Please enter at least either email or phone number."),
				title=_("Error"),
			)
