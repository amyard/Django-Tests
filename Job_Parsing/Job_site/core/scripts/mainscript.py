from .scriptbysites import rabota


##############################################################################################
#################################        MAIN SCRIPT         #################################
##############################################################################################



job = None
city = None
site = None
number_id = None

def main_script(job, city, site, number_id):

	if site == 0:
		# RABOTA.UA
		data = rabota(job, city, site, number_id)
		return data

		
	else:
		# WORK.UA
		data = rabota()