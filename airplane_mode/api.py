import frappe
from frappe.utils import today
from frappe.utils import add_to_date


def pending_to_overdue():
    filters = {
        "status": "Pending",
        "period_start": [">=", today]
    }
    pendings = get_tracking_records(filters)
    for p in pendings:
        doc = frappe.get_doc("Airport Rental Income Tracking", p.name)
        doc.status = "Overdue"
        doc.save()
    

def send_7_day_rental_payment_reminder_email():
    seven_days_after = add_to_date(today(), days=7)
    filters = {
        "status": "Pending",
        "period_start": seven_days_after,
    }
    pendings = get_tracking_records(filters)
    for p in pendings:
        p.email = frappe.get_value("Airport Tenant", p.tenant, "email" )
        frappe.sendmail(
            recipients=[p.email],
            subject="Rental Payment due in 7 days",
            message=f"""
                <p>Dear Sir/Madam,<p>
                <p>Friendly reminder.  Please be advised that the following rental contract is due in 7 days:</p>
                <p><b>Contact Number</b>: {p.shop_rental_contract}<br>
                <b>Due Date</b>: {p.period_start}<br>
                <b>Amount</b>: {p.amount}</p>
                <p>Please settle the above at your convenience.  If you have already done so, please neglect this email.</p>
                <p>Thank you for your attention</p>
                <p>Best regards,</p>
                <p>DDR Aiport Management Team</p>
            """
        )

def send_3_day_rental_payment_reminder_email():
    three_days_after = add_to_date(today(), days=3)
    filters = {
        "status": "Pending",
        "period_start": three_days_after,
    }
    pendings = get_tracking_records(filters)
    for p in pendings:
        p.email = frappe.get_value("Airport Tenant", p.tenant, "email" )
        frappe.sendmail(
            recipients=[p.email],
            subject="Rental Payment due in 3 days",
            message=f"""
                <p>Dear Sir/Madam,<p>
                <p>Please be reminded that the following rental contract is due in 3 days:</p>
                <p><b>Contact Number</b>: {p.shop_rental_contract}<br>
                <b>Due Date</b>: {p.period_start}<br>
                <b>Amount</b>: {p.amount}</p>
                <p>Please settle the above at your convenience.  If you have already done so, please neglect this email.</p>
                <p>Thank you for your attention</p>
                <p>Best regards,</p>
                <p>DDR Aiport Management Team</p>
            """
        )

def send_1_day_rental_payment_reminder_email():
    one_day_after = add_to_date(today(), days=1)
    filters = {
        "status": "Pending",
        "period_start": one_day_after,
    }
    pendings = get_tracking_records(filters)
    for p in pendings:
        p.email = frappe.get_value("Airport Tenant", p.tenant, "email" )
        frappe.sendmail(
            recipients=[p.email],
            subject="REMINDER: Rental Payment due tomorrow",
            message=f"""
                <p>Dear Sir/Madam,<p>
                <p>Please be reminded that the following rental contract is tomorrow:</p>
                <p><b>Contact Number</b>: {p.shop_rental_contract}<br>
                <b>Due Date</b>: {p.period_start}<br>
                <b>Amount</b>: {p.amount}</p>
                <p>Please settle the above at your earliest convenience.  If you have already done so, please neglect this email.</p>
                <p>Thank you for your attention</p>
                <p>Best regards,</p>
                <p>DDR Aiport Management Team</p>
            """
        )


def send_overdue_rental_payment_reminder_email():
    filters = {
        "status": "Overdue",
    }
    overdues = get_tracking_records(filters)
    for o in overdues:
        o.email = frappe.get_value("Airport Tenant", o.tenant, "email" )
        frappe.sendmail(
            recipients=[o.email],
            subject="REMINDER: Rental Payment Overdue",
            message=f"""
                <p>Dear Sir/Madam,<p>
                <p>Please be reminded that the following rental contract is overdue:</p>
                <p><b>Contact Number</b>: {o.shop_rental_contract}<br>
                <b>Due Date</b>: {o.period_start}<br>
                <b>Amount</b>: {o.amount}</p>
                <p>Please settle the above immediately.  If you have already done so, please neglect this email.</p>
                <p>Thank you for your attention</p>
                <p>Best regards,</p>
                <p>DDR Aiport Management Team</p>
            """
        )

def get_tracking_records(filters: dict):
    return frappe.get_all("Airport Rental Income Tracking",
        filters = filters,
        fields = ['name','shop_rental_contract', 'perid_start', 'amount', 'tenant', 'status']
    )
