# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_to_date, days_diff, getdate, today
# from datetime import datetime 


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

	# def validate(self):
	# 	if self.docstatus != 0 and self.status == "Received":

	# 		self.submit()


	def on_submit(self):
		if (self.status == "Received"): 
			frappe.enqueue(
				method=self.send_receipt_email,
				queue='default'
			)
			frappe.msgprint(
				_("Receipt is being sent to the tenant.")
			)
		if self.is_expired():
			frappe.msgprint(
				msg=_("No new income tracking period was created."), 
				title=_("Contract Expiring"),
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
		
		end_date = add_to_date(start_date, months=1, days=-1, as_string=True)
		dates = {
			'period_start': start_date,
			'period_end': end_date
		}
		return dates
	
	def send_receipt_email(self):
		recipient = frappe.db.get_value("Airport Tenant", self.tenant, "email")
		pdf_content = frappe.attach_print(
			doctype=self.doctype, 
			name=self.name,
			print_format="Airport Shop Rental Receipt",
			doc=self
		)
		if not recipient:
			frappe.log_error(
				title=_("Rental Receipt Email Failed"),
				message=_(f"Could not find email address for Tenant: {0}. Receipt: {1}").format(self.tenant, self.name)
			)
			return

		frappe.sendmail(
			recipients=[recipient],
			subject=_("Receipt for Rental Payment: {0} to {1}").format(self.period_start, self.period_end),
			message=_("Please find the rental receipt for period between {0} and {1} attached.").format(self.period_start, self.period_end),
			attachments=[pdf_content]
		)
		


# @frappe.whitelist()
# def enqueue_receipt_email():
# 	frappe.enqueue(
# 		method='airplane_mode.airplane_mode.doctype.airport_rental_income_tracking.airport_rental_income_tracking.send_receipt_email',
# 		queue='default'
# 	)