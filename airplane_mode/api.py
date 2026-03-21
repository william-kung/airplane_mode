import frappe
from frappe.utils import today, add_to_date, date_diff
from frappe import _



def send_rental_payment_reminder_email():
    doc = frappe.get_doc("Airport Shop Rental Settings")
    if doc.enable_rent_reminder == 1:
        filters = {
            "status": "Pending",
        }
        pendings = get_tracking_records(filters)
        # only send emails for 7, 3, and 1 days before due.
        seven_days = add_to_date(today(), days=7)
        three_days = add_to_date(today(), days=3)
        one_day = add_to_date(today(), days=1)
        for p in pendings:
            if p.period_start == seven_days or p.period_start == three_days or p.period_start == one_day:
                days = date_diff(p.period_start, today())
                p.email = frappe.db.get_value("Airport Tenant", p.tenant, "email")
                frappe.sendmail(
                    recipients=[p.email],
                    subject=_(f"REMINDER: Rental Payment due in {days} day(s)"),
                    message=_(f"""
                        <p>Dear Sir/Madam,<p>
                        <p>Please be reminded that the rental payment of the following contract is overdue in {days} day(s):</p>
                        <p><b>Contact Number</b>: {p['shop_rental_contract']}<br>
                        <b>Due Date</b>: {p['period_start']}<br>
                        <b>Amount</b>: {p['amount']}</p>
                        <p>Please settle the above at your earliest convenience.  If you have already done so, please neglect this email.</p>
                        <p>Thank you for your attention.</p>
                        <p>Best regards,</p>
                        <p>DDR Aiport Management Team</p>
                    """)
                )
    else:
        return

def send_overdue_rental_payment_reminder_email():
    filters = {
        "status": "Overdue",
    }
    overdues = get_tracking_records(filters)
    if len(overdues)>0:
        for o in overdues:
            email = frappe.db.get_value("Airport Tenant", o['tenant'], "email" )
            frappe.sendmail(
                recipients=[email],
                subject=_("REMINDER: Rental Payment Overdue"),
                message=_(f"""
                    <p>Dear Sir/Madam,<p>
                    <p>Please be reminded that the following rental payment is overdue:</p>
                    <p><b>Contact Number</b>: {o['shop_rental_contract']}<br>
                    <b>Due Date</b>: {o['period_start']}<br>
                    <b>Amount</b>: {o['amount']}</p>
                    <p>Please settle the above immediately.  If you have already done so, please neglect this email.</p>
                    <p>Thank you for your attention.</p>
                    <p>Best regards,</p>
                    <p>DDR Aiport Management Team</p>
                """)
            )

def add_missing_shop_rental_tracking():

    active_contracts = get_active_contracts()
    if not active_contracts:
        return
    filters={
            'docstatus':  ['!=', '2'],
            'period_start': ['<=', today()],
            'period_end': ['>=', today()]
        },
    tracking_records = get_tracking_records(filters)
    if tracking_records:
        tracking_records = [r.shop_rental_contract for r in tracking_records]
    
    tracking_set = set(tracking_records)
    
    missing_contracts= [c for c in active_contracts if c['name'] not in tracking_set]
    
    if missing_contracts:
        add_tracking_records(missing_contracts)


def set_pending_to_overdue():
    filters = {
        'docstatus':  ['!=', '2'],
        "status": "Pending",
        "period_start": ["<=", today()]
    }
    pendings = get_tracking_records(filters)
    for p in pendings:
        doc = frappe.get_doc("Airport Rental Income Tracking", p.name)
        doc.status = "Overdue"
        doc.save()
    

def get_active_contracts():
    return frappe.get_all("Shop Rental Contract",
        filters={
            'docstatus':  ['!=', '2'],
            "effective_date": ['<=', add_to_date(today(), days = -15)], # include contracts to be effective in 15 days
            "expiry_date": ['>=', today()],
        },
        fields=['name', 'tenant', 'rent_amount']
    )

def get_tracking_records(filters: dict):
    return frappe.get_all("Airport Rental Income Tracking",
        filters = filters,
        fields = ['name','shop_rental_contract', 'period_start', 'amount', 'tenant', 'status']
    )


def add_tracking_records(contracts):
    for c in contracts:
        doc = frappe.new_doc("Airport Rental Income Tracking")
        doc.shop_rental_contract = c.name
        doc.tenant = c.tenant
        doc.amount = c.rent_amount
        dates = doc.get_dates()
        doc.period_start = dates.get("period_start")
        doc.period_end = dates.get("period_end")
        if date_diff(doc.period_start, today()) >0:
            doc.status = "Pending"
        else:
            doc.status = "Overdue"
        doc.insert()





