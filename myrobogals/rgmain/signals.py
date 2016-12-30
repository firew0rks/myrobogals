from django.db.models.signals import post_migrate
from django.dispatch import receiver
from myrobogals.rgmain.models import Timezone
from pytz import all_timezones
from django.apps import AppConfig

def update_timezones(sender, **kwargs):
	installed_timezones = []
	timezones_to_add = []
	timezones_to_remove = []
	for tzone in Timezone.objects.all():
		installed_timezones.append(tzone.description)

	# Add any timezone that isn't in the myRobogals timezone table
	for timezone in all_timezones:
		if timezone not in installed_timezones:
			timezones_to_add.append(timezone)
			
	# Note any obsolete timezone that are in the myRobogals timezone table
	for timezone in installed_timezones:
		if timezone not in all_timezones:
			timezones_to_remove.append(timezone)

	for timezone in timezones_to_add:
		tzone = Timezone(description=timezone)
		tzone.save()
		print("Added timezone " + tzone.description)

	if len(timezones_to_remove) == 0:
		print("Timezones in rgmain_timezone are up to date")
	else:
		print("The following timezones need to be manually removed from your database (table rgmain_timezone) after confirming that no chapters use them:")
		for timezone in timezones_to_remove:
			print timezone
	
	print(" ")
	print("*** IMPORTANT ***")
	print("Remember to periodically update the pytz package to get the latest timezone definitions")
	print(" ")
	print("Also periodically update MySQL's timezones using the following command. You will need the MySQL root password.")
	print("   mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql")
	print(" ")

class RgMainAppConfig(AppConfig):
	name = 'myrobogals.rgmain'
	def ready(self):
		post_migrate.connect(update_timezones, sender=self, weak=False)
