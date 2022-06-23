# Import necessary classes
import requests
from bs4 import BeautifulSoup
import re
import time

# Read in the discussions home page
discussionHome_url = "https://live.paloaltonetworks.com/t5/discussions/ct-p/members"
discussionHome_page = requests.get(discussionHome_url)

# Parse through the discussion home page using beautiful soup
discussionHome_soup = BeautifulSoup(discussionHome_page.content, 'html.parser')


# Create an empty list to hold each discussion page's URL's
discussion_groups = []

# Loop through the class that contains the different discussion pages
for i in discussionHome_soup.find_all('div', {'class': 'custom-tiled-node-navigation'}):
    for link in i.find_all('a', attrs={'href': re.compile("^/t5/")}):
        if link.get('href') not in discussion_groups:
            discussion_groups.append(link.get('href'))

# Get the base URL that all of the discussion page web pages have
base_url = "https://live.paloaltonetworks.com/t5/"

# Create a new list that appends the base url to each page's new url
discussion_groups_url = [base_url + x for x in discussion_groups]

# Initialize lists of information
title = []


# Loop through the list of the web pages we want to scrape to extract information
for url in discussion_groups_url:
    # Read in the page
    page = requests.get(url)

    # Parse through the page using beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')
