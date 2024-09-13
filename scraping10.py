import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the webpage
url = "https://onepiece.fandom.com/es/wiki/Tony_Tony_Chopper/Habilidades_y_poderes#Arm_Point"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Create lists to store the title and content data
titles = []
contents = []

# Extract the <h1>, <h2>, <h3> titles and corresponding <p>, <div> contents
for element in soup.find_all(['h1', 'h2', 'h3']):
    if element.text.strip() == "Enlaces externos":
        break  # stop extracting when we reach the "Enlaces externos" section
    title = element.text.strip()
    for link in element.find_all('a'):
        title += ' ' + link.text.strip()
    paragraphs = element.find_all(['p', 'div'])
    content = ''
    for paragraph in paragraphs:
        for text in paragraph.find_all(string=True):
            content += text.strip() + ' '
        for link in paragraph.find_all('a'):
            content += ''
    content = ' '.join(set(content.split()))  # remove duplicates and whitespace
    titles.append(title)
    contents.append(content)

# Extract the <ul> titles and corresponding <li> contents
for ul in soup.find_all('ul'):
    previous_heading = ul.find_previous(['h1', 'h2', 'h3'])
    if previous_heading and previous_heading.text.strip() != "Enlaces externos":
        title = previous_heading.text.strip()
        for link in previous_heading.find_all('a'):
            title += ' ' + link.text.strip()
    else:
        continue  # skip if no previous heading or if it's "Enlaces externos"
    content = ''
    for li in ul.find_all('li'):
        for text in li.find_all(string=True):
            content += text.strip() + ' '
        for link in li.find_all('a'):
            content += ''
    content = ' '.join(set(content.split()))  # remove duplicates and whitespace
    titles.append(title)
    contents.append(content)

# Remove Unknown titles and contents
titles = [title for title in titles if title != "Unknown"]
contents = [content for content in contents if content != "Unknown"]

# Create a Pandas DataFrame from the lists
df = pd.DataFrame({'Title': titles, 'Content': contents})

# Remove whitespace and duplicates from the content column
df['Content'] = df['Content'].apply(lambda x: ' '.join(set(x.split())))

# Write the DataFrame to a CSV file
df.to_csv('chopper_powers.csv', index=False)