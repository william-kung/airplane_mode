# Copyright (c) 2026, DDR and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase



# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = ['Airport'] 
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]

def make_test_records():
	if frappe.flags.test_records_created:
		return
	
	test_data = [{
		"doctype": "Airport",
		"name": "_test Airport",
		"code": "ZZZ",
		"city": "Sim City",
		"country": "Heaven Not Hell"	
	}]
	for entry in test_data:

		if not frappe.db.exists(entry):
			doc = frappe.get_doc(entry)
			doc.insert()
	frappe.flags.test_records_created = True



def create_shop():	
	if frappe.flags.shops_created:
		return
	
	if not frappe.db.exists("Shop Type", "Normal"):
		frappe.get_doc({"doctype": "Shop Type", "name": "Normal"}).insert()

	frappe.get_doc({
		"doctype": "Airport Shop",
		"airport": "_test Airport",
		"shop_number": "999",
		"shop_type": "Normal",
		"area": 50,
		"is_published": 1
	}).insert()
	frappe.flags.shops_created = True


class IntegrationTestShopType(IntegrationTestCase):

	def setUp(self):
		pass

	# def tearDown(self):
	# 	frappe.db.rollback()


	def test_autoname(self):
		make_test_records()
		create_shop()
		doc = frappe.get_doc("Airport Shop", {
			"airport": "_test Airport",
			"shop_number": "999",
		})
		self.assertEqual(doc.name, "S-ZZZ-999")


	def test_airport_code(self):
		make_test_records()
		create_shop()
		doc = frappe.get_doc("Airport Shop", {
			"airport": "_test Airport",
			"shop_number": "999",
		})
		self.assertEqual(doc.airport_code, "ZZZ")