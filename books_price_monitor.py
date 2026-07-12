import requests
from bs4 import BeautifulSoup
import csv
product_page_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(product_page_url)
print(response.status_code)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.title.string)
upc = soup.find("table").find_all("td")[0].text
print(upc)
book_title = soup.find("h1").text
print(book_title)
price_excluding_tax = soup.find("p", class_="price_color").text
print(price_excluding_tax)
price_including_tax = soup.find("table").find_all("td")[3].text
print(price_including_tax)
quantity_available = soup.find("table").find_all("td")[5].text
print(quantity_available)
product_description = soup.find_all("p")[3].text
print(product_description)
category = soup.find("ul", 
                     class_ ="breadcrumb").find_all("a")[2].text
print(category)
review_rating = soup.find("p", class_="star-rating")["class"][1]
print(review_rating)
image_url = soup.find("img")["src"]
print(image_url)
with open("book_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "product_page_url",
        "universal_product_code (upc)",
        "book_title",
        "price_including_tax",
        "price_excluding_tax",
        "quanity_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ])
    writer.writerow([
        product_page_url,
        upc,
        book_title,
        price_including_tax,
        price_excluding_tax,
        quantity_available,
        product_description,
        category,
        review_rating,
        image_url
    ])