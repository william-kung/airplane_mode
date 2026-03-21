# Copyright (c) 2026, DDR and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestFlightPassenger(IntegrationTestCase):
	def test_full_name_correctly_set(self):
		doc = frappe.get_doc({
			"doctype": "Flight Passenger",
			"first_name": "John",
			"last_name": "Doe",
			"date_of_birth": "1985-11-04"
		})
		doc.insert()
		self.assertEqual(doc.full_name, "John Doe")

	def test_full_name_correctly_set_with_no_last_name(self):
		doc = frappe.get_doc({
			"doctype": "Flight Passenger",
			"first_name": "John",
			"date_of_birth": "1985-11-04"
		})
		doc.insert()
		self.assertEqual(doc.full_name, "John")
