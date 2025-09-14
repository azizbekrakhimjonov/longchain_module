import requests
from bs4 import BeautifulSoup

def search_olx(query, max_results=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Create OLX search URL
    search_url = f"https://www.olx.uz/list/q-{query.replace(' ', '-')}/"

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch data from OLX")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # Find product listings
    for item in soup.select("div.css-1sw7q4x")[:max_results]:
        title_tag = item.select_one("h6")
        price_tag = item.select_one("p[data-testid='ad-price']")
        link_tag = item.find("a", href=True)

        title = title_tag.get_text(strip=True) if title_tag else "No title"
        price = price_tag.get_text(strip=True) if price_tag else "No price"
        link = "https://www.olx.uz" + link_tag["href"] if link_tag else "No link"

        results.append({
            "title": title,
            "price": price,
            "link": link
        })

    return results


# Example usage
if __name__ == "__main__":
    query = input("Enter product to search: ")
    products = search_olx(query)

    if products:
        for idx, product in enumerate(products, 1):
            print(f"\n{idx}. {product['title']}")
            print(f"   Price: {product['price']}")
            print(f"   Link: {product['link']}")
    else:
        print("No products found.")
