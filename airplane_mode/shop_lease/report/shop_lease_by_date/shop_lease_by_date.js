frappe.query_reports["Shop Lease by Date"] = {
    "filters": [
        {
            "fieldname": "airport_shop",
            "label": __("Airport Shop"),
            "fieldtype": "Link",
            "options": "Airport Shop",
            "mandatory": 0,
            "default": ""
        }
    ]
};