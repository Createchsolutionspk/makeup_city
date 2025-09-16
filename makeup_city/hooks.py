app_name = "makeup_city"
app_title = "Makeup City"
app_publisher = "Createch Solutions"
app_description = "A frappe custom app for Makeup City"
app_email = "ab.qadeershah@createch.solutions"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/makeup_city/css/makeup_city.css"
# app_include_js = "/assets/makeup_city/js/makeup_city.js"

# include js, css files in header of web template
# web_include_css = "/assets/makeup_city/css/makeup_city.css"
# web_include_js = "/assets/makeup_city/js/makeup_city.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "makeup_city/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Material Request" : "public/js/material_request.js",
	"Stock Entry" : "public/js/stock_entry.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "makeup_city.utils.jinja_methods",
# 	"filters": "makeup_city.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "makeup_city.install.before_install"
# after_install = "makeup_city.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "makeup_city.uninstall.before_uninstall"
# after_uninstall = "makeup_city.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "makeup_city.utils.before_app_install"
# after_app_install = "makeup_city.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "makeup_city.utils.before_app_uninstall"
# after_app_uninstall = "makeup_city.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "makeup_city.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"validate": "makeup_city.events.sales_invoice.validate",
        "on_submit": "makeup_city.events.sales_invoice.on_submit"
	},
	"Stock Entry": {
		"validate": "makeup_city.events.stock_entry.validate"
	},
	"Material Request": {
		"validate": "makeup_city.events.material_request.validate"
	},
    "Purchase Receipt": {
        "validate": "makeup_city.events.purchase_receipt.validate_duplicate_draft_grn"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"makeup_city.tasks.all"
# 	],
# 	"daily": [
# 		"makeup_city.tasks.daily"
# 	],
# 	"hourly": [
# 		"makeup_city.tasks.hourly"
# 	],
# 	"weekly": [
# 		"makeup_city.tasks.weekly"
# 	],
# 	"monthly": [
# 		"makeup_city.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "makeup_city.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "makeup_city.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "makeup_city.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["makeup_city.utils.before_request"]
# after_request = ["makeup_city.utils.after_request"]

# Job Events
# ----------
# before_job = ["makeup_city.utils.before_job"]
# after_job = ["makeup_city.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"makeup_city.auth.validate"
# ]

fixtures = [
	{
		"dt": "Custom Field",
		"filters": [
			["name", "in", [
					"POS Opening Shift-custom_opening_shift_denomination",
					"POS Closing Shift-custom_closing_shift_denomination",
					"POS Opening Shift Detail-custom_last_day_closing",
					"POS Opening Shift Detail-custom_difference",
					"Shift Denomination-custom_amount",
					"Sales Invoice-custom_bank",
					"Sales Invoice-custom_bank_last_4_digits",
					"POS Closing Shift-custom_section_break_nj8yw",
					"POS Closing Shift-custom_pos_shift_closing_cash_out",
					"POS Closing Shift Detail-custom_sales_amount",
					"POS Closing Shift Detail-custom_cash_deposits",
					"POS Opening Shift-custom_remarks"
					"POS Closing Shift-custom_remarks",
					"POS Closing Shift-custom_closing_amount",
					"Sales Invoice Item-custom_tax_rate",
					"Sales Invoice Item-custom_rate_with_tax",
					"Sales Person-custom_pos_profiles_links",
					"Sales Person-custom_pos_profiles",
					"POS Opening Shift-Sales Person-pos_profile",
					"Item-is_bundle",
                    "Material Request-custom_section_break_cadyf",
                    "Material Request-custom_total_qty",
                    "Material Request-custom_column_break_rwlqc",
                    "Material Request-custom_total_amount",
                    "Company-custom_validate_outstanding"
				]
			]
		]
	}
]