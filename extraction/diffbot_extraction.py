import json
import os
import requests
from requests.api import head
import json
from . models import Publication,Edition,Notes
from datetime import datetime
import requests

""" this function is for extracting the information from main site such as rp-online.de"""
def getinformation():
	url = "https://api.diffbot.com/v3/article?token=829b2a8c8929900986ff95e766d1dbc4&url=https://rp-online.de/&fields=%26fields=links,meta&paging=false&maxTags=10&tagConfidence=0.0&discussion=false&timeout=30000"
	payload={}
	headers = {}
	response = requests.request("GET", url, headers=headers, data=payload)

	responsejson= response.text
	data = json.loads(responsejson)

	''' getting data for publisher table '''
	""" this is internal to x-cago so I'm using just a random for rp-online.de """
	pubcode = 'RP-ONLN' # internal code, I just used this code randomly because I don't have access 
	publisher = data['objects'][0]['meta']['author'] # author is publisher, because author here is who published it
	feed_time = datetime.now() # getting current date and time when this call is made
	print("feed time")
	print(feed_time)
	edition_table = 0
	pub_table = 0
	
	""" check if publication table has been created ever or its first time """
	if Publication.objects.filter(pubcode=pubcode).exists():
		""" if publication table is already there then just update the feedtime """
		pub_table = Publication.objects.get(pubcode=pubcode) # user pubcode is filter to find the publication
		pub_table.feed_time = feed_time # updating the feed time column
		pub_table.save() # saving the table with updated feed time
	else:
		""" else create a table for publication and save with appropriate data """
		pub_table = Publication(name=publisher,pubcode=pubcode,publisher=publisher,repub_new=True,priority=True,frequency='hourly',feed_time=feed_time,contractor='Diffbot',ftp_client_in='Diffbot_client_in',ftp_client_out='Diffbot_client_out',ftp_contractor_in='Diffbot in/out',ftp_contractor_out='Diffbot in/out')
		pub_table.save()



	""" Check if there is any edition record created for todays day, else create a new edition record for todays day. """
	if Edition.objects.filter(issue=datetime.now().date()).exists()==False:
		todays_date = datetime.now().date() # getting todays date for every different day edition records
		pages = 0  # pages will be zero as there is no article process at the start of new date
		todays_datetime = datetime.now() # getting todays date time for client and contractor received date time
		edition_table = Edition(publication=pub_table,issue=todays_date,pages=pages,expected=todays_date,client_received=todays_datetime,contractor_received=todays_datetime)
		edition_table.save()
	else:
		""" this query is only for purpose that we need edition object for notes"""
		edition_table = Edition.objects.get(issue = datetime.now().date())


	""" this loop will run until the length of article list """
	new_article_ingest_count = 0
	for article_url_count in range(len(data['objects'][0]['meta']['microdata']['itemListElement'])):
		article_url = data['objects'][0]['meta']['microdata']['itemListElement'][article_url_count]['url']
		""" we will use this table to save the urls and keep checks for duplicates, that's for now we have!!!"""
		if Notes.objects.filter(note=article_url).exists()==False:
		# if 1==1:
			notes_table = Notes(note=article_url,edition=edition_table,publication=pub_table)
			notes_table.save()
			print("saving the notes table data")
			new_article_ingest_count+=1
			""" now as we get each url we will call the api again to get all details of the article, """
			""" I could not find the details of individual article in first crawl except the urls and other random stuff, may be I'm wrong though """
			api_call_to_article_details(article_url,pubcode) # get the details and call anohter function to save them in text files
			
	
	

	''' update "Edition" table with page count as we see new articles '''
	# current_date = data['objects'][0]['meta']['date'][0:10] # it's date time but we only need date for this.
	current_date = datetime.now().date() # it's date time but we only need date for this.
	if Edition.objects.filter(issue=current_date).exists():
		previous_record = Edition.objects.get(issue=current_date) # get edition record by filtering todays date
		previous_article_page_count = previous_record.pages # how many articles process before in todays date
		updated_page_count = previous_article_page_count+new_article_ingest_count # previous process articles of todays date and new ones which we just got now.
		previous_record.pages = updated_page_count # put the updated page count in table specific column
		previous_record.save() # finally, save the updated table.

	print("total ingested articles are: ")
	print(updated_page_count)


""" this function runs through individual URL and get details of that URL, article itself """
def api_call_to_article_details(article_url,pubcode):
	print("here is article url for which full details are being fetched: ")
	print(article_url)
	""" we are calling api two times because first time it just returns the article urls and other details 
	but here we call to get the details only about specific article """
	url = "https://api.diffbot.com/v3/article?token=829b2a8c8929900986ff95e766d1dbc4&url="+article_url+"/&fields=fields=links,meta&paging=false&maxTags=10&tagConfidence=0.0&discussion=false&timeout=30000"
	payload={}
	headers = {}
	response = requests.request("GET", url, headers=headers, data=payload)

	responsejson= response.text  # getting the text part of json,
	save_article_json_text(responsejson,article_url,pubcode) # sending that json for saving into file


""" this function saves the full article specifc data to a file with current date and timestamp """
def save_article_json_text(article_json,article_url,pubcode):
	
	""" getting the directory and saving with unique name such as timestamp """
	ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # getting the root folder of project
	directory_path = ROOT_DIR+"\\output_article_json_files\\"+pubcode+"\\"+str(datetime.now().date()) # creating a directory with current date
	if not os.path.exists(directory_path): # if does exist then create directory with base + todays date path
		os.makedirs(directory_path)

	with open(os.path.join(directory_path,str(datetime.now().timestamp())+'.json'),"w") as outfile:
		json.dump(article_json,outfile)
		outfile.close()




