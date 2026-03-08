# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AirportRentalIncomeLog(Document):
	def before_submit(self):
		if self.status != "Received":
			frappe.throw(_('Document can only be submitted after payment received.'))

