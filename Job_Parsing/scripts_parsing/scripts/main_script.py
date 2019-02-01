from script_by_sites import rabota
# from rabota_headless_browser_cli import rabota


##############################################################################################
#################################        MAIN SCRIPT         #################################
##############################################################################################



job = 'python'
city = 'одесса'
site = 0
number_id = 1

def main(job, city, site, number_id):

	if site == 0:
		# RABOTA.UA
		print('RABOTA')
		total, data = rabota(job, city, site, number_id)
		return total, data

		
	else:
		# WORK.UA
		print('WORK')

total, bla = main(job, city, site, number_id)
print(total)
# [print(i['url']) for i in bla]