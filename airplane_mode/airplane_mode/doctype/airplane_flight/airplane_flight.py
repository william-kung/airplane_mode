# Copyright (c) 2026, DDR and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import getdate, add_to_date




class AirplaneFlight(WebsiteGenerator):
	
	def before_submit(self):
		self.status = "Completed"

	def validate(self):
		self.remove_duplcate_crew()

	def remove_duplcate_crew(self):
		seen_names = set()
		unique_names = []
		has_duplicates = False
		
		# Change 'self.crew_on_board' to 'self.crew_member'
		for crew in self.crew_member: 
			if crew.flight_crew_member not in seen_names:
				seen_names.add(crew.flight_crew_member)
				unique_names.append(crew)
			else:
				has_duplicates = True
				
		if has_duplicates:
			self.crew_member = unique_names # Update the correct field here too
			frappe.msgprint(
				msg=_("Duplicated crew members were removed."),
				title=_("Notice"),
				indicator="blue",
			)


	def on_update(self):
		if self.is_new():
			if self.is_ticket_related():
				frappe.enqueue(
					'airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.push_to_ticket',
					queue='short',
					flight = self
				)


	def is_ticket_related(self):
		# validate if the following ticket related fields are changed.  Avoid unnecessary DB operations.
		fields_to_check = [
			'source_gate_number',
			'source_airport_code',
			'destination_airport_code',
			'destination_gate_number',
			'date_of_departure',
			'time_of_departure',
			'duration',
		]
		old_doc = self.get_doc_before_save()
		if any(getattr(old_doc, field) != getattr(self, field) and # compare value before and after
			str(getattr(old_doc, field)) != str(getattr(self, field)) # compare string version of that value e.g. datetime, trigger action only if both are False.
			for field in fields_to_check):
			return True
		else:
			return False
			# if ticket related fields are changed push changes to ticket.
			
def push_to_ticket(flight):
	frappe.db.set_value(
		'Airplane Ticket',
		{'flight': flight.name},
		{
			'source_gate_number': flight.source_gate_number,
			'source_airport_code': flight.source_airport_code,
			'destination_airport_code': flight.destination_airport_code,
			'destination_gate_number': flight.destination_gate_number,
			'departure_date': flight.date_of_departure,
			'departure_time': flight.time_of_departure,
			'duration_of_flight': flight.duration,
		}
	)

@frappe.whitelist()
def get_events():

	events = frappe.get_all(
		"Airplane Flight",
		fields=["name", "date_of_departure", "duration", "source_airport_code", "destination_airport_code"],
		# filters=filters
	)


	processed_events = []
	for event in events:
		if event.date_of_departure and event.duration:
			start_datetime = getdate(f"{event.date_of_departure}")
			end_datetime = add_to_date(start_datetime, seconds=event.duration)			
			processed_events.append({
				"name": event.name,
				"doctype": "Airplane Flight",
				"start": start_datetime,
				"end": end_datetime,
				"title": f"{event.source_airport_code} -> {event.destination_airport_code} \n {event.name}",
				"allDay": 0
			})

	return processed_events


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_crew_member_list(doctype, txt, searchfield, start, page_len, filters):
    # Initialize base parameters
    params = {
        'txt': f"%{txt}%",
        'start': int(start),
        'page_len': int(page_len)
    }
    
    # Handle the excluded crew list using named parameters
    excluded_crew = filters.get("existing_crew") if filters else []
    exclude_condition = ""
    
    if excluded_crew:
        # Create unique keys for each excluded member to avoid positional conflicts
        exclude_keys = []
        for i, member in enumerate(excluded_crew):
            key = f"exclude_{i}"
            params[key] = member
            exclude_keys.append(f"%({key})s")
        
        # Build the NOT IN clause: AND tabUser.name NOT IN (%(exclude_0)s, %(exclude_1)s)
        exclude_condition = f"AND tabUser.name NOT IN ({', '.join(exclude_keys)})"

    query = f"""
        SELECT 
            tabUser.name, tabUser.full_name
        FROM 
            `tabUser`
        INNER JOIN 
            `tabHas Role` ON tabUser.name = `tabHas Role`.parent
        WHERE 
            `tabHas Role`.parenttype = 'User'
            AND `tabHas Role`.role = 'Flight Crew Member'
            AND tabUser.enabled = 1
            {exclude_condition}
            AND (tabUser.name LIKE %(txt)s OR tabUser.full_name LIKE %(txt)s)
        LIMIT %(start)s, %(page_len)s
    """

    return frappe.db.sql(query, params)