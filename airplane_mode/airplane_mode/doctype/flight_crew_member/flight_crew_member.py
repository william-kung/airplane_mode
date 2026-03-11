# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cached_property


class FlightCrewMember(Document):
    pass



    # @property
    # def flights(self):
    #     flight_names = frappe.get_all(
    #         "Flight Crew On Board",
    #         filters={"flight_crew_member": self.name},
    #         pluck="parent",
    #     )
    #     frappe.msgprint(flight_names)
    #     return frappe.get_all(
    #         "Airplane Flight",
    #         filters={"name": ["in", flight_names]},
    #         fields=["name", "source_airport_code", "destination_airport_code", "date_of_departure"],
    #     )

	# @frappe.whitelist()
	# def get_flights(self:dict | None = None):
	# 	frappe.msgprint(self.name)
	# 	flight_names = frappe.get_all(
	# 		"Flight Crew On Board",
	# 		filters={"flight_crew_member": self.name},
	# 		pluck="parent",
	# 	)
	# 	frappe.msgprint(flight_names[0])

	# 	flights = frappe.get_all("Airplaine Flight",
	# 		filters = {"name": {"in": flight_names}},
	# 		fields = ['name', 'source_airport_code', 'destination_airport_code', 'date_of_departure']
	# 	)

	# 	return flights