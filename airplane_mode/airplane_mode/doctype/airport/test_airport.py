# Copyright (c) 2026, DDR and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]

def create_airport():
	if frappe.flags.airports_created:
		return
	if not frappe.db.exists({
		"doctype": "Airport",
		"name": "Singapore Changi Airport",
	}):
		frappe.get_doc({
			"doctype": "Airport",
			"code": "SIN",
			"name": "Singapore Changi Airport",
			"city": "Singapore",
			"country": "Singapore"
		}).insert()
		
	frappe.flags.airports_created = True
		

class IntegrationTestShopType(IntegrationTestCase):
	# def setUp(self):
	# 	pass

	# def tearDown(self):
	# 	frappe.db.rollback()
	
	def test_airport_created(self):
		create_airport()
		db_exists = frappe.get_doc("Airport", "Singapore Changi Airport")
		self.assertTrue(db_exists != None)