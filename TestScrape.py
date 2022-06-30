# Import necessary classes
import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

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

# This list will hold the individual discussion post's URL and will act as the unique id for the posts dataframe
discussion_urls = []

# Final test: testing the entire scrape loop on just 1 of the sites
url = discussion_groups_url[0]
print(url)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

for y in soup.find_all('title'):
    # Strip the livecommunity part from the beginning and end of the string
    page_title = re.search(
        '\n\tLIVEcommunity - (.*?.) - LIVEcommunity\n', (y.get_text())).group(1)
    time.sleep(5)

# Go through the discussion posts on each page
for x in soup.find_all('div', {'class': 'custom-message-list'}):

    # Scrape the titles of the discussion posts
    for title in x.find_all('a'):
        if title.get('title') not in post_titles:
            post_titles.append(title.get('title'))
        # Add the title of the discussion page to the list
        page_titles.append(page_title)
        time.sleep(5)

    # Scrape all of the bodies
    for body in x.find_all('p'):
        post_bodies.append(body.get_text())
        time.sleep(5)

    # Scrape the number of likes
    for y in x.find_all('li', {'class': 'custom-tile-kudos'}):
        for like in y.find_all('b'):
            post_likes.append(like.get_text())
        time.sleep(5)

    # Scrape the author
    for author in x.find_all('img', {'class': 'lia-user-avatar-message'}):
        post_authors.append(author.get('alt'))
        time.sleep(5)

    # Scrape the discussion post's URL to loop through and get further data
    # Create a list of each discussion page's individual discussion URLs
    individual_discussions = []
    # Loop through all of the discussion post's to find their link and add it to the individual_discussions list
    for link in x.find_all('a', attrs={'href': re.compile("^/t5/")}):
        if ((link.get('title')) != "View profile") and (link.get('href') not in individual_discussions) and (link.get('href') not in discussion_groups):
            individual_discussions.append(link.get('href'))
        time.sleep(5)
    # The base URL is the same base URL that was used earlier in the code (line 25)
    # Create a new list that combines the base URL with each individual discussion post's URL
    individual_discussions_urls = [
        base_url + k for k in individual_discussions]
    # Add the URL to the list so it can be used as the unique id for the post table
    discussion_urls += individual_discussions_urls

individual_url = individual_discussions_urls[0]
print(individual_url)
individual_page = requests.get(individual_url)
individual_soup = BeautifulSoup(individual_page.content, 'html.parser')


# Scrape the labels of the discussion post
# Initialize an empty string for the labels to be concatenated into
discussion_label = ''
# Loop through the labels
for label in individual_soup.find_all('li', {'class': 'label'}):
    discussion_label += ', ' + \
        re.search('\n(.*?.)\n', (label.get_text())).group(1)
    time.sleep(5)
    # Add the individual discussion post's labels to the label list
post_labels.append(discussion_label)

# Scrape the tags of the discussion post
# Initialize an empty string for the tags to be concatenated into
discussion_tag = ''
for y in individual_soup.find_all('div', id='taglist'):
    for tag in y.find_all('a'):
        discussion_tag += ', ' + tag.get_text()
    time.sleep(5)
post_tags.append(discussion_tag)

# Scrape the date of the discussion post
for date in individual_soup.find('span', {'class': 'local-date'}):
    post_dates.append(date.get_text().lstrip('\u200e'))
    time.sleep(5)

# Scrape the time of the discussion post
for local_time in individual_soup.find('span', {'class': 'local-time'}):
    post_times.append(local_time.get_text())
    time.sleep(5)

# Get a variable with the name of the discussion post
for x in individual_soup.find_all('h1', {'class': 'lia-node-header-title'}):
    discussion_name = x.get_text()
    time.sleep(5)

# Loop through the discussion post's replies
for response in individual_soup.find_all('div', {'class': 'linear-message-list message-list'}):

    # Add the name of the discussion to a list so we know what the response was for
    response_discussions.append(discussion_name)

    # Scrape the author of each response
    for x in response.find_all('div', {'class': 'lia-message-author-with-avatar'}):
        for response_author in x.find_all('a'):
            response_authors.append(response_author.get(
                'aria-label').lstrip('View Profile of '))
        time.sleep(5)

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
        time.sleep(5)

    # Scrape the number of likes for each response
    for response_like in response.find_all('span', {'class': 'MessageKudosCount lia-component-kudos-widget-message-kudos-count'}):
        response_likes.append(
            (re.search('\n\t\n\t\t\t(.*?.) Likes\n\t\t\n', response_like.get_text())).group(1))
        time.sleep(5)

        # Scrape the date of each response
    for response_date in response.find_all('span', {'class': 'local-date'}):
        response_dates.append(response_date.get_text().lstrip('\u200e'))
        time.sleep(5)

    # Scrape the time of each response
    for response_time in response.find_all('span', {'class': 'local-time'}):
        response_times.append(response_time.get_text())
        time.sleep(5)


# Create dataframes from the lists that contain the scraped data
post_df = pd.DataFrame({'URL': discussion_urls, 'Topic': post_titles, 'Body': post_bodies, 'Likes': post_likes,
                       'Tags': post_tags, 'Labels': post_labels, 'Author': post_authors, 'Date': post_dates, 'Time': post_times})
response_df = pd.DataFrame({'Discussion Title': response_discussions, 'Body': response_bodies,
                           'Likes': response_likes, 'Author': response_authors, 'Date': response_dates, 'Time': response_times})

print(page_titles)
print(discussion_urls)
print(post_titles)