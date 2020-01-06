import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
	r = requests.get(url)
	return r.text


def get_total_pages(html):
	soup = BeautifulSoup(html, 'html.parser')

	pages = soup.find('ul', class_ = 'pagn').find_all('a')[-1].get('href')
	total_pages = pages.split('=')[-1]

	return int(total_pages)


def write_csv(data):
	with open('lalafo2.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerow( (data['name'], data['price'], data['photo']) )


def get_page_data(html):
	soup = BeautifulSoup(html, 'html.parser' )
	ads = soup.find('div', id = 'main-listing-block').find_all('article', class_ = 'listing-item')
	for ad in ads:
		#name , price, photo

		try:
			name = ad.find('a', class_ = 'item').text.strip()
			print(name)
		except:
			name = ""

		try:
			price = ad.find('p', class_ = 'listing-item-title').text.strip()
			new_price = price.replace(u'\xa0', ' ')
			print(new_price)
		except:
			price = ''

		try:
			photo = ad.find('img', class_ = 'listing-item-photo').get('src')
		except:
			photo = ''

		data = {'name':name, 'price':new_price, 'photo':photo}
		write_csv(data )

def main():
	url = 'https://lalafo.kg/en/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnyetelefony?'
	page_part = 'page='
	total_pages = get_total_pages(get_html(url))
	for i in range(1, total_pages + 1):
		url_gen = url + page_part + str(i)
		# print(url_gen)
		html = get_html(url_gen)
		get_page_data(html)

if __name__ == '__main__':
	main()