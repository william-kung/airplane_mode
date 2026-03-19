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
		order_by="airport_shop asc, expiry_date desc"
    )

	data = query.run(as_dict=True)

	if data == []:
		return [{"shop": filters.get("airport_shop"), "tenant": "n/a", "effective_date": None, "expiry_date": None, "docstatus": "n/a", "contract": "No Contract Found"}]


	return query.run(as_dict=1)