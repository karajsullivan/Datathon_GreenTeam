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
post_titles = []
post_bodies = []
post_likes = []
post_authors = []

# This next group of lists are scraped from the individual discussion post page
post_labels = []
post_tags = []
post_dates = []
post_times = []
response_authors = []
response_discussions = []
response_bodies = []
response_likes = []
response_dates = []
response_times = []


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
            if title.get('title') not in post_titles:
                post_titles.append(title.get('title'))

        # Scrape all of the bodies
        for body in x.find_all('p'):
            post_bodies.append(body.get_text())

        # Scrape the number of likes
        for y in x.find_all('li', {'class': 'custom-tile-kudos'}):
            for like in y.find_all('b'):
                post_likes.append(like.get_text())

        # Scrape the author
        for author in x.find_all('img', {'class': 'lia-user-avatar-message'}):
            post_authors.append(author.get('alt'))

        # Scrape the discussion post's URL to loop through and get further data
        # Create a list of each discussion page's individual discussion URLs
        individual_discussions = []
        # Loop through all of the discussion post's to find their link and add it to the individual_discussions list
        for link in x.find_all('a', attrs={'href': re.compile("^/t5/")}):
            if ((link.get('title')) != "View profile") and (link.get('href') not in individual_discussions) and (link.get('href') not in discussion_groups):
                individual_discussions.append(link.get('href'))
        # The base URL is the same base URL that was used earlier in the code (line 25)
        # Create a new list that combines the base URL with each individual discussion post's URL
        individual_discussions_urls = [
            base_url + k for k in individual_discussions]

    # Loop through the individual discussion post links and scrape the data within the page
    for individual_discussion_url in individual_discussions_urls:

        # Read in the indvidual discussion page
        individual_page = requests.get(individual_discussion_url)

        # Parse through the page using beautiful soup
        individual_soup = BeautifulSoup(individual_page.content, 'html.parser')

        # Scrape the labels of the discussion post
        # Initialize an empty string for the labels to be concatenated into
        discussion_label = ''
        # Loop through the labels
        for label in individual_soup.find_all('li', {'class': 'label'}):
            discussion_label += ', ' + \
                re.search('\n(.*?.)\n', (label.get_text())).group(1)
        # Add the individual discussion post's labels to the label list
        post_labels.append(discussion_label)

        # Scrape the tags of the discussion post
        # Initialize an empty string for the tags to be concatenated into
        discussion_tag = ''
        for y in individual_soup.find_all('div', id='taglist'):
            for tag in y.find_all('a'):
                discussion_tag += ', ' + tag.get_text()
        post_tags.append(discussion_tag)

        # Scrape the date of the discussion post
        for date in individual_soup.find('span', {'class': 'local-date'}):
            post_dates.append(date.get_text().lstrip('\u200e'))

        # Scrape the time of the discussion post
        for local_time in individual_soup.find('span', {'class': 'local-time'}):
            post_times.append(local_time.get_text())

        # Get a variable with the name of the discussion post
        for x in individual_soup.find_all('h1', {'class': 'lia-node-header-title'}):
            discussion_name = x.get_text()

        # Loop through the discussion post's replies
        for response in individual_soup.find_all('div', {'class': 'linear-message-list message-list'}):

            # Add the name of the discussion to a list so we know what the response was for
            response_discussions.append(discussion_name)

            # Scrape the author of each response
            for x in response.find_all('div', {'class': 'lia-message-author-with-avatar'}):
                for response_author in x.find_all('a'):
                    response_authors.append(response_author.get(
                        'aria-label').lstrip('View Profile of '))

            # Scrape the body of each response
            for y in response.find_all('div', {'class': 'lia-message-body-content'}):
                # Initiate a string that will comprise the body
                response_body_text = ''
                # Get all of the parts of the response's body
                for response_body in y.find_all('p'):
                    # Remove the unwanted part of the strings
                    response_body_text += response_body.get_text().replace('\xa0', '')
                # Append the response's body to the list
                response_bodies.append(response_body_text)

            # Scrape the number of likes for each response
            for response_like in response.find_all('span', {'class': 'MessageKudosCount lia-component-kudos-widget-message-kudos-count'}):
                response_likes.append(
                    (re.search('\n\t\n\t\t\t(.*?.) Likes\n\t\t\n', response_like.get_text())).group(1))

            # Scrape the date of each response


# Test the functionality using just 1 of the sites to not overwhelm the site
test_url = discussion_groups_url[6]
print(test_url)
test_page = requests.get(test_url)
test_soup = BeautifulSoup(test_page.content, 'html.parser')
individual_discussions = []
for x in test_soup.find_all('div', {'class': 'custom-message-list'}):
    # Loop through all of the discussion post's to find their link and add it to the individual_discussions list
    for link in x.find_all('a', attrs={'href': re.compile("^/t5/")}):
        if ((link.get('title')) != "View profile") and (link.get('href') not in individual_discussions) and (link.get('href') not in discussion_groups):
            individual_discussions.append(link.get('href'))
    # The base URL is the same base URL that was used earlier in the code (line 25)
    # Create a new list that combines the base URL with each individual discussion post's URL
    individual_discussions_urls = [
        base_url + k for k in individual_discussions]
print(individual_discussions_urls)

# Test the functionality of just scraping one of the individual discussion post pages
test_individual_url = 'https://live.paloaltonetworks.com/t5/best-practice-assessment/performance-issues-over-internet-speed-from-firewall/td-p/493152'
print(test_individual_url)
test_individual_page = requests.get(test_individual_url)
test_individual_soup = BeautifulSoup(
    test_individual_page.content, 'html.parser')
discussion_tag = ''
for y in test_individual_soup.find_all('div', id='taglist'):
    for tag in y.find_all('a'):
        discussion_tag += ', ' + tag.get_text()
post_tags.append(discussion_tag)
print(post_tags)
