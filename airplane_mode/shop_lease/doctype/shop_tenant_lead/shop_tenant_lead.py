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
		organisation_code = str(self.organisation_name).replace(" ", "")[:8].upper()
		contact_code = str(self.contact_name).replace(" ", "")[:8].upper()
		prefix = f"LD-{date_str}-{organisation_code}-{contact_code}"
		index = getseries(prefix, 2)
		self.name = f"{prefix}-{index}"
	
	def validate(self):
		if self.email == None and self.phone_number == None:
			frappe.throw(
				msg=_("Please enter at least either email or phone number."),
				title=_("Error"),
			)
