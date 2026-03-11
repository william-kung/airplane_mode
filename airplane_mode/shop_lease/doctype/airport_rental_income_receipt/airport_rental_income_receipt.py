# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, add_months


class AirportRentalIncomeReceipt(Document):
	def before_submit(self):
		if self.status != "Received":
			frappe.throw(_('Document can only be submitted after payment received.'))

	def before_validate(self):
		if not self.period_start or not self.period_end:
			dates = self.get_dates()
			self.period_start = dates.get("period_start")
			self.period_end = dates.get("period_end")

	@frappe.whitelist()
	def get_dates(self):
		dates = {}
		last_period_end = frappe.db.get_value(self.doctype,
			filters={
				'shop_rental_contract' : self.shop_rental_contract,
				'status' : 'Received',
				'name': ['!=', self.name]
			},
			fieldname='period_end',
			order_by='period_end DESC'
		)
		if last_period_end:
			start_date = add_days(last_period_end, 1)
		else:
			start_date = frappe.db.get_value(
				'Shop Rental Contract',
				self.shop_rental_contract,
				'effective_date'
			)
		
		next_month = add_months(start_date, 1)
		end_date = add_days(next_month, -1)
		dates = {
			'period_start': start_date,
			'period_end': end_date
		}
		return dates
	

	