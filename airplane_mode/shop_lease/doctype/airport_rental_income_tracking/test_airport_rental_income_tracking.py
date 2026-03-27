# Copyright (c) 2026, DDR and Contributors
# See license.txt

import frappe
from frappe.utils import getdate, today, add_to_date
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


def make_test_records():
	if frappe.flags.test_records_created:
		return
	
	test_data = [
		{
			"doctype": "Airport Tenant",
			"tenant_name": "_test Tenant",
			"email": "watsonkingman@gmail.com"
		},
		{
			"doctype": "Airport",
			"name": "_test Airport",
			"code": "ZZZ",
			"city": "Sim City",
			"country": "Heaven Not Hell"	
		},
		{
			"doctype": "Airline",
			"name": "_test_Airline",
			"headquarters": "_test Headquarter",
			"customer_care_number": "+852 1234 5678"
		}, 
		{
			"doctype": "Flight Passenger",
			"first_name": "John",
			"last_name": "Doe",
			"date_of_birth": "2000-01-01",
		},
		{
			"doctype": "Airplane",
			"model": "A388",
			"airline": "_test_Airline",
			"capacity": 200
		},
		{
			"doctype": "Airport Shop",
			"airport": "_test Airport",
			"shop_number": "000",
			"shop_type": "Normal",
			"area": 50
		},
		{
			"doctype": "Airport Shop",
			"airport": "_test Airport",
			"shop_number": "999",
			"shop_type": "Normal",
			"area": 50
		},
	]
	
	if not frappe.db.exists("Shop Type", "Normal"):
		frappe.get_doc({"doctype": "Shop Type", "name": "Normal"}).insert()
	
	for entry in test_data:

		if not frappe.db.exists(entry):
			doc = frappe.get_doc(entry)
			doc.insert()
	
	create_submittted_contracts()
	frappe.flags.test_records_created = True


def create_submittted_contracts():
	if frappe.flags.submitted_contracts_created:
		return
	
	frappe.get_doc({
		"doctype": "Shop Rental Contract",
		"airport_shop": "S-ZZZ-999",
		"tenant": frappe.db.get_value("Airport Tenant", {"tenant_name": "_test Tenant"}, ["name"]),
		"effective_date": today(),
		"expiry_date": add_to_date(today(), years=1),
		"rent_per_square_meter": 5000,
		"rent_amount": 250000
	}).insert().submit()
	frappe.get_doc({
		"doctype": "Shop Rental Contract",
		"airport_shop": "S-ZZZ-000",
		"tenant": frappe.db.get_value("Airport Tenant", {"tenant_name": "_test Tenant"}, ["name"]),
		"effective_date": today(),
		"expiry_date": add_to_date(today(), years=1),
		"rent_per_square_meter": 5000,
		"rent_amount": 250000
	}).insert().submit()
	frappe.flags.submitted_contracts_created = True


class IntegrationTestAirportRentalIncomeTracking(IntegrationTestCase):

	def test_autocreate_income_tracking_on_submit(self):
		make_test_records()
		self.assertTrue(frappe.db.exists("Airport Rental Income Tracking", {
			'docstatus': 0,
			'shop_rental_contract': ['like', 'ZZZ-S999-_TEST%']
		}))

	def test_periods_before_and_after_submit(self):
		make_test_records()
		doc = frappe.get_doc("Airport Rental Income Tracking",{
			'docstatus': 0,
			'shop_rental_contract': ['like', 'ZZZ-S999-_TEST%']
		})
		self.assertEqual(getdate(doc.period_start), getdate(today()))
		self.assertTrue(getdate(doc.period_end) == getdate(add_to_date(today(), months=1, days=-1)))

		doc.status = "Received"
		doc.payment_received_date = today()
		doc.save().submit()
		self.assertTrue(doc.docstatus == 1)
		new_doc = frappe.get_doc("Airport Rental Income Tracking",{
			'docstatus': 0,
			'shop_rental_contract': ['like', 'ZZZ-S999-_TEST%']
		})
		self.assertTrue(getdate(new_doc.period_start) == getdate(add_to_date(doc.period_start, months=1)))
		self.assertTrue(getdate(new_doc.period_end) == getdate(add_to_date(doc.period_start, months=2, days=-1)))

	
	def test_do_not_create_next_period_on_expiring_contract(self):
		make_test_records()
		doc = frappe.get_doc("Airport Rental Income Tracking",{
			'docstatus': 0,
			'shop_rental_contract': ['like', 'ZZZ-S000-_TEST%']
		})
		doc.period_start = add_to_date(doc.period_start, months = 12)
		doc.period_end = add_to_date(doc.period_end, months = 13, days = -1)
		doc.status = "Received"
		doc.payment_received_date = doc.period_start
		doc.save().submit()
		self.assertFalse(frappe.db.exists("Airport Rental Income Tracking",{
			'docstatus': 0,
			'shop_rental_contract': ['like', 'ZZZ-S000-_TEST%']
		}))
		



	



