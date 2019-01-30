from script_by_sites import rabota


##############################################################################################
#################################        MAIN SCRIPT         #################################
##############################################################################################



job = 'python'
city = 'киев'
site = 0
number_id = 1

def main(job, city, site, number_id):

	if site == 0:
		# RABOTA.UA
		print('RABOTA')
		data = rabota(job, city, site, number_id)
		print(data)
		return data

		
	else:
		# WORK.UA
		print('WORK')

main(job, city, site, number_id)