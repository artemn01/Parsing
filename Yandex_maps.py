from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from parsing.temp import gamma_delay, get_urls
import asyncio
import curl_cffi
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup
import pandas
import numpy as np
import random
from random import uniform
from time import sleep
from IPython.display import clear_output

def get_urls():
    with SB(uc=True, block_images=True, disable_csp=True, do_not_track=True, page_load_strategy='eager', guest_mode=True, undetectable=True) as sb:
        sb.uc_open_with_reconnect('https://yandex.ru/maps/?display-text=%D0%93%D0%B4%D0%B5%20%D0%BF%D0%BE%D0%B5%D1%81%D1%82%D1%8C&ll=50.569114%2C53.231253&mode=search&sctx=ZAAAAAgBEAAaKAoSCbjqOlRTYElAEXJr0m2JsEpAEhIJibX4FADDDkARbXL4pBPJ9D8iBgABAgMEBSgKOABAKEgBYjNwcmljZXNfc25pcHBldHNfcmFua2luZ19tb2RlbD1tb2RlbF8yMDI1MTIwOF8xMzM5NTliLnByaWNlc19zbmlwcGV0c19yYW5raW5nX21vZGVsX3RocmVzaG9sZD0wLjYzNjJiOnJlYXJyPXNjaGVtZV9Mb2NhbC9HZW8vU3VidGl0bGVzL1VzZVBpbkdvb2RzUHJpY2VGb3JtdWxhPTFqAnJ1nQHNzMw9oAEAqAEAvQFwh4NswgGTAaPXmun5At%2F9jJqDBZPs97jdA5K3kbrgBKWszq2cBc%2Fel7O2AZeni5OjAcX795yoBLXvrpjnA63mhaoGifKR%2BJkBzf2Qgf8CurXtmecEgP3yjJUD2anuiJgDiv3iga8G1a%2BLx0O39I24iQSRjcLRBouC67PABcCPopGaBZrhgf3eBOv1%2FOe4A%2BCZs7fRBuPw1YOBBoICE9CT0LTQtSDQv9C%2B0LXRgdGC0YyKAlwxODQxMDYzOTAkMTg0MTA2Mzg2JDE4NDEwNjM5NiQxODQxMDYzOTIkMTg0MTA2Mzg0JDE4NDEwNjM5NCQzNTE5MzExNDkzNyQxMzg3Nzg4OTk2JDc3MDkzMTUzN5ICAJoCDGRlc2t0b3AtbWFwc6oCtgIxMDA1MjUyOTQyMDEsMTkwMzUxODU0NDczLDYwMDMyMDYsMjMxMTE5MDk0OTcxLDQ2OTQ2NDk4OTg5LDI4NTg1OTM2OTksMTU2MzQ3MTI5NTQsMTU1OTQ3NDc5MDMsMTIwNjMzNTk2MTMsNjAwMzA0MSwxNjYwNjg1OTcwNjgsNDE1NDYwNzc2NDIsMzA5MjU4MzQ4NiwxOTM5NTM1MTc5MTAsMzkyMDYzNjQwMzcsMTk3NDQ2NTI5MTk0LDEyNzk2MDQzNDg2MiwxMzI1MzQ4Njg1OTMsOTA2NTc1NDk2MjcsMTM0NjUxNTYzMDU0LDk4MTAwNjg3OTQ1LDIzNjAyNTQzNjQ2Miw1MjUxNDMyMTI1LDIwNjY0NjU0NzE0NSwxNTgwMDgxNzU2MSwyMTg1NTA5Mjc02gIoChIJHksfuqBESUARhdw%2BdazISkASEgmAtfgUAMMOQBFgmUJKYLH0P%2BACAQ%3D%3D&sll=50.569114%2C53.231253&sspn=3.845215%2C1.303621&text=%D0%93%D0%B4%D0%B5%20%D0%BF%D0%BE%D0%B5%D1%81%D1%82%D1%8C&z=9')
        print('Загрузка сайта...')
        sb.sleep(1.5)
        try:
            sb.uc_gui_handle_captcha()
        except:
            print('Капчи нет')
            pass
        
        browser : WebDriver = sb.driver

        wait = WebDriverWait(browser, 10)

        elements = browser.execute_script("return document.querySelectorAll('li.search-snippet-view');")

        href_set = set()
        last_len = 0
        new_data_count = 0

        print('Начинаю прокрутку страницы...')

        while len(elements) < 500:
            clear_output(wait=True)
            elements1 = len(elements)
            elements = browser.execute_script("return document.querySelectorAll('li.search-snippet-view');")
            browser.execute_script('arguments[0].scrollIntoView(true);', elements[-1])
            elements = browser.execute_script("return document.querySelectorAll('li.search-snippet-view');")
            elements2 = len(elements)
            sleep(uniform(0.1, 0.3))
            print(f'Количество - {len(elements)}', end=' ')

            if elements1 == elements2:
                n += 1
                print(f'n = {n}', end=' ')
                if n >= 200:
                    break
            
            else:
                n = 0
            
        script = """return Array.from(document.querySelectorAll('.search-snippet-view__body-button-wrapper span[data-nosnippet="true"] a.link-overlay')).map(a => a.href);"""
        all_hrefs = browser.execute_script(script)
        href_list = list(set(all_hrefs))

        
        return href_list


async def fetch(session, link):
    print(f'Обработка: {link}')
    try:
        responce = await session.get(link, impersonate='chrome110')
        await asyncio.sleep(uniform(0.5, 0.8))
        soup = BeautifulSoup(responce.text, 'lxml')
        element_data = {
            'Ссылка': link,
            'Название': 'null',
            'Адрес': 'null',
            'Телефон': 'телефон не указан',
            'Рейтинг': 'null'
        }

        try:
            name = soup.find('h1', class_='orgpage-header-view__header').text
            element_data['Название'] = name
        except:
            pass
        
        try:
            adress = soup.find('a', class_='business-contacts-view__address-link').text
            element_data['Адрес'] = adress
        except:
            pass

        try:
            phone = soup.find('div', class_='card-phones-view__number').find('span').text
            element_data['Телефон'] = phone
        except:
            try:
                phone = soup.find(attrs={'itemprop': 'telephone'}).text
                element_data['Телефон'] = phone
            except:
                try:
                    phone = soup.find('a', class_='card-phones-view__phone-number-link').text
                    element_data['Телефон'] = phone
                except:
                    pass

        try:
            rating = soup.find('div', class_='business-rating-badge-view__rating').find('span', class_='business-rating-badge-view__rating-text').text
            element_data['Рейтинг'] = rating
        except:
            pass
            
        return element_data

    except Exception as e:
        print(f"Ошибка при обработке {link}: {e}")
        return None


async def main():

    href_list = get_urls()

    all_data = []

    semaphore = asyncio.Semaphore(10)

    async with AsyncSession() as session:

        async def sem(link):
            async with semaphore:
                return await fetch(session, link)

        tasks = [sem(link) for link in href_list]

        result = await asyncio.gather(*tasks)

        all_data = [data for data in result if data is not None]
    
    df = pandas.DataFrame(all_data)
    df.to_excel('async_data.xlsx')
    print('Завершено!')

if __name__ == '__main__':
    asyncio.run(main())