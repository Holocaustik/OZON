import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ParserOzon(object):

    def __init__(self, main_divs=None, name_class=None, price_class=None, review_class=None, rat_class=None, sales_class=None, brands=None, pages=None):
        self.divs = main_divs
        self.name_class = name_class
        self.price_class = price_class
        self.review_class = review_class
        self.rat_class = rat_class
        self.sales_class = sales_class
        self.brands = brands
        self.pages = pages

    def get_divs(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(chrome_options=options)
        driver.set_window_size(1440, 900)
        driver.get(f'https://www.ozon.ru/brand/china-dans-85036613/')
        num = driver.page_source.split()
        start_index = num.index('href="/category/elektronika-15500/"')
        category_class = num[start_index + 1:start_index + 2]
        for i in num:
            print(i)

        # r = requests.get('https://www.ozon.ru/brand/china-dans-85036613/')
        # soup = BeautifulSoup(r.text)
        # n = list(soup.text)
        # print(len(n))


    def passer(self):
        result = []
        for brand, adres in self.brands.items():
            print(f'Начили парсить {brand}')
            flag = True
            for page in range(1, self.pages + 1):
                if flag:
                    options = Options()
                    options.headless = True
                    driver = webdriver.Chrome(chrome_options=options)
                    driver.set_window_size(1440, 900)
                    driver.get(f'https://www.ozon.ru/brand/{brand}{adres}?page={page}')
                    for item in self.divs:
                        divs = driver.find_elements_by_class_name(item)
                        if len(divs) > 0:
                            for div in divs:
                                name = ' '.join(div.find_element_by_class_name(self.name_class).text.split())
                                if name not in ['Бестселлер', 'Новинка', 'Есть дешевле внутри',
                                                'Лучшая цена на Ozon'] and '/ шт' not in name and 'Есть дешевле внутри' not in name:
                                    price = div.find_element_by_class_name(self.price_class).text.replace('\u2009','').replace('\n', '').split('₽')
                                    try:
                                        review = div.find_element_by_class_name(self.review_class).text.split()
                                    except:
                                        pass
                                    try:
                                        rat = ''.join(div.find_element_by_class_name(self.rat_class).get_attribute('style').replace('width:', '').replace('%;', '').split())
                                    except:
                                        pass
                                    try:
                                        x = div.find_element_by_class_name(self.sales_class).text.split().index('продавец')
                                        sales = ' '.join(div.find_element_by_class_name(self.sales_class).text.split()[x + 1:])
                                    except:
                                        pass
                                    result.append({
                                        'name': name,
                                        'brand': brand,
                                        'review': review,
                                        'price': price,
                                        'rat': rat,
                                        'sales': sales
                                    })

                                else:
                                    pass
                        else:
                            flag = False
                else:
                    break
            driver.close()
            driver.quit()
            print(f'Закончили парсить {brand}')
        return result

    def save_result(self, result):
        workbook = xlsxwriter.Workbook(f'ozon {datetime.date.today()}.xlsx')
        worksheet = workbook.add_worksheet("skill")
        row = 1
        col = 0
        worksheet.write(0, 0, 'Бренд')
        worksheet.write(0, 1, 'Наименование')
        worksheet.write(0, 2, 'Отзывы')
        worksheet.write(0, 3, 'Цена')
        worksheet.write(0, 4, 'Рейтинг')
        worksheet.write(0, 5, 'Продавец')
        worksheet.write(0, 6, 'Дата')
        for item in result:
            worksheet.write(row, col, item['brand'])
            worksheet.write(row, col + 1, item['name'])
            worksheet.write(row, col + 2, int(item['review'][0]))
            worksheet.write(row, col + 3, int(item['price'][0]))
            worksheet.write(row, col + 4, float(item['rat'][0:5]))
            worksheet.write(row, col + 5, item['sales'])
            worksheet.write(row, col + 6, datetime.date.today())
            row += 1

        workbook.close()


class ParserVseinstrumenti(object):
    def __init__(self, url, pages):
        self.options = Options()
        self.options.headless = False
        self.url = url
        self.pages = pages

    def get_links_rasdel(self):
        links_rasdel = []
        driver = webdriver.Chrome(chrome_options=self.options)
        driver.get(self.url)
        rasdels = driver.find_elements_by_class_name('inner-wrapper')
        for rasdel_in in rasdels:
            rasdel_name = rasdel_in.find_element_by_class_name('title').text
            links_rasdel.append({
                rasdel_name: rasdel_in.find_element_by_tag_name('a').get_attribute('href')
            })
        return links_rasdel

    def get_links_groups(self, links_rasdel):
        links_groups = []
        for link in links_rasdel:
            rasdel = ' '.join(list(link))
            driver = webdriver.Chrome(chrome_options=self.options)
            driver.get(link[rasdel])
            if len(driver.find_elements_by_class_name('card-category')) > 0:
                groups = driver.find_elements_by_class_name('inner-wrapper')
                for link_group in groups:
                    group = link_group.find_element_by_class_name('title').text
                    links_groups.append({
                        'rasdel': rasdel,
                        group: link_group.find_element_by_tag_name('a').get_attribute('href')
                    })
            else:
                links_groups.append({
                    'rasdel': rasdel,
                    rasdel: link[rasdel]
                })
        return links_groups

    def get_content_from_groups(self, dict_group):
        list_sku = []
        name_rasdel = dict_group['rasdel']
        name_group = list(dict_group)[1]
        flag = True
        for page in range(1, self.pages):
            if flag:
                driver = webdriver.Chrome(chrome_options=self.options)
                driver.get(dict_group[name_group]) if page < 2 else driver.get(f'{dict_group[name_group]}page{page}')
                product_cards = driver.find_elements_by_class_name('product-row')
                if len(product_cards) > 0:
                    for product in product_cards:
                        try:
                            cheсk_not_element = product.find_element_by_class_name('-not-available').text
                            flag = False
                            driver.close()
                            driver.quit()
                            break
                        except:
                            rasdel = name_rasdel
                            group = name_group
                            name = product.find_element_by_class_name('title').text
                            try:
                                price = product.find_element_by_class_name('price').find_element_by_tag_name(
                                    'span').text
                            except:
                                price = 0
                            try:
                                rat = product.find_element_by_class_name('rating-count').text
                            except:
                                rat = ''
                            if len(name) > 1:
                                list_sku.append({
                                    'rasdel': rasdel,
                                    'group': group,
                                    'name': name,
                                    'price': price,
                                    'rat': rat,
                                })
                            else:
                                pass
                else:
                    flag = False
                    break
                    driver.close()
                    driver.quit()
            else:
                break
                driver.close()
                driver.quit()
        return list_sku


    def get_content_from_listing(self, dict_group):
        list_sku = []
        name_rasdel = dict_group['rasdel']
        name_group = ''.join(list(dict_group)[1])
        flag = True
        for page in range(1, self.pages):
            if flag:
                driver = webdriver.Chrome(chrome_options=self.options)
                driver.get(dict_group[name_group]) if page < 2 else driver.get(f'{dict_group[name_group]}page{page}')
                product_cards = driver.find_elements_by_class_name('product-tile')
                if len(product_cards) > 0:
                    for product in product_cards:
                        try:
                            cheсk_not_element = product.find_element_by_class_name('-not-available')
                            flag = False
                            driver.close()
                            driver.quit()
                            break
                        except:

                            rasdel = name_rasdel
                            group = name_group
                            name = product.find_element_by_class_name('title').find_element_by_tag_name(
                                'a').get_attribute('title')
                            try:
                                price = product.find_element_by_class_name('price').text
                            except:
                                price = 0
                            try:
                                rat = product.find_element_by_class_name('rating-count').text
                            except:
                                rat = ''
                            if len(name) > 1:
                                list_sku.append({
                                    'rasdel': rasdel,
                                    'group': group,
                                    'name': name,
                                    'price': price,
                                    'rat': rat,
                                })
                            else:
                                pass
                    else:
                        flag = False
                else:
                    break
                    driver.close()
                    driver.quit()
        return list_sku


    def get_content(self, list_groups):
        sku = []
        for dict_group in list_groups:
            name_rasdel = dict_group['rasdel']
            name_group = ''.join(list(dict_group)[1])
            if name_rasdel != name_group:
                list_sku = self.get_content_from_groups(dict_group)
            else:
                list_sku = self.get_content_from_listing(dict_group)
            sku.append(list_sku)
        return sku


    def save_result(self, result):
        workbook = xlsxwriter.Workbook(f'Vseinstrumenti {datetime.date.today()}.xlsx')
        worksheet = workbook.add_worksheet("skill")
        row = 1
        col = 0
        worksheet.write(0, 0, 'Раздел')
        worksheet.write(0, 1, 'Группа')
        worksheet.write(0, 2, 'Наименование')
        worksheet.write(0, 3, 'Рейтинг')
        worksheet.write(0, 4, 'Цена')
        worksheet.write(0, 5, 'Дата')
        for items in result:
            for item in items:
                worksheet.write(row, col, item['rasdel'])
                worksheet.write(row, col + 1, item['group'])
                worksheet.write(row, col + 2, item['name'])
                worksheet.write(row, col + 3, item['rat'])
                worksheet.write(row, col + 4, item['price'])
                worksheet.write(row, col + 5, datetime.date.today())
                row += 1

        workbook.close()


    def parser(self):
        list_rasdel = self.get_links_rasdel()
        list_groups = self.get_links_groups(list_rasdel)
        result = self.get_content(list_groups)
        self.save_result(result)
