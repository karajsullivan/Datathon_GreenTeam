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

# Create an empty list for the extra discussion groups
extra_discussion_groups = []

# Create an empty list for the urls we want to delete
delete_url = []

# Some of the discussion pages take you to a new page with new discussion pages instead of to the discussion posts
# We want to get those URLs too
# Loop through the first list of discussion groups
for extra_url in discussion_groups_url:
    # Read in the page
    extra_page = requests.get(extra_url)

    # Parse through the page using beautiful soup
    extra_soup = BeautifulSoup(extra_page.content, 'html.parser')

    # Loop through the new page to get the URLs of the discussion groups
    for x in extra_soup.find_all('div', {'class': 'custom-tiled-node-navigation'}):
        for extra_link in x.find_all('a', attrs={'href': re.compile("^/t5/")}):
            if extra_link.get('href') not in extra_discussion_groups:
                # Add the link to the new list for the extra URLs that was created
                extra_discussion_groups.append(extra_link.get('href'))
        # We want to add the URL of the pages that hold extra URLs to the delete_url list that was initialized earlier
        delete_url.append(extra_url)

# Concatenate the url that we scraped and the base url
extra_discussion_groups_urls = [base_url + x for x in extra_discussion_groups]

# We now want to go through the discussion_groups_url list and delete any URLs that are also in the delete_url list
# We will do this by a creating a new list that will only include URLs that are NOT in delete_url
all_discussion_groups_urls = [
    x for x in discussion_groups_url if x not in delete_url]

# Now we want to append the new URLs to the all_discussion_groups_urls
for url in extra_discussion_groups_urls:
    all_discussion_groups_urls.append(url)


# Initialize lists of information based off Ethan's datathon schema

# This first group of lists can be scraped from the discussion group page
page_titles = []
post_titles = []
post_bodies = []
post_likes = []
post_replies = []
post_views = []
post_authors = []
post_authorLabel = []

# This next group of lists are scraped from the individual discussion post page
post_labels = []
post_tags = []
post_dates = []
post_times = []
post_solution = []
response_authors = []
response_discussions = []
response_bodies = []
response_likes = []
response_dates = []
response_times = []

# This list will hold the individual discussion post's URL and will act as the unique id for the posts dataframe
discussion_urls = []

# Initializing an empty string for the title of the discussion page
page_title = ''

# Create an empty list for the 'next page' links to be added to
next_page = []

# Add the first item from all_discussion_groups_urls to next_page so the loop begins with that url
next_page.append(all_discussion_groups_urls[0])

