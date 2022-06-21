# Import necessary classes
import requests
from bs4 import BeautifulSoup

discussion_url = "https://live.paloaltonetworks.com/t5/discussions/ct-p/members"
discussion_page = requests.get(discussion_url)

soup = BeautifulSoup(discussion_page.content, 'html.parser')
print(soup.prettify)

data = []

discussion_elements = soup.find_all(
    "div", class_="custom-tiled-node-navigation")

for discussion_element in discussion_elements:
    title_element = discussion_element.find("h3", a="a")
    print(title_element)
