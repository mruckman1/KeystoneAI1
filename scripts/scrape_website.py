import requests
from bs4 import BeautifulSoup
import os

# Step 1: Set up the URL for the main page and initialize headers
base_url = 'https://www.keystone.ai/our-people'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

# File path for saving the output
output_file = '/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/data/our_people.txt'

# Step 2: Request the main "Our People" page
response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Locate all team member profile links
profile_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if '/our-people/' in href and href != '/our-people':  # Filter to only profile links
        full_link = 'https://www.keystone.ai' + href if href.startswith('/') else href
        profile_links.append(full_link)

# Function to scrape an individual profile
def scrape_profile(url):
    profile_data = {}
    response = requests.get(url, headers=headers)
    profile_soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract name
    name = profile_soup.find('h1').text.strip() if profile_soup.find('h1') else ''
    profile_data['Name'] = name
    
    # Extract position
    position_div = profile_soup.find('div', class_='c-title-6')
    position = position_div.text.strip() if position_div else ''
    profile_data['Position'] = position
    
    # Extract biography
    bio_div = profile_soup.find('div', class_='c-global-richtext w-richtext')
    bio = bio_div.text.strip() if bio_div else ''
    profile_data['Biography'] = bio
    
    # Extract education information
    education_section = profile_soup.find('h3', text="Education")
    education_list = []
    if education_section:
        for item in education_section.find_next('ul').find_all('li'):
            education_list.append(item.text.strip())
    profile_data['Education'] = '; '.join(education_list)  # Join education items with a semicolon for a single string
    
    return profile_data

# Step 5: Loop through each profile, store the extracted data, and write to file
profiles_data = []
with open(output_file, 'w') as f:
    # Write the header
    f.write("Name,Position,Biography,Education\n")
    
    for link in profile_links:
        profile_info = scrape_profile(link)
        
        # Format each profile's information as a comma-separated line
        line = f"{profile_info['Name']},{profile_info['Position']},{profile_info['Biography']},{profile_info['Education']}\n"
        
        # Write the formatted line to the file
        f.write(line)
        profiles_data.append(profile_info)  # Optional: keep in memory if further processing is needed

print(f"Data saved to {output_file}")
