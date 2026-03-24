# Copyright (c) 2026, DDR and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.tests.utils import FrappeTestCase


EXTRA_TEST_RECORD_DEPENDENCIES = ["Airport Tenant"]  # eg. ["User"]
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
		}

	]
	if not frappe.db.exists("Shop Type", "Normal"):
		frappe.get_doc({"doctype": "Shop Type", "name": "Normal"}).insert()
	for entry in test_data:

		if not frappe.db.exists(entry):
			doc = frappe.get_doc(entry)
			doc.insert()
	frappe.flags.test_records_created = True

def create_contract ():
	if frappe.flags.contracts_created:
		return
	
	airport_shop = frappe.get_doc("Airport Shop",{
		"airport": "_test Airport",
		"shop_number": "000",
		"shop_type": "Normal",
		"area": 50
	}).name
	tenant = frappe.get_doc("Airport Tenant",{
		"tenant_name": "_test Tenant",
		"email": "watsonkingman@gmail.com"
	}).name

	frappe.get_doc({
		"doctype": "Shop Rental Contract",
		"airport_shop": airport_shop,
		"tenant": tenant,
		"effective_date": "2000-01-01",
		"expiry_date": "2000-01-31",
		"rent_per_square_meter": 5000,
		"rent_amount": 250000
	}).insert()
	frappe.flags.contracts_created = True

def amend_contract():		
	if not frappe.flags.contract_created:
		create_contract()
	if frappe.flags.contract_amended:
		return
	
	airport_shop_orginal = frappe.get_doc("Airport Shop",{
		"airport": "_test Airport",
		"shop_number": "000",
	}).name
	airport_shop_changed = frappe.get_doc("Airport Shop",{
		"airport": "_test Airport",
		"shop_number": "999",
	}).name
	tenant = frappe.get_doc("Airport Tenant",{
		"tenant_name": "_test Tenant",
		"email": "watsonkingman@gmail.com"
	}).name
	doc = frappe.get_doc("Shop Rental Contract",{
		"airport_shop": airport_shop_orginal,
		"tenant": tenant,
	})
	doc.airport_shop = airport_shop_changed
	doc.save()

	frappe.flags.contract_amended = True

# class TestEvent(FrappeTestCase):
# 	pass

class IntegrationTestShopRentalContract(IntegrationTestCase):

	def test_auto_name(self):
		make_test_records()
		create_contract()
		airport_shop = frappe.get_doc("Airport Shop",{
			"airport": "_test Airport",
			"shop_number": "000",
		}).name
		tenant = frappe.get_doc("Airport Tenant",{
			"tenant_name": "_test Tenant",
			"email": "watsonkingman@gmail.com"
		}).name
		doc = frappe.get_doc("Shop Rental Contract",{
			"airport_shop": airport_shop,
			"tenant": tenant
		})
		self.assertTrue(doc.name.startswith("ZZZ-S000-_TEST"))

	def test_auto_rename_after_contract_amended(self):
		make_test_records()
		amend_contract()		
		airport_shop = frappe.get_doc("Airport Shop",{
			"airport": "_test Airport",
			"shop_number": "999",
		}).name
		tenant = frappe.get_doc("Airport Tenant",{
			"tenant_name": "_test Tenant",
			"email": "watsonkingman@gmail.com"
		}).name
		doc = frappe.get_doc("Shop Rental Contract",{
			"airport_shop": airport_shop,
			"tenant": tenant
		})
		self.assertTrue(doc.name.startswith("ZZZ-S999-_TEST"))

	def test_create_income_tracking_on_submit(self):
		make_test_records()
		amend_contract()
		airport_shop = frappe.get_doc("Airport Shop",{
			"airport": "_test Airport",
			"shop_number": "999",
		}).name
		tenant = frappe.get_doc("Airport Tenant",{
			"tenant_name": "_test Tenant",
		}).name
		doc = frappe.get_doc("Shop Rental Contract",{
			"airport_shop": airport_shop,
			"tenant": tenant
		})
		doc.submit()
		
		new_exists = frappe.db.exists("Airport Rental Income Tracking", {
			'shop_rental_contract': doc.name,
			'tenant': doc.tenant,
			'period_start': doc.effective_date,
			'period_end': doc.expiry_date,
			'amount': doc.rent_amount
		})
		self.assertTrue(new_exists != None)

