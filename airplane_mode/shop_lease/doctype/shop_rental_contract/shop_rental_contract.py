# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, add_days, add_months


class ShopRentalContract(Document):
	def validate(self):
		self.verify_rent_amount()
		self.check_overlap_dates()

	def on_submit(self):
		self.create_income_tracking()


	
	def check_overlap_dates(self):
		
		effective_date = getdate(self.effective_date)
		expiry_date = getdate(self.expiry_date)


		contracts = frappe.db.get_list("Shop Rental Contract",
			filters={
				'airport_shop': self.airport_shop,
			},
			fields=['name', 'effective_date', 'expiry_date', 'docstatus']
		)

		for c in contracts:
			if self.name == c.name:
				continue
			c_start = getdate(c.effective_date)
			c_end = getdate(c.expiry_date)
			
			if (effective_date >= c_start and effective_date <= c_end) or (expiry_date >= c_start and expiry_date <= c_end):
				if c.docstatus == 1:
					frappe.throw(
					title=_("Error"),
					msg=_("Request denied.  This period is overlapping with another lease.  Please select another Airport Shop or amend Effective Date and Expiry Date")
				)
				elif c.docstatus == 0:
					frappe.msgprint(
						title=_("Warning"),
						msg=_("⚠️There is another potential contract overlapping this period.  Please make sure you resolve conflict before submit."),
						indicator="orange"
					)
					break
				else:
					continue

	
	def create_income_tracking(self):
		doc = frappe.new_doc('Airport Rental Income Tracking')
		doc.shop_rental_contract = self.name
		doc.tenant = self.tenant
		doc.period_start = self.effective_date
		doc.period_end = add_days(add_months(self.effective_date, 1), -1)
		doc.amount = self.rent_amount
		doc.insert()
		frappe.msgprint("New Aiport Rental Income Tracking DocumentCreated")


	# make sure rental amount equals rate * area
	def verify_rent_amount(self):
		rate = self.rent_per_square_meter
		area = self.area

		rent_amount = rate * area
		if self.rent_amount != rent_amount:
			frappe.throw(
				title="Error",
				msg="Please check Rent Amount."
			)
	

