# Import required modules
import requests
import time
import csv

# Paste your Access token here
# To create an access token - https://github.com/settings/tokens
#token = "access_token=" + "e2d2c3b8526dd9c3916ed51171bd87ebfb3ec624"
token_header = {"Authorization" : "token e2d2c3b8526dd9c3916ed51171bd87ebfb3ec624"}
# Base API Endpoint
base_api_url = 'https://api.github.com/'

search_code_url = base_api_url + 'search/code?q='
search_repo_url = base_api_url + 'search/repositories?q='
rate_limit_url = base_api_url + 'rate_limit'

# Enter multiple word queries with a '+' sign
# Ex: machine+learning to search for Machine Learning

#Check rate limit
rate = requests.get(rate_limit_url, headers=token_header).json()
print(rate)

print('Enter the Search Query to get the Data ')

#queries = ['gets', 'memcmp', 'memcpy', 'strcmp', 'strcpy']
queries = ['gets']

#query = input()
#print('\n Query entered is', query, '\n')

# A CSV file containting the data would be saved with the name as the query
# Ex: machine+learning.csv

for query in queries:
    print('Searching for popular code with: ' + query)

    filename = query + '.csv'

    # Create a CSV file or clear the existing one with the same name
    with open(filename, 'w', newline='') as csvfile:
        write_to_csv = csv.writer(csvfile, delimiter='|')
        write_to_csv.writerow(['code_name', 'code_api_url', 'code_html_url', 'repo_name', 'repo_owner', 'repo_starcount', 'repo_forkcount', 'repo_description', 'repo_api_url', 'repo_html_url', 'repo_stargazers', 'repo_subscribers', 'repo_forks', 'repo_main_language'])


    # GitHub returns information of only 30 repositories with every request
    # The Search API Endpoint only allows upto 1000 results, hence the range has been set to 35
    for page in range(1, 35):

        # Building the Search API URL
        search_final_url = search_code_url + \
            query + ' language:C++' + '&sort:interactions' + '&page=' + str(page)
            
        print(search_final_url)
        
        # try-except block just incase you set up the range in the above for loop beyond 35
        try:
            response = requests.get(search_final_url, headers=token_header).json()
        except:
            print("Issue with GitHub API, Check your token")

        # Parsing through the response of the search query
        for item in response['items']:
            # Append to the CSV file
            with open(filename, 'a', newline='') as csvfile:
                write_to_csv = csv.writer(csvfile, delimiter='|')
                
                code_name = item['name']
                code_api_url = item['url']
                code_html_url = item['html_url']
                repo_name = item['repository']['name']
                repo_owner = item['repository']['owner']['login']               
                repo_description = item['repository']['description']
                repo_api_url = item['repository']['url']

                getthedamnforksandstars = requests.get(repo_api_url, headers=token_header).json()
                
                repo_starcount = getthedamnforksandstars['stargazers_count']
                repo_forkcount = getthedamnforksandstars['forks_count']

                repo_html_url = item['repository']['html_url']
                repo_stars = item['repository']['stargazers_url']
                repo_subscribers = item['repository']['subscribers_url']
                repo_forks = item['repository']['forks_url']
                repo_main_language = item['repository']['languages_url']
                
                #repo_license = None
                # repo_score is the relevancy score of a repository to the search query
                # Reference - https://developer.github.com/v3/search/#ranking-search-results
                #repo_score = item['score']

                # Many Repositories don't have a license, this is to filter them out
                #if item['license']:
                #    repo_license = item['license']['name']
                #else:
                #    repo_license = "NO LICENSE"

                # Just incase, you face any issue with GitHub API Rate Limiting, use the sleep function as a workaround
                # Reference - https://developer.github.com/v3/search/#rate-limit

                #time.sleep(10)

                # Languages URL to access all the languages present in the repository
                #language_url = item['url'] + '/languages?'
                #language_response = requests.get(language_url).json()

                #repo_languages = {}

                # Calculation for the percentage of all the languages present in the repository
                #count_value = sum([value for value in language_response.values()])
                #for key, value in language_response.items():
                #    key_value = round((value / count_value) * 100, 2)
                #    repo_languages[key] = key_value
                #print("Repo Name = ", repo_name, "\tDescription", repo_description, "\tStars = ", repo_stars, "\tWatchers = ", repo_watchers, "\tForks = ", repo_forks, "\tOpen Issues = ", repo_issues_count, "\tPrimary Language = ", repo_main_language, "\tRepo Languages =", repo_languages, '\tRepo Score', repo_score)

                # Write as a row to the CSV file
                write_to_csv.writerow([code_name, code_api_url, code_html_url, repo_name, repo_owner, repo_starcount, repo_forkcount, repo_description, repo_api_url, repo_html_url, repo_stars, repo_subscribers, repo_forks, repo_main_language])
                #print('==========')

        #Avoid reaching raid limit. Have fun waiting a while.
        time.sleep(11)