# Loop through the list of the web pages we want to scrape to extract information
for index, url in enumerate(next_page):
    # Read in the page
    page = requests.get(url)

    # Parse through the page using beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the title of the discussion page the discussion was posted on
    for title in soup.find_all('title'):
        page_title = title.get_text()

    # Go through the discussion posts on each page
    for x in soup.find_all('div', {'class': 'custom-message-list'}):

        # Add the title of the discussion page to the list
        page_titles.append(page_title)

        # Scrape the titles of the discussion posts
        for title in x.find_all('a'):
            if title.get('title') not in post_titles:
                post_titles.append(title.get('title'))

        # Scrape the number of likes
        for y in x.find_all('li', {'class': 'custom-tile-kudos'}):
            for like in y.find_all('b'):
                post_likes.append(like.get_text())

        # Scrape the number of views
        for y in x.find_all('li', {'class': 'custom-tile-views'}):
            for view in y.find_all('b'):
                post_views.append(view.get_text())

        # Scrape the number of replies
        for y in x.find_all('li', {'class': 'custom-tile-replies'}):
            for reply in y.find_all('b'):
                post_replies.append(reply.get_text())

        # Scrape the author
        for author in x.find_all('img', {'class': 'lia-user-avatar-message'}):
            post_authors.append(author.get('alt'))

        # Scrape the author label
        for y in x.find_all('div', {'class': 'custom-tile-author-info'}):
            for authorLabel in y.find('em'):
                post_authorLabel.append(authorLabel.get_text())

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
        # Add the URL to the list so it can be used as the unique id for the post table
        discussion_urls = [link for link in individual_discussions_urls]

        # Loop through the individual discussion post links and scrape the data within the page
        for individual_discussion_url in individual_discussions_urls:

            # Read in the indvidual discussion page
            individual_page = requests.get(individual_discussion_url)

            # Parse through the page using beautiful soup
            individual_soup = BeautifulSoup(
                individual_page.content, 'html.parser')

            # Scrape the body
            # Create an empty string for the different parts of the body to be appended to
            body_content = ''
            post = individual_soup.find(
                'div', {'class': 'lia-message-body-content'})
            for body in post.find_all('p'):
                body_content += body.get_text()
            post_bodies.append(body_content)

            # Scrape the labels of the discussion post
            # Initialize an empty string for the labels to be concatenated into
            discussion_label = ''
            # Not every discussion post has labels, so if they don't they will automatically be given a 'None' value
            try:
                # Loop through the labels
                for label in individual_soup.find_all('li', {'class': 'label'}):
                    discussion_label += ', ' + \
                        re.search('\n(.*?.)\n', (label.get_text())).group(1)
                # Add the individual discussion post's labels to the label list
                post_labels.append(discussion_label)
            except:
                post_labels.append(None)

            # Scrape the tags of the discussion post
            # Initialize an empty string for the tags to be concatenated into
            discussion_tag = ''
            # Not every discussion post hsa tags, so if they don't they will automatically be given a 'None' value
            try:
                # Loop through the tags
                for y in individual_soup.find_all('div', id='taglist'):
                    for tag in y.find_all('a'):
                        discussion_tag += ', ' + tag.get_text()
                # Add the individual discussion post's tags to the tag list
                post_tags.append(discussion_tag)
            except:
                post_tags.append(None)

            # Scrape the date of the discussion post
            try:
                post_dates.append(individual_soup.find(
                    'span', {'class': 'local-date'}).get_text().lstrip('\u200e'))
            except:
                post_dates.append(None)

            # Scrape the time of the discussion post
            try:
                post_times.append(individual_soup.find(
                    'span', {'class': 'local-time'}).get_text())
            except:
                post_times.append(None)

            # Get a variable with the name of the discussion post
            for x in individual_soup.find_all('h1', {'class': 'lia-node-header-title'}):
                discussion_name = x.get_text()

            # Get the link of the solution for that discussion post if there is 1
            # If there isn't a solution, it will store 'None' as the value
            solution = ''
            for x in individual_soup.find_all('div', {'class': 'solution-link-wrapper'}):
                for link in x.find_all('a', attrs={'href': re.compile("^/t5/")}):
                    solution = (base_url + link.get('href'))
            for x in individual_soup.find_all('div', {'class': 'solution-link-wrapper lia-mark-empty'}):
                if solution == '':
                    solution = None
            post_solution.append(solution)

            # Loop through the discussion post's replies
            for response in individual_soup.find_all('div', {'class': 'lia-component-message-list-detail-with-inline-editors'}):

                # Add the name of the discussion to a list so we know what the response was for
                response_discussions.append(discussion_name)

                # Scrape the author of each response
                for x in response.find_all('div', {'class': 'lia-message-author-with-avatar'}):
                    for response_author in x.find_all('a'):
                        response_authors.append(
                            response_author.get('aria-label'))

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
                    response_likes.append(response_like.get_text())

                # Scrape the date of each response
                for response_date in response.find_all('span', {'class': 'local-date'}):
                    response_dates.append(
                        response_date.get_text().lstrip('\u200e'))

                # Scrape the time of each response
                for response_time in response.find_all('span', {'class': 'local-time'}):
                    response_times.append(response_time.get_text())

            # Lag for 3 seconds between each discussion post
            time.sleep(3)

    # Make sure to get the next page in that discussion group page
    for next in soup.find_all('li', {'class': 'lia-paging-page-next lia-component-next'}):
        next_url = next.find('a').get('href')

    # Add that url to the next index of the list we are iterating through
    next_page.append(next_url)


# Create dataframes from the lists that contain the scraped data
post_df = pd.DataFrame({'Author': post_authors, 'Author Label': post_authorLabel, 'Topic': post_titles, 'Body': post_bodies, 'Likes': post_likes, 'Views': post_views,
                       'Replies': post_replies, 'Tags': post_tags, 'Labels': post_labels,  'Solution Link': post_solution, 'Date': post_dates, 'Time': post_times})
response_df = pd.DataFrame({'Discussion Title': response_discussions, 'Author': response_authors,
                           'Body': response_bodies, 'Likes': response_likes, 'Date': response_dates, 'Time': response_times})

'''
# Test the functionality using just 1 of the sites to not overwhelm the site
test_url = "https://live.paloaltonetworks.com/t5/next-generation-firewall/bd-p/NGFW_Discussions"
print(test_url)
test_page = requests.get(test_url)
test_soup = BeautifulSoup(test_page.content, 'html.parser')
for next in test_soup.find_all('li', {'class': 'lia-paging-page-next lia-component-next'}):
    next_url = next.find('a').get('href')
print(next_url)
page_title = ''


# Test the functionality of just scraping one of the individual discussion post pages
#test_individual_url = individual_discussions_urls[8]
test_individual_url = "https://live.paloaltonetworks.com/t5/next-generation-firewall/palo-alto-denying-the-traffic-randamly/td-p/507446"
print(test_individual_url)
test_individual_page = requests.get(test_individual_url)
test_individual_soup = BeautifulSoup(
    test_individual_page.content, 'html.parser')
body_content = ''
post = test_individual_soup.find('div', {'class': 'lia-message-body-content'})
for body in post.find_all('p'):
    body_content += body.get_text()
post_bodies.append(body_content)

print(body_content)
'''
