import frappe
from frappe.utils import today
from frappe.utils import add_to_date, date_diff
from frappe import _



def validate_shop_rental_tracking():

    active_contracts = frappe.get_all("Shop Rental Contract",
    filters={
        "effective_date": ['<=', today()],
        "expiry_date": ['>=', today()],
        "docstatus": 1
    },
    pluck="name")
    if not active_contracts:
        return

    tracking_contracts = frappe.get_all("Airport Rental Income Tracking",
        filters={
            'period_start': ['<=', today()],
            'period_end': ['>=', today()]
        },
        fields=['shop_rental_contract'],
        pluck="shop_rental_contract"
    )
    
    missing_contracts = list(set(active_contracts) - set(tracking_contracts))

    if missing_contracts:
        send_tracking_alert_email(missing_contracts)

def send_tracking_alert_email(missing_list):
    # Define who should receive the alert here.
    roles = ("Airport Authority Personnel", "System Manager")

    recipients = frappe.db.sql(f"""
        SELECT DISTINCT `tabUser`.email, `tabUser`.first_name, `tabUser`.name FROM `tabUser`
        JOIN `tabHas Role`
        ON `tabHas Role`.parent = `tabUser`.name
        WHERE `tabHas Role`.parenttype = "User"
        && `tabHas Role`.role IN {roles}
        """,as_dict=1)
    if recipients:
        recipient_list = [r.email for r in recipients]
        items_html = "".join([f"<li>{i}</li>" for i in missing_list])
        message = f"""
            <h3>Action Required: Missing Rental Tracking</h3>
            <p>The following active contracts currently have no recorded income tracking:</p>
            <ul>{items_html}</ul>
            <p>Please create a record in <b>Airport Rental Income Tracking</b> immediately
            or update the contract expiry date, so as to make sure it is expired.</p>
            <p>This is a system notification.  Do not reply to this email.</p>
        """
        subject = f"Missing Income Tracking: {len(missing_list)} Contracts"
        frappe.sendmail(
            recipients=recipient_list,
            subject=subject,
            message=message,
            now=False,
            header=["Tracking Compliance Alert", "red"]
        )


def set_pending_to_overdue():
    filters = {
        "status": "Pending",
        "period_start": ["<=", today]
    }
    pendings = get_tracking_records(filters)
    for p in pendings:
        doc = frappe.get_doc("Airport Rental Income Tracking", p.name)
        doc.status = "Overdue"
        doc.save()
    

def send_rental_payment_reminder_email():
    doc = frappe.get_doc("Airport Shop Rental Settings")
    if doc.enable_rent_reminder == 1:
        filters = {
            "status": "Pending",
        }
        pendings = get_tracking_records(filters)
        seven_days = add_to_date(today(), days=7)
        three_days = add_to_date(today(), days=3)
        one_day = add_to_date(today(), days=1)
        for p in pendings:
            if p.period_start == seven_days or p.period_start == three_days or p.period_start == one_day:
                days = date_diff(p.period_start, today())
                p.email = frappe.get_value("Airport Tenant", p.tenant, "email")
                frappe.sendmail(
                    recipients=[p.email],
                    subject=_(f"REMINDER: Rental Payment due in {days} day(s)"),
                    message=_(f"""
                        <p>Dear Sir/Madam,<p>
                        <p>Please be reminded that the rental payment of the following contract is overdue in {days} day(s):</p>
                        <p><b>Contact Number</b>: {p.shop_rental_contract}<br>
                        <b>Due Date</b>: {p.period_start}<br>
                        <b>Amount</b>: {p.amount}</p>
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
    for o in overdues:
        o.email = frappe.get_value("Airport Tenant", o.tenant, "email" )
        frappe.sendmail(
            recipients=[o.email],
            subject="REMINDER: Rental Payment Overdue",
            message=f"""
                <p>Dear Sir/Madam,<p>
                <p>Please be reminded that the following rental payment is overdue:</p>
                <p><b>Contact Number</b>: {o.shop_rental_contract}<br>
                <b>Due Date</b>: {o.period_start}<br>
                <b>Amount</b>: {o.amount}</p>
                <p>Please settle the above immediately.  If you have already done so, please neglect this email.</p>
                <p>Thank you for your attention.</p>
                <p>Best regards,</p>
                <p>DDR Aiport Management Team</p>
            """
        )

def get_tracking_records(filters: dict):
    return frappe.get_all("Airport Rental Income Tracking",
        filters = filters,
        fields = ['name','shop_rental_contract', 'period_start', 'amount', 'tenant', 'status']
    )
