import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin, quote


class OLXScraper:
    def __init__(self):
        self.base_url = "https://www.olx.uz"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'uz-UZ,uz;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def search_products(self, query, category="", location="", max_pages=3):
        """
        OLX saytidan mahsulotlarni qidiradi

        Args:
            query (str): Qidiruv so'zi
            category (str): Kategoriya (ixtiyoriy)
            location (str): Joylashuv (ixtiyoriy)
            max_pages (int): Maksimal sahifalar soni

        Returns:
            list: Topilgan e'lonlar ro'yxati
        """
        results = []

        # Qidiruv URL yaratish
        search_url = f"{self.base_url}/uz/q-{quote(query)}"
        if category:
            search_url += f"/c-{category}"
        if location:
            search_url += f"/{location}"

        print(f"Qidiruv boshlandi: {query}")
        print(f"URL: {search_url}")

        for page in range(1, max_pages + 1):
            try:
                page_url = f"{search_url}/?page={page}"
                print(f"\nSahifa {page} yuklanmoqda...")

                response = self.session.get(page_url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # E'lonlarni topish
                ads = soup.find_all('div', {'data-cy': 'l-card'}) or soup.find_all('div', class_='css-1sw7q4x')

                if not ads:
                    print("Bu sahifada e'lonlar topilmadi")
                    break

                for ad in ads:
                    try:
                        ad_data = self.parse_ad(ad)
                        if ad_data:
                            results.append(ad_data)
                    except Exception as e:
                        print(f"E'lonni o'qishda xatolik: {e}")
                        continue

                print(f"Sahifa {page}dan {len([ad for ad in ads if self.parse_ad(ad)])} ta e'lon topildi")

                # Sahifalar orasida pauza
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"Sahifa {page}ni yuklashda xatolik: {e}")
                break
            except Exception as e:
                print(f"Umumiy xatolik sahifa {page}: {e}")
                break

        return results

    def parse_ad(self, ad_element):
        """
        Bitta e'lon ma'lumotlarini ajratib oladi
        """
        try:
            # Sarlavha
            title_elem = ad_element.find('h6') or ad_element.find('h4') or ad_element.find('a', class_='css-rc5s2u')
            title = title_elem.get_text(strip=True) if title_elem else "Sarlavha topilmadi"

            # Narx
            price_elem = ad_element.find('p', {'data-testid': 'ad-price'}) or ad_element.find('span',
                                                                                              class_='css-10b0gli')
            price = price_elem.get_text(strip=True) if price_elem else "Narx ko'rsatilmagan"

            # Havola
            link_elem = ad_element.find('a', href=True)
            link = urljoin(self.base_url, link_elem['href']) if link_elem else ""

            # Joylashuv
            location_elem = ad_element.find('p', {'data-testid': 'location-date'}) or ad_element.find('span',
                                                                                                      class_='css-643j0o')
            location = location_elem.get_text(strip=True) if location_elem else "Joylashuv ko'rsatilmagan"

            # Rasm
            img_elem = ad_element.find('img')
            image_url = img_elem.get('src', '') if img_elem else ""

            return {
                'title': title,
                'price': price,
                'location': location,
                'link': link,
                'image_url': image_url
            }

        except Exception as e:
            print(f"E'lonni tahlil qilishda xatolik: {e}")
            return None

    def get_ad_details(self, ad_url):
        """
        E'lonning batafsil ma'lumotlarini oladi
        """
        try:
            response = self.session.get(ad_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Batafsil ma'lumotlar
            details = {}

            # Tavsif
            description_elem = soup.find('div', {'data-cy': 'ad_description'})
            details['description'] = description_elem.get_text(strip=True) if description_elem else ""

            # Xususiyatlar
            features = {}
            feature_items = soup.find_all('p', class_='css-b5m1rv') or soup.find_all('div', class_='css-1ti8b9t')

            for item in feature_items:
                try:
                    key_elem = item.find('span', class_='css-643j0o')
                    value_elem = item.find('span', class_='css-1p8lxx0')

                    if key_elem and value_elem:
                        key = key_elem.get_text(strip=True)
                        value = value_elem.get_text(strip=True)
                        features[key] = value
                except:
                    continue

            details['features'] = features

            # Telefon raqam (agar mavjud bo'lsa)
            phone_elem = soup.find('a', href=lambda x: x and 'tel:' in x)
            details['phone'] = phone_elem['href'].replace('tel:', '') if phone_elem else ""

            return details

        except Exception as e:
            print(f"Batafsil ma'lumotlarni olishda xatolik: {e}")
            return {}

    def save_results(self, results, filename='olx_results.json'):
        """
        Natijalarni faylga saqlaydi
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\nNatijalar {filename} fayliga saqlandi")
        except Exception as e:
            print(f"Faylga saqlashda xatolik: {e}")

    def print_results(self, results):
        """
        Natijalarni chiroyli formatda chiqaradi
        """
        print(f"\n{'=' * 60}")
        print(f"JAMI TOPILDI: {len(results)} ta e'lon")
        print(f"{'=' * 60}")

        for i, ad in enumerate(results, 1):
            print(f"\n{i}. {ad['title']}")
            print(f"   Narx: {ad['price']}")
            print(f"   Joylashuv: {ad['location']}")
            print(f"   Havola: {ad['link']}")
            print(f"   {'-' * 50}")


def main():
    """
    Asosiy funksiya - dasturni ishga tushiradi
    """
    scraper = OLXScraper()

    print("OLX Qidiruv Dasturi")
    print("=" * 30)

    # Foydalanuvchidan ma'lumotlarni olish
    query = input("Qidiruv so'zini kiriting: ").strip()

    if not query:
        print("Qidiruv so'zi kiritilmadi!")
        return

    max_pages = input("Necha sahifa qidirish kerak? (standart: 3): ").strip()
    try:
        max_pages = int(max_pages) if max_pages else 3
    except ValueError:
        max_pages = 3

    location = input("Joylashuv (ixtiyoriy, bo'sh qoldiring): ").strip()

    # Qidiruvni boshlash
    print("\nQidiruv boshlandi...")
    results = scraper.search_products(query, location=location, max_pages=max_pages)

    if results:
        # Natijalarni ko'rsatish
        scraper.print_results(results)

        # Faylga saqlash
        save_option = input("\nNatijalarni faylga saqlaysizmi? (y/n): ").strip().lower()
        if save_option in ['y', 'yes', 'ha', 'h']:
            filename = input("Fayl nomi (standart: olx_results.json): ").strip()
            filename = filename if filename else 'olx_results.json'
            scraper.save_results(results, filename)

        # Batafsil ma'lumot olish
        detail_option = input("\nBiror e'lonning batafsil ma'lumotini ko'rasizmi? (y/n): ").strip().lower()
        if detail_option in ['y', 'yes', 'ha', 'h']:
            try:
                ad_number = int(input(f"E'lon raqamini kiriting (1-{len(results)}): ")) - 1
                if 0 <= ad_number < len(results):
                    print("\nBatafsil ma'lumotlar yuklanmoqda...")
                    details = scraper.get_ad_details(results[ad_number]['link'])

                    print(f"\n{'=' * 50}")
                    print("BATAFSIL MA'LUMOTLAR")
                    print(f"{'=' * 50}")
                    print(f"Sarlavha: {results[ad_number]['title']}")
                    print(f"Tavsif: {details.get('description', 'Tavsif mavjud emas')}")
                    features_text = details.get('features', "Ma'lumot yo'q")
                    print(f"Xususiyatlar: {features_text}")
                    phone_text = details.get('phone', "Ko'rsatilmagan")
                    print(f"Telefon: {phone_text}")
                else:
                    print("Noto'g'ri raqam!")
            except ValueError:
                print("Noto'g'ri raqam formati!")
    else:
        print("Hech qanday e'lon topilmadi!")


if __name__ == "__main__":
    main()