import frappe


def get_context(context):

	context.color = frappe.form_dict.param("color")


# Fetch 'color' from frappe.form_dict (query parameters)
# # Default to 'black' if the parameter is missing
# requested_color = frappe.local.form_dict.param("color")

# # Pass the variable to the Jinja context
# context.color = requested_color if requested_color else "black"

# # Optional: Set the page title dynamically
# context.title = f"Displaying {requested_color.capitalize()}"
