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
# doctype_js = {"doctype" : "public/js/doctype.js"}
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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

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
