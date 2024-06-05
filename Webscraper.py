import requests
from bs4 import BeautifulSoup as Bs
import csv
import json
import xml.etree.ElementTree as ET

def scraper(url, output_form, content_type):
    # Scrape content from the website URL provided
    res = requests.get(url)

    # Check if the connection was successful
    if res.status_code != 200:
        print("Failed to connect to the website URL provided. Please check the URL once.")
        return
    
    # Parse/Extract the HTML content
    out = Bs(res.text, "html.parser")

    # Extract specific content based on content_type
    #if HTML
    if content_type == 'html':
        data = out.prettify()
    
    #if paragraphs
    elif content_type == 'paragraphs':
        data = [p.get_text() for p in out.find_all('p')]
        if not data:
            print("No paragraphs found.")
            return
        
    #if tables
    elif content_type == 'tables':
        data = []
        tables = out.find_all('table')
        if not tables:
            print("No tables found.")
            return
        for table in tables:
            table_data = []
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                cols = [ele.text.strip() for ele in cols]
                table_data.append(cols)
            data.append(table_data)
    else:
        print("Unsupported content type.")
        return

    # Save the data in the required format
    #CSV
    if output_form == 'csv':
        with open('output.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if content_type == 'paragraphs':
                for item in data:
                    writer.writerow([item])
            elif content_type == 'tables':
                for table in data:
                    for row in table:
                        writer.writerow(row)
            elif content_type == 'html':
                writer.writerow([data])
        print("Data saved in output.csv")
    
    #JSON
    elif output_form == 'json':
        with open('output.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Data saved in output.json")
    
    #XML
    elif output_form == 'xml':
        root = ET.Element("data")
        if content_type == 'paragraphs':
            for p in data:
                child = ET.SubElement(root, "paragraph")
                child.text = p
        elif content_type == 'tables':
            for table in data:
                table_element = ET.SubElement(root, "table")
                for row in table:
                    row_element = ET.SubElement(table_element, "row")
                    for col in row:
                        col_element = ET.SubElement(row_element, "column")
                        col_element.text = col
        elif content_type == 'html':
            child = ET.SubElement(root, "html")
            child.text = data
        tree = ET.ElementTree(root)
        tree.write("output.xml", encoding='utf-8', xml_declaration=True)
        print("Data saved in output.xml")
    else:
        print("Unsupported format. Please choose from 'csv', 'json', or 'xml'.")

URL = input("Enter URL you want to scrape (make sure the website allows scraping): ")
output_format = input("Enter the desired output format (csv, json, xml): ")
content_type = input("Enter the content type to store (html, paragraphs, tables, etc.): ")
scraper(URL, output_format, content_type)
