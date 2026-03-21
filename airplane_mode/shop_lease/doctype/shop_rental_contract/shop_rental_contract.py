# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import getseries, make_autoname
from frappe.utils import add_days, add_months, get_link_to_form, getdate


class ShopRentalContract(Document):
	def autoname(self):
		prefix = f"{self.airport_code}-S{self.shop_number}"
		self.name = make_autoname(f"{prefix}-.###")

	def validate(self):
		self.verify_rent_amount()
		self.check_overlap_dates()

	def on_submit(self):
		self.create_income_tracking()


	def on_update(self):
		if self.has_value_changed("airport_shop"):
			self.rename()
	
	def check_overlap_dates(self):
		base_filters = {
			'name': ['!=', self.name],
			'airport_shop': self.airport_shop,
		}
		or_filters = [
			["effective_date", "between", [self.effective_date, self.expiry_date]],
			["expiry_date", "between", [self.effective_date, self.expiry_date]]
		]

		overlapped = frappe.db.get_list("Shop Rental Contract",
			filters = base_filters,
			or_filters = or_filters,
			fields = ['docstatus'],
			order_by = "docstatus desc",
			limit = 1
		)

		if overlapped:
			if overlapped[0]["docstatus"] == 1:
				frappe.throw(
					title=_("Error"),
					msg=_("Request denied.  This period is overlapping with another lease.  Please select another Airport Shop or amend Effective Date and Expiry Date")
				)
			else:
				frappe.msgprint(
				title=_("Warning"),
				msg=_("⚠️There is another potential contract overlapping this period.  Please make sure you resolve conflict before submit."),
				indicator="orange"
			)
				
	def rename(self):
		new_prefix = f"{self.airport_code}-S{self.shop_number}"
		new_name = make_autoname(f"{new_prefix}-.###")
		frappe.rename_doc(self.doctype, self.name, new_name)


	@frappe.whitelist()
	def create_income_tracking(self):
		doc = frappe.new_doc('Airport Rental Income Tracking')
		doc.shop_rental_contract = self.name
		doc.tenant = self.tenant
		doc.period_start = self.effective_date
		doc.period_end = add_days(add_months(self.effective_date, 1), -1)
		doc.amount = self.rent_amount
		doc.status =self.get_status()
		doc.insert()
		msg = _("New Aiport Rental Income Tracking Document for {0} created.").format(frappe.bold(self.name))
		msg += "<br><br>" + _("Visit {0} for details.").format(get_link_to_form("Airport Rental Income Tracking", doc.name))
		title = _("Income Tracking Started")
		frappe.msgprint(msg=msg, title=title, indicator="green")


	# make sure rental amount equals rate * area
	def verify_rent_amount(self):
		rate = self.rent_per_square_meter
		area = self.area

		rent_amount = rate * area
		if self.rent_amount != rent_amount:
			frappe.throw(
				title=_("Error"),
				msg=_("Please check Rent Amount.")
			)


	def get_status(self):
		date = getdate(self.effective_date)
		if date <= date.today():
			return "Overdue"
		else:
			return "Pending"