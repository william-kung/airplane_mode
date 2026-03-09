# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Count
from frappe.utils import getdate, today


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:

	return [
		{
			"label": _("Airport"),
			"fieldname": "airport",
			"fieldtype": "link",
			"options": "Airport",
			"width": 250,
		},
		{
			"label": _("All Shops"),
			"fieldname": "shop_count",
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"label": _("Leased"),
			"fieldname": "occupied_shop_count",
			"fieldtype": "Int",
			"width": 120,
		}
	]


def get_data(filters: dict | None = None) -> list[list]:

	# 1. Define DocTypes
	AirportShop = frappe.qb.DocType("Airport Shop")
	ShopRentalContract = frappe.qb.DocType("Shop Rental Contract")
	Airport = frappe.qb.DocType("Airport")

	reference_date = filters.get("reference_date") if filters and filters.get("reference_date") else today()
	reference_date = getdate(reference_date)

	# Condition for a shop to be considered occupied
	is_occupied = (
		(ShopRentalContract.docstatus == 1)
		& (reference_date >= ShopRentalContract.effective_date)
		& (reference_date <= ShopRentalContract.expiry_date)
	)

	# 2. Build the query
	query = (
		frappe.qb.from_(Airport)
		.left_join(AirportShop)
		.on(AirportShop.airport == Airport.name)
		.left_join(ShopRentalContract)
		.on((ShopRentalContract.airport_shop == AirportShop.name) & is_occupied)
		.select(
			Airport.name.as_("airport"),
			AirportShop.name.as_("shop_name"),
			Count(AirportShop.name).distinct().as_("shop_count"),
			Count(ShopRentalContract.airport_shop).distinct().as_("occupied_shop_count"),
			ShopRentalContract.effective_date.as_("effective_date"),
			ShopRentalContract.expiry_date.as_("expiry_date"),
		)
		.groupby(Airport.name)
	)
	return query.run(as_dict=1)
