# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	return [
		{
			"label": _("Shop"),
			"fieldname": "shop",
			"fieldtype": "Link",
			"options": "Airport Shop",
			"width": 120,
		},
		{
			"label": _("Tenant"),
			"fieldname": "tenant",
			"fieldtype": "Link",
			"options": "Airport Tenant",
			"width": 120,
		},
		{
			"label": _("Effective Date"),
			"fieldname": "effective_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Expiry Date"),
			"fieldname": "expiry_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("DocStatus"),
			"fieldname": "docstatus",
			"fieldtype": "Status",
			"width": 100,
		},
		{
			"label": _("Contract"),
			"fieldname": "contract",
			"fieldtype": "Link",
			"options": "Shop Rental Contract",
			"width": 180,
		},
		

	]


def get_data(filters: dict | None = None) -> list[list]:
	if not filters:
		filters = {}
	else:
		filters = {"airport_shop": filters.get("airport_shop")}
    
	query = frappe.qb.get_query("Shop Rental Contract",
        fields=[
            "airport_shop as shop", 
            "tenant as tenant",
            "effective_date as effective_date",
            "expiry_date as expiry_date",
            "docstatus as docstatus",
            "name as contract"
        ],
		filters=filters,
		order_by="airport_shop asc, effective_date desc"
    )

	return query.run(as_dict=1)