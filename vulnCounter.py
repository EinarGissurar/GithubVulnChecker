import csv
import time
import requests

token_header = {"Authorization" : "token e2d2c3b8526dd9c3916ed51171bd87ebfb3ec624"}
# Base API Endpoint
base_api_url = 'https://api.github.com/'

query = base_api_url + 'search/code?q='

#Create a file that will contain a list of all repos and number of vulnerabilies
filename = 'vulnerabilities.csv'
fieldnames = ['repo_name', 'repo_owner', '#_memcmp', '#_memcpy', '#_strcmp', '#_strcpy', '#_stars', '#_forks', 'repo_description', 'repo_api_url', 'repo_html_url', 'repo_stargazers', 'repo_subscribers', 'repo_forks', 'repo_main_language']
#with open(filename, 'w', newline='') as csvfile:
#	write_to_scv = csv.writer(csvfile, delimiter='|')
#	write_to_scv.writerow(fieldnames)

#List of vulnerabilities that were queried.
docs = ['top_stars', 'top_forks', 'gets', 'memcmp', 'memcpy', 'strcmp', 'strcpy']
vuln = ['memcmp', 'memcpy', 'strcmp', 'strcpy']

unique_repos = 0

#Iterate through each query
for doc in docs:
	print('Counting through ' + doc)
	with open(doc+'.csv', 'r',) as file:
		reader = csv.DictReader(file, delimiter='|')
		for row in reader:
			#Assume you need to add repo unless it already exists
			add_row = True

			#Fetch existing repos
			with open(filename, 'r') as csvfile:
				current = csv.DictReader(csvfile, delimiter='|')
				data = list(current)

			#Check if repo already exists
			for existing_row in data[1:]:
				if existing_row['repo_html_url'] == row['repo_html_url']:
					add_row = False

			#Append new row if repo doesn't exist, otherwise update existing row
			if add_row:
				unique_repos += 1
				with open(filename, 'a', newline='') as csvfile:
					writer = csv.writer(csvfile, delimiter='|')

					repo_name = row['repo_name']
					repo_owner = row['repo_owner']
					print(repo_owner+'/'+repo_name)
					for hax in vuln:
						inner_response = requests.get(query+hax+' repo:'+repo_owner+'/'+repo_name, headers=token_header).json()
						count = inner_response['total_count']
						
						if hax == 'memcmp':
							memcmp = count
						if hax == 'memcpy':
							memcpy = count
						if hax == 'strcmp':
							strcmp = count
						if hax == 'strcpy':
							strcpy = count
					repo_stars = row['repo_starcount']
					repo_forkcount = row['repo_forkcount']
					repo_description = row['repo_description']
					repo_api_url = row['repo_api_url']
					repo_html_url = row['repo_html_url']
					repo_starsgazers = row['repo_stargazers']
					repo_subscribers = row['repo_subscribers']
					repo_forks = row['repo_forks']
					repo_main_language = row['repo_main_language']

					time.sleep(9)

					writer.writerow([repo_name,repo_owner,memcmp,memcpy,strcmp,strcpy,repo_stars,repo_forkcount,repo_description,repo_api_url,repo_html_url,repo_starsgazers,repo_subscribers,repo_forks,repo_main_language])
print('Done. Total of ' + str(unique_repos) + 'repos cataloged.')
