import frappe
from frappe import _
from frappe.utils import getdate, now
from datetime import timedelta

def execute(filters: dict | None = None):
    return get_columns(), get_data(filters), message

def get_columns() -> list[dict]:
    return [
         {
			"label": _("Crew Member"), 
			"fieldname": "crew_name", 
			"fieldtype": "Link", 
			"options": "Flight Crew Member"
        },
        {
            "label": _("Last Flight"), 
			"fieldname": "flight", 
            "fieldtype": "Link", 
			"options": "Airplane Flight"
        },
        {
            "label": _("Arrival Time"), 
            "fieldname": "arrival_time", 
            "fieldtype": "Datetime"
        },
        {
            "label": _("Destination"), 
			"fieldname": "destination_code", 
            "fieldtype": "Data"
        },
    ]

# def get_data(filters: dict | None = None) -> list[dict]:

#     ref_date = filters.get("reference_date") if filters and filters.get("reference_date") else now()
#     ref_date = get_datetime(ref_date)

#     CrewsOnBoard = frappe.qb.DocType("Flight Crew On Board")
#     Flights = frappe.qb.DocType("Airplane Flight")

#     query = (
#         frappe.qb.from_(CrewsOnBoard)
#         .inner_join(Flights).on(Flights.name == CrewsOnBoard.parent)
#         .select(
#             CrewsOnBoard.flight_crew_member.as_("crew_name"),
#             CrewsOnBoard.parent.as_("flight"),
#             Flights.destination_airport_code.as_("destination_code"),
#             Flights.date_of_departure.as_("departure_time"),
#             Flights.duration.as_("duration")
#         )
#         .where(Flights.date_of_departure <= ref_date)
# 		.orderby(Flights.date_of_departure, order=frappe.qb.desc)
#         .groupby(CrewsOnBoard.flight_crew_member)
# 	)

#     raw_data = query.run(as_dict=1)
    
#     for d in raw_data:
#         departure_time = get_datetime(d["departure_time"])
#         duration_delta = timedelta(seconds=d["duration"] or 0)
#         arrival_time = departure_time + duration_delta
#         d["arrival_time"] = arrival_time
    
#     return raw_data


def get_data(filters: dict | None = None) -> list[dict]:

    ref_date = filters.get("reference_date") if filters and filters.get("reference_date") else now()
    ref_date = getdate(ref_date)


    CrewsOnBoard = frappe.qb.DocType("Flight Crew On Board")
    Flights = frappe.qb.DocType("Airplane Flight")

	
    onboard_flights = (
		frappe.qb.from_(CrewsOnBoard)
		.inner_join(Flights).on(Flights.name == CrewsOnBoard.parent)
		.select(
			CrewsOnBoard.flight_crew_member.as_("crew_name"),
			CrewsOnBoard.parent.as_("flight"),
			Flights.destination_airport_code.as_("destination_code"),
			Flights.date_of_departure.as_("departure_time"),
			Flights.duration.as_("duration")
		)
		.orderby(Flights.date_of_departure, order=frappe.qb.asc)
		.run(as_dict=1)
	)
    data = []
    crew_list = frappe.db.get_list("Flight Crew Member", pluck="name")
    for row in crew_list:
        last_flight = {
			"crew_name": row,
			"flight": None,
			"destination_code": None,
			"arrival_time": None,
		}
        for flight in onboard_flights:
            if flight["crew_name"] != row:
                continue
            departure_time = getdate(flight["departure_time"])
            duration_delta = timedelta(seconds=flight["duration"] or 0)
            arrival_time = departure_time + duration_delta
            flight["arrival_time"] = arrival_time
            if departure_time + timedelta(hours=-18) < ref_date or arrival_time + timedelta(hours=-18) < ref_date:
                last_flight = flight
            if arrival_time > ref_date:
                break
        
        data.append(last_flight)
    return data


message = """
    <div class="alert alert-warning">
        <strong>Note:</strong> Change the Target Datetime above to update last flight information.  18 hours buffer is added.
    </div>
"""