import csv
import requests
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin

site_url = "https://books.toscrape.com/index.html"
all_data = []


def scrape(url):
    try:
        r = requests.get(url)
        print(url)
        doc = BeautifulSoup(r.text, "html.parser")
        for product in doc.select(".product_pod"):
            product_page_link = product.select_one(".image_container").select_one("a")["href"]
            product_page_url = urljoin(url, product_page_link)
            all_data.append(scrape_details(product_page_url))

        next_button = doc.select_one(".next")
        if next_button:
            next_href = next_button.a["href"]
            next_href = urljoin(url, next_href)
            url = next_href
            scrape(url)

    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError occurred!\nWaiting 3 seconds to reconnect...")
        sleep(3)
        scrape(url)


def scrape_details(product_url):
    r = requests.get(product_url)
    doc = BeautifulSoup(r.text, "html.parser")
    prod_category = doc.select(".breadcrumb a")[-1].text
    for detail in doc.select(".product_page"):
        prod_title = detail.select_one(".product_main").select_one("h1").text
        prod_review_rating = detail.select_one(".star-rating").attrs["class"][1]
        prod_img_link = detail.select_one(".thumbnail").img["src"]
        prod_img_url = urljoin(site_url, prod_img_link)
        prod_description = detail.find("p", class_=False).text
        prod_info_table = detail.select_one(".table-striped").select("tr")
        prod_details = {
            prod_title: {
                "Product_Page_URL": product_url,
                "Description": prod_description,
                "Category": prod_category,
                "Image_URL": prod_img_url,
                "Review Rating": f"{prod_review_rating} Stars"}}
        for tr in prod_info_table:
            keyword = tr.select_one("th").text
            value = tr.select_one("td").text
            prod_details[prod_title][keyword] = value

    return prod_details


print(scrape_details("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"))
print(scrape_details("https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"))
# scrape(site_url)


