# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime


class ShopRentalContract(Document):
	def validate(self):
		self.check_rent_amount()
		self.check_dates()

	def check_dates(self):
		effective_date_status = is_overlap(self.effective_date, self.airport_shop),
		expiry_date_status = is_overlap(self.expiry_date, self.airport_shop)
		if effective_date_status == "Deny" or expiry_date_status == "Deny":
			frappe.throw(
				title=_("Error"),
				msg=_("Request denied.  This period is overlapping with another lease.  Please select another Airport Shop or amend Effective Date and Expiry Date")
			)
		if effective_date_status == "Warning" or expiry_date_status == "Warning":
			frappe.msgprint(
				title=_("Warning"),
				msg=_("⚠️There is another potential contract overlapping this period.  Please resolve conflict before submit!"),
				indicator="orange"
			)

	# make sure rental amount equals rate * area
	def check_rent_amount(self):
		rate = self.rent_per_square_meter
		area = self.area

		rent_amount = rate * area
		if self.rent_amount != rent_amount:
			frappe.throw(
				title="Error",
				msg="Please check Rent Amount."
			)
	

@frappe.whitelist()
def is_overlap(date, airport_shop):
	date = get_datetime(date)
	contracts = frappe.db.get_list("Shop Rental Contract",
		filters={
			'airport_shop': airport_shop,
		},
		fields=['effective_date', 'expiry_date', 'docstatus']
	)
	for contract in contracts:
		
		start_date = get_datetime(contract.effective_date)
		end_date = get_datetime(contract.expiry_date)
		
		if date >= start_date and date <= end_date:
			if contract.docstatus == 1:
				return "Deny"
			if contract.docstatus == 0:		
				return "Warning"
		else:
			return "Pass"



