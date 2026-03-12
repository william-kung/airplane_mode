import frappe
from frappe import _

def get_context(context):
	# do your magic here
	pass


# def validate(self):
# 	if self.email:
# 		self.email = self.email.strip()
# 	if self.phone:
# 		self.phone = self.phone.strip()
# 	if not self.email and not self.phone:		
# 		frappe.throw(
# 			msg=_("Please enter at least either email or phone number."),
# 			title=_("Error"),
# 		)