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
base_url = "https://live.paloaltonetworks.com/"

# Create a new list that appends the base url to each page's new url
discussion_groups_url = [base_url + x for x in discussion_groups]

# Initialize lists of information based off Ethan's datathon schema
titles = []
# locations = [] # Not sure where that is located on the site
bodies = []
likes = []
tags = []
labels = []
authors = []
datetime = []


# Loop through the list of the web pages we want to scrape to extract information
for url in discussion_groups_url:
    # Read in the page
    page = requests.get(url)

    # Parse through the page using beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Go through the discussion posts on each page
    for x in soup.find_all('div', {'class': 'custom-message-list'}):
        # Scrape the titles of the discussion posts
        for title in x.find_all('a'):
            if title.get('title') not in titles:
                titles.append(title.get('title'))
        # Scrape all of the bodies
        for body in x.find_all('p'):
            bodies.append(body.get_text())
        # Scrape the number of lies
        for likes in x.find_all('b', {'class': 'custom-tile-kudos'}):
            likes.append(likes.get_text())


# Test the functionality using just 1 of the sites to not overwhelm the site
test_url = discussion_groups_url[2]
print(test_url)
test_page = requests.get(test_url)
test_soup = BeautifulSoup(test_page.content, 'html.parser')
for x in soup.find_all('div', {'class': 'custom-message-list'}):
    for likes in (x.find_all('li', {'class': 'custom-tile-kudos'})):

        likes.append(likes.get_text())
print(likes)
