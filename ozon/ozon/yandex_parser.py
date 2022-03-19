import random
import time

import xlsxwriter
from selenium import webdriver


def main():
    driver = webdriver.Chrome()
    list_links = {
        'Бензопила Hammer BPL3814C 1,47кВт/2лс 38см3 шина 14" цепь 3/8"-1,3мм-52 5кг': 'https://market.yandex.ru/product--benzinovaia-pila-hammer-bpl3814c-1470-vt-2-l-s/417636040?text=B5%20%D0%91%D0%B5%D0%BD%D0%B7%D0%BE%D0%BF%D0%B8%D0%BB%D0%B0%20Hammer%20BPL3814C%201%2C47%D0%BA%D0%92%D1%82%2F2%D0%BB%D1%81%2038%D1%81%D0%BC3%20%D1%88%D0%B8%D0%BD%D0%B0%2014%22%20%D1%86%D0%B5%D0%BF%D1%8C%203%2F8%22-1%2C3%D0%BC%D0%BC-52%205%D0%BA%D0%B3&cpc=xbzjHyjB6O46mM-_MxQutwWQTUmZ8mPaz04SG-n6zqgLB7E4IJ5_5YbZActBBRbrnwZzGCWzlKvoGOEfdBgBjhbZFfwPkdRvzSSG69K2o9KI7C-IjiTsi2Lck28q-Uz6DvYnF2NV3KdCkGHxy54yWU2gBQjgV-WldNWpnTTWJSInLKKHnl1a0A%2C%2C&sku=417636040&do-waremd5=cz-5AeSlGtN07ZvfRnFJQA&cpa=1&nid=71579',
        'Вибратор глубинный Hammer Flex VBR1100 1100Вт 4000об/мин + вал 1 метр': 'https://market.yandex.ru/product--elektricheskii-glubinnyi-vibrator-hammerflex-vbr1100/639927121?text=%D0%92%D0%B8%D0%B1%D1%80%D0%B0%D1%82%D0%BE%D1%80%20%D0%B3%D0%BB%D1%83%D0%B1%D0%B8%D0%BD%D0%BD%D1%8B%D0%B9%20Hammer%20Flex%20VBR1100%201100%D0%92%D1%82%204000%D0%BE%D0%B1%2F%D0%BC%D0%B8%D0%BD%20%2B%20%D0%B2%D0%B0%D0%BB%201%20%D0%BC%D0%B5%D1%82%D1%80&cpc=s6aLnH8Itn5Jy8VunpQ_if-t8EDK7QCDUJXiAPmJYGiI28g46uYfI1v69drJCk-tnNQm6K7ht5R4su2wpGSPhQhpAlBXt7u1UPVHI3F1dcwPN6GJiXyBW8bFCByacmYw4xN7TH8YgdbJxbgeCTS1rtaL1Qk33QB7d4NeyKIgslnBh1-_oYCQyQLHHj6mP2Op&sku=639927121&do-waremd5=Rkegj9jFP407nC_8G0tcVQ&cpa=1&nid=55599',
        'Бензоэлектростанция Hammer Flex GN6000T 5.5КВт 220В 50Гц бак 30л непр.9ч': 'https://market.yandex.ru/product--benzinovyi-generator-hammer-gn6000t-5500-vt/159400059?nid=56410&show-uid=16470011917684085067916001&context=search&glfilter=7893318%3A1581410&text=%D0%91%D0%B5%D0%BD%D0%B7%D0%BE%D1%8D%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D1%8F%20Hammer%20Flex%20GN6000T%205.5%D0%9A%D0%92%D1%82%20220%D0%92%2050%D0%93%D1%86%20%D0%B1%D0%B0%D0%BA%2030%D0%BB%20%D0%BD%D0%B5%D0%BF%D1%80.9%D1%87&sku=159400059&cpc=04btjgeIIMZ11ffqOYYQggd9DKoG_k9ZcVASZ_rAdwiZmtwrnoMXi-oRviHDoMN_ktvMFLB8uWslh5PqpRqqT6mJpgkIFyFm-6LGcuZ6XdDDkEPjE8aJwypmL1G5-OAJeab43RX8sIPzMRFn378sGQTHvlLf1iUGx3ajIHOFqkcZAySgup5OkA%2C%2C&do-waremd5=EDXu7D2lcvFh878i09A6sg',
    }
    result = []

    for key, val in list_links.items():
        driver.get(f'{val}')
        divs = driver.find_elements_by_class_name('zsSJk')
        for div in divs:
            time.sleep(random.randrange(1, 3))
            if 'предлож' in div.text:
                div.click()
                sku = driver.find_elements_by_class_name('ihl0O')
                sales = driver.find_elements_by_class_name('Vu-M2')
                price = driver.find_elements_by_class_name('_3NaXx')
                if price == '':
                    price = driver.find_elements_by_class_name('_1YKgk')
                for i in range(len(sales)):
                    print(price[i].text)
                    result.append(
                        {
                            'name': sku[i].text,
                            'sales': sales[i].text,
                            'price': price[i + 1].text.replace(' ₽', '')
                        })
                time.sleep(random.randrange(1, 10))
            else:
                pass
    driver.close()
    driver.quit()
    print(result)
    workbook = xlsxwriter.Workbook('yandex.xlsx')
    worksheet = workbook.add_worksheet("skill")
    row = 1
    col = 0
    worksheet.write(0, 0, 'Наименование')
    worksheet.write(0, 1, 'Продавец')
    worksheet.write(0, 2, 'Цена')

    for item in result:
        worksheet.write(row, col , item['name'])
        worksheet.write(row, col + 1, item['sales'])
        worksheet.write(row, col + 2, item['price'])
        row += 1

    workbook.close()


if __name__ == '__main__':
    try:
        main()
    except:
        main()
