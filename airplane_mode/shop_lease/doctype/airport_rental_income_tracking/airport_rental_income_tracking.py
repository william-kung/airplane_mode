# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, add_months, getdate


class AirportRentalIncomeTracking(Document):
	def autoname(self):
		contract = frappe.db.get_value('Shop Rental Contract', 
			self.shop_rental_contract,
			['airport_code', 'shop_number'],
			as_dict=1
		)
		start_str = self.period_start.replace('-', '')
		end_str = self.period_end.replace('-', '')
		self.name = f"RIT-{contract.airport_code}-{contract.shop_number}-{start_str}{end_str}"

	def before_submit(self):
		if self.status != "Received":
			frappe.throw(_('Document can only be submitted after payment received.'))

	def before_validate(self):
		if not self.period_start or not self.period_end:
			dates = self.get_dates()
			self.period_start = dates.get("period_start")
			self.period_end = dates.get("period_end")

	def on_submit(self):
		if self.is_expired():
			frappe.msgprint(
				msg="No new income tracking period was created.", 
				title="Contract will expire in next month",
				indicator="red"
			)
			return	
		else:
			self.create_next_period()


	def create_next_period(self):
		next_period_start = add_days(self.period_end, 1)
		next_month = add_months(next_period_start, 1)
		next_period_end = add_days(next_month, -1)
		doc = frappe.new_doc('Airport Rental Income Tracking')
		doc.shop_rental_contract = self.shop_rental_contract
		doc.period_start = next_period_start
		doc.period_end = next_period_end
		doc.insert()

	def is_expired(self):
		next_period_start = add_days(self.period_end, 1)
		period_start = getdate(next_period_start)
		expiry_date = getdate(frappe.db.get_value('Shop Rental Contract', 
			self.shop_rental_contract,
			'expiry_date',
		))
		if period_start >= expiry_date:
			return True
		else:
			return False


	## get
	@frappe.whitelist()
	def get_dates(self):
		dates = {}
		last_period_end = frappe.db.get_value(self.doctype,
			filters={
				'shop_rental_contract' : self.shop_rental_contract,
				'docstatus' : 1,
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
	

	