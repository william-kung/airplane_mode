# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_to_date, days_diff, getdate
from datetime import datetime 


class AirportRentalIncomeTracking(Document):
	def autoname(self):
		contract = frappe.db.get_value('Shop Rental Contract', 
			self.shop_rental_contract,
			['airport_code', 'shop_number'],
			as_dict=1
		)
		start_str = getdate(self.period_start).strftime('%Y%m%d')
		end_str = getdate(self.period_end).strftime('%Y%m%d')
		self.name = f"RIT-{contract.airport_code}-{str(contract.shop_number)}-{start_str}{end_str}"

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
		next_period_start = add_to_date(self.period_end, days=1, as_string=True)
		next_month = add_to_date(next_period_start, months=1, as_string=True)
		next_period_end = add_to_date(next_month, days=-1, as_string=True)
		doc = frappe.new_doc('Airport Rental Income Tracking')
		doc.shop_rental_contract = self.shop_rental_contract
		doc.period_start = next_period_start
		doc.period_end = next_period_end
		doc.insert()

	def is_expired(self):
		period_start = add_to_date(self.period_end, days=1, as_string=True)
		expiry_date = frappe.db.get_value('Shop Rental Contract', 
			self.shop_rental_contract,
			'expiry_date',
		)
		if days_diff(period_start, expiry_date) >= 0:
			return True
		else:
			return False
	

	
	@frappe.whitelist()
	def get_dates(self):
		dates = {}
		last_period_end = frappe.db.get_all(self.doctype,
			filters={
				'shop_rental_contract' : self.shop_rental_contract,
				'docstatus' : 1,
				'name': ['!=', self.name]
			},
			fields=['period_end'],
			order_by='period_end DESC'
		)
		# if there were submitted tracking doc (paid)
		if len(last_period_end) > 0:
			last_period_end = last_period_end[0].period_end
			start_date = add_to_date(last_period_end, days=1, as_string=True)
		# contract effective date as start day.
		else:
			start_date = frappe.db.get_value(
				'Shop Rental Contract',
				self.shop_rental_contract,
				'effective_date'
			)
		
		next_month = add_to_date(start_date, months=1, as_string=True)
		end_date = add_to_date(next_month, days=-1, as_string=True)
		dates = {
			'period_start': start_date.strftime('%Y-%m-%d'),
			'period_end': end_date
		}
		return dates
	

	