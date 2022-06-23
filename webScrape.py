# Import necessary classes
import requests
from bs4 import BeautifulSoup
import re


class webScrape:
    # Initializer function
    def __init__(self, url):
        self.url = url

    # Function to extract html from a given url and parse through the data
    def getHTML(self):

        # Request the HTML from the url
        page = requests.get(self.url)

        # Use BeautifulSoup to parse through the html
        soup = BeautifulSoup(page.content, 'html.parser')

        # Create an empty list to hold the discussion page URLs
        discussion_groups = []
        # Find all anchor tags with "href" to get the links for the different discussion groups
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):

            # Add each link to the end of the list
            discussion_groups.append(link.get('href'))

        # Return the list of discussion group URLs
        return discussion_groups


# Test getHTML() functionality
def test_getHTML():
    # Assign palo alto discussion home page to the url variable
    url = "https://live.paloaltonetworks.com/t5/discussions/ct-p/members"

    # Initialize webscrape class to test
    getHTML_check = webScrape(url)

    # Check if getHTML() works
    get_list = getHTML_check.getHTML()

    print(get_list)

# Test if the function will work


def main():
    print("Checking if the discussion group links can successfully be scraped")
    test_getHTML()


if __name__ == '__main__':
    main()
