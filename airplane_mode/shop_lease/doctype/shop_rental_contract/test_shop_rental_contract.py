# Copyright (c) 2026, DDR and Contributors
# See license.txt

# from frappe.tests.utils import FrappeTestCase
import frappe
from frappe.tests import IntegrationTestCase


class IntegrationTestShopRentalContract(IntegrationTestCase):

	def test_auto_name(self):
		doc = frappe.get_doc({
            "doctype": "Shop Rental Contract",
            "airport_shop": "S-TPE-002",
            "tenant": "Family Mart",
            "effective_date": "2000-01-01",
            "expiry_date": "2000-01-31",
            "rent_per_square_meter": 5000,
            "area": 49.8,
            "rent_amount": 249000
        })
		doc.insert()
		self.assertEqual(doc.name[:8], "TPE-S002")
		print("doc.doctype:", doc.doctype)
		print("doc.name:", doc.name)
		db_check = frappe.db.exists(doc.doctype, doc.name, cache=True)
		print("db_check:", db_check)
		# self.assertTrue(db_check)

		# print(f"after running method: {doc.name}")

		# doc.save()
		# print(f"doc.name after change: {doc.name}")
		# doc.save()
		# self.assertEqual(doc.name[:8], "NRT-S002")
		# doc.delete()

		# test_contract = frappe.get_doc("Shop Rental Contract", doc.name)
		# test_contract.airport_shop = 'S-NRT-002'
		# test_contract.tenant = "Duty Free"
		# test_contract.effective_date = "2000-01-01"
		# test_contract.expiry_date = "2000-01-31"
		# test_contract.rent_per_square_meter = 5000
		# test_contract.area = 45
		# test_contract.rent_amount = 225000
		# test_contract.save()

		# self.assertEqual(test_contract.name[:8], "NRT-S002")
