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

# This first group of lists can be scraped from the discussion group page
page_titles = []
titles = []
bodies = []
likes = []
authors = []

# This next group of lists are scraped from the individual discussion post page
labels = []
tags = []
datetimes = []


# locations = [] # Not sure where that is located on the site


# ***HAVE NOT YET INCLUDED A TIME LAG <-- RUNNING THE ENTIRE THING MIGHT OVERWHELM THE SITE***

# Loop through the list of the web pages we want to scrape to extract information
for url in discussion_groups_url:
    # Read in the page
    page = requests.get(url)

    # Parse through the page using beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the title of the discussion page the discussion was posted on
    for y in soup.find_all('title'):
        # Strip the livecommunity part from the beginning and end of the string
        page_title = re.search(
            '\n\tLIVEcommunity - (.*?.) - LIVEcommunity\n', (y.get_text())).group(1)

    # Go through the discussion posts on each page
    for x in soup.find_all('div', {'class': 'custom-message-list'}):

        # Add the title of the discussion page to the list
        page_titles.append(page_title)

        # Scrape the titles of the discussion posts
        for title in x.find_all('a'):
            if title.get('title') not in titles:
                titles.append(title.get('title'))

        # Scrape all of the bodies
        for body in x.find_all('p'):
            bodies.append(body.get_text())

        # Scrape the number of likes
        for y in x.find_all('li', {'class': 'custom-tile-kudos'}):
            for like in y.find_all('b'):
                likes.append(like.get_text())

        # Scrape the author
        for author in x.find_all('img', {'class': 'lia-user-avatar-message'}):
            authors.append(author.get('alt'))

        # Scrape the discussion post's URL to loop through and get further data
        # Create a list of each discussion page's individual discussion URLs
        individual_discussions = []
        # Loop through all of the discussion post's to find their link and add it to the individual_discussions list
        for link in x.find_all('a', attrs={'href': re.compile("^/t5/")}):
            if (link.get('title')) != "View profile":
                if link.get('href') not in individual_discussions:
                    individual_discussions.append(link.get('href'))
        # The base URL is the same base URL that was used earlier in the code (line 25)
        # Create a new list that combines the base URL with each individual discussion post's URL
        individual_discussions_urls = [
            base_url + k for k in individual_discussions]

    # Loop through the individual discussion post links and scrape the data within the list
    for individual_discussion_url in individual_discussions_urls:

        # Read in the indvidual discussion page
        individual_page = requests.get(individual_discussion_url)

        # Parse through the page using beautiful soup
        individual_soup = BeautifulSoup(individual_page.content, 'html.parser')

        # Scrape the labels
        for label in individual_soup.find_all('li', {'class': 'label'}):
            labels.append(re.search('\n(.*?.)\n', (label.get_text())).group(1))

        # Scrape the tags
        for y in individual_soup.find_all('div', id='taglist'):
            for tag in y.find_all('a'):
                tags.append(tag.get_text())


# Test the functionality using just 1 of the sites to not overwhelm the site
test_url = discussion_groups_url[5]
print(test_url)
test_page = requests.get(test_url)
test_soup = BeautifulSoup(test_page.content, 'html.parser')
for x in test_soup.find_all('div', {'class': 'custom-message-list'}):
    individual_discussions = []
    # Loop through all of the discussion post's to find their link and add it to the individual_discussions list
    for link in x.find_all('a', attrs={'href': re.compile("^/t5/")}):
        if (link.get('title')) != "View profile":
            if link.get('href') not in individual_discussions:
                individual_discussions.append(link.get('href'))
    # The base URL is the same base URL that was used earlier in the code (line 25)
    # Create a new list that combines the base URL with each individual discussion post's URL
    individual_discussions_urls = [
        base_url + k for k in individual_discussions]
print(individual_discussions_urls)

# Test the functionality of just scraping one of the individual discussion post pages
test_individual_url = individual_discussions_urls[0]
print(test_individual_url)
test_individual_page = requests.get(test_individual_url)
test_individual_soup = BeautifulSoup(
    test_individual_page.content, 'html.parser')
for y in test_individual_soup.find_all('div', id='taglist'):
    for tag in y.find_all('a'):
        tags.append(tag.get_text())
print(tags)
