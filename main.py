import csv
import requests
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_categories(url):
    # takes Homepage-URL and returns a Dictionary with the Category-Name as key, and the Link as value.
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
            print("ConnectionError occurred in scrape_categories!\nWaiting 3 seconds to reconnect...")
            sleep(3)

    return category_links


def scrape_products(category_url):
    # takes a Category-URL and returns a list of all the product-Links from that category.
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
            print("ConnectionError occurred in scrape_from_category!\nWaiting 3 seconds to reconnect...")
            sleep(3)

    return product_urls


def scrape_details(product_url):
    # takes a product-URL and returns a dictionary with all requested details.
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
            print("ConnectionError occurred in scrape_details!\nWaiting 3 seconds to reconnect...")
            sleep(3)

    return prod_details


site_url = "https://books.toscrape.com/index.html"
categories = scrape_categories(site_url)
print(f"\n{len(categories)} categories found...")

header = ["Title", "Product Page URL", "UPC", "Price (excl. tax)",
          "Price (incl. tax)", "Availability", "Description",
          "Category", "Review Rating", "Image URL"]

for (cat_name, cat_link) in categories.items():
    print(f"\nCurrent category: {cat_name}\n")
    with open(f"Created CSV Files/{cat_name}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for book in scrape_products(cat_link):
            detail = scrape_details(book)
            writer.writerow({i: detail[i] for i in header})
            print(f"{detail['Title']} analysed")
