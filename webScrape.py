# Import necessary classes
import requests
from bs4 import BeautifulSoup

# Read in the URL
#discussionHome_url = "https://live.paloaltonetworks.com/t5/discussions/ct-p/members"

# Get the page content
#discussionHome_page = requests.get(discussionHome_url)

# Use beautiful soup to parse the page
#soup = BeautifulSoup(discussionHome_page.content, 'html.parser')
# print(soup.prettify)

#tag_a = soup.find_all("a")
# tag_a.string
# for string in soup.stripped_strings:
#    print(repr(string))


#discussionHome_titles = soup.find_all('h3', a_='href')
# print(discussionHome_titles)

# for x in soup.find('div', class_='custom-tiled.node-navigation'):
#   title =

# Read in discussion page urls
# Maybe make into a dictionary
generalPost_url = "https://live.paloaltonetworks.com/t5/general-topics/bd-p/members_discuss"
bestPractice_url = "https://live.paloaltonetworks.com/t5/best-practice-assessment/bd-p/Best_Practice_Assessment_Discussions"
cortexXDR_url = "https://live.paloaltonetworks.com/t5/cortex-xdr-discussions/bd-p/Analytics_Discussions"
cortexXSOAR_url = "https://live.paloaltonetworks.com/t5/cortex-xsoar-discussions/bd-p/Cortex_XSOAR_Discussions"
customSignatures_url = "https://live.paloaltonetworks.com/t5/custom-signatures/bd-p/CustomSignatures"
endpoint_url = "https://live.paloaltonetworks.com/t5/endpoint-traps-discussions/bd-p/Endpoint_Discussions"
globalProtect_url = "https://live.paloaltonetworks.com/t5/globalprotect-discussions/bd-p/GlobalProtect_Discussions"
nextGenFirewalls_url = "https://live.paloaltonetworks.com/t5/next-generation-firewall/bd-p/NGFW_Discussions"
prismaAccessInsights_url = "https://live.paloaltonetworks.com/t5/prisma-access-insights/bd-p/Prisma_Access_Insights_Discussions"
panorama_url = "https://live.paloaltonetworks.com/t5/panorama-discussions/bd-p/Panorama_Discussions"
prismaAccess_url = "https://live.paloaltonetworks.com/t5/prisma-access-discussions/bd-p/Prisma_Access_Discussions"
virusTotal_url = "https://live.paloaltonetworks.com/t5/virustotal/bd-p/VirusTotal_Discussions"
prismaCloud_url = "https://live.paloaltonetworks.com/t5/prisma-cloud-discussions/bd-p/Prisma_Cloud_Discussions"
threatVulnerability_url = "https://live.paloaltonetworks.com/t5/threat-vulnerability-discussions/bd-p/Threat_Discussions"
vmPrivate_url = "https://live.paloaltonetworks.com/t5/vm-series-in-the-private-cloud/bd-p/Private_Cloud_Discussions"
vmPublic_url = "https://live.paloaltonetworks.com/t5/vm-series-in-the-public-cloud/bd-p/AWS_Azure_Discussions"

# Get each page's content
