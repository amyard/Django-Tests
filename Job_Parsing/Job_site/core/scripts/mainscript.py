from .scriptbysites import rabota, work


##############################################################################################
#################################        MAIN SCRIPT         #################################
##############################################################################################



job = None
city = None
site = None
number_id = None

def main_script(job, city, slug, site, number_id):

	if site == 0:
		# RABOTA.UA
		total, data = rabota(job, city, site, number_id)
		return total, data

		
	else:
		# WORK.UA
		total, data = work(job, slug, site, number_id)
		return total, data
