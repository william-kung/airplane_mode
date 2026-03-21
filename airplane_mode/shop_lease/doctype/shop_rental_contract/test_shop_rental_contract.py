# Copyright (c) 2026, DDR and Contributors
# See license.txt

import frappe
# from frappe.tests import IntegrationTestCase
from frappe.tests.utils import FrappeTestCase
from frappe.model.naming import getseries


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
# EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
# IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



# class IntegrationTestShopRentalContract(IntegrationTestCase):
# 	pass
	
class TestShopRentalContract(FrappeTestCase):

	def test_auto_name(self):
		test_contract = frappe.new_doc("Shop Rental Contract")
		test_contract.airport_shop = 'S-HKG-001'
		test_contract.tenant = "Family Mart"
		test_contract.effective_date = "2026-01-01"
		test_contract.expiry_date = "2027-01-31"
		test_contract.rent_amount = 249000
		test_contract.save()

		self.assertEqual(test_contract.name[:8], "HKG-S001")

