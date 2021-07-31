import csv
import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path


def scrape_categories(url):
    # takes homepage-URL and returns a dictionary with the category-name as key, and the link as value.
    category_links = {}
    while not category_links:
        try:
            r = requests.get(url)
            doc = BeautifulSoup(r.text.encode(r.encoding), "html.parser")

            for category in doc.select_one(".nav-list ul").select("li a"):
                category_name = category.text.strip()
                category_page_link = category["href"]
                category_page_url = urljoin(url, category_page_link)
                category_links[category_name] = category_page_url

        except requests.exceptions.ConnectionError:
            print("\nConnectionError occurred in scrape_categories!\nWaiting 3 seconds to reconnect...\n")
            sleep(3)

    return category_links


def scrape_products(category_url):
    # takes a category-URL and returns a list of all the product-links from that category.
    product_urls = []
    while category_url != "":
        try:
            r = requests.get(category_url)
            doc = BeautifulSoup(r.text.encode(r.encoding), "html.parser")
            for product in doc.select(".product_pod"):
                product_page_link = product.select_one(".image_container").select_one("a")["href"]
                product_page_url = urljoin(category_url, product_page_link)
                product_urls.append(product_page_url)

            next_button = doc.select_one(".next")
            if next_button:
                next_href = next_button.a["href"]
                next_href = urljoin(category_url, next_href)
                category_url = next_href
            else:
                category_url = ""

        except requests.exceptions.ConnectionError:
            print("\nConnectionError occurred in scrape_products!\nWaiting 3 seconds to reconnect...\n")
            sleep(3)

    return product_urls


def scrape_details(product_url):
    # takes a product-URL and returns a dictionary with all required details.
    prod_details = {}
    while not prod_details:
        try:
            r = requests.get(product_url)
            doc = BeautifulSoup(r.text.encode(r.encoding), "html.parser")
            prod_category = doc.select(".breadcrumb a")[-1].text
            details = doc.select_one(".product_page")
            prod_title = details.select_one(".product_main").select_one("h1").text
            prod_review_rating = details.select_one(".star-rating").attrs["class"][1]
            prod_img_link = details.select_one(".thumbnail").img["src"]
            prod_img_url = urljoin(site_url, prod_img_link)
            prod_description = details.find("p", class_=False)
            if prod_description is None:
                prod_description = "Description currently not available"
            else:
                prod_description = prod_description.text
            prod_info_table = details.select_one(".table-striped").select("tr")
            prod_details = {
                "Title": prod_title,
                "Product Page URL": product_url,
                "Description": prod_description,
                "Category": prod_category,
                "Image URL": prod_img_url,
                "Review Rating": f"{prod_review_rating} Star(s) out of five"
            }
            for tr in prod_info_table:
                keyword = tr.select_one("th").text
                value = tr.select_one("td").text
                prod_details[keyword] = value

        except requests.exceptions.ConnectionError:
            print("\nConnectionError occurred in scrape_details!\nWaiting 3 seconds to reconnect...\n")
            sleep(3)

    return prod_details


def save_img(category, title, img_url):
    # Saves the image of the URL, named after the title, in the directory named after the category.
    img_name = re.sub('[<>:"/|?*\\\\]', '-', title)
    img = False
    while not img:
        try:
            img = requests.get(img_url)
            with open(f"Product Images/{category}/{img_name}.jpg", "wb") as image:
                image.write(img.content)
        except requests.exceptions.ConnectionError:
            img = False
            sleep(3)
            print("\nConnectionError occurred in save_img!\nWaiting 3 seconds to reconnect...\n")


site_url = "https://books.toscrape.com/index.html"
Path("Created CSV Files").mkdir(parents=True, exist_ok=True)
categories = scrape_categories(site_url)
total_number = len(categories)
count = 1

header = ["Title", "Product Page URL", "UPC", "Price (excl. tax)",
          "Price (incl. tax)", "Availability", "Description",
          "Category", "Review Rating", "Image URL"]

print(f"\n{total_number} categories found...")
for (cat_name, cat_link) in categories.items():
    Path(f"Product Images/{cat_name}").mkdir(parents=True, exist_ok=True)
    print(f"\nCategory {count} of {total_number}: {cat_name}\n")
    with open(f"Created CSV Files/{cat_name}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for book in scrape_products(cat_link):
            detail = scrape_details(book)
            writer.writerow({i: detail[i] for i in header})
            save_img(cat_name, detail['Title'], detail["Image URL"])
            print(f"{detail['Title']} - done")
    count += 1
