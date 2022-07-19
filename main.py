# pip install beautifulsoup4 lxml requests wheel selenium
import os
import time
import os, glob
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from site_token import my_email, my_password


def get_game_data(url: str):

    service = Service(executable_path="chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get(url=url)
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@data-key='email']").send_keys(my_email)
    driver.find_element(By.XPATH, "//input[@data-key='password']").send_keys(my_password)
    driver.find_element(By.XPATH, "//button['Sign In']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//input[@placeholder='Pin code']").click()
    time.sleep(10)

    driver.find_element(By.XPATH, "//div[@class='product-icon icon-p-id-3']").click()
    time.sleep(15)

    # print(f"[INFO] Страница: {driver.window_handles}")
    # driver.switch_to.window(driver.window_handles[0])
    # print('[INFO] Закрываем страницу:', driver.title)
    # driver.close()
    # time.sleep(10)
    driver.switch_to.window(driver.window_handles[1])
    print('[INFO] Переходим на страницу:', driver.title)
    time.sleep(10)
    print('[INFO] Ждем полную загрузку страницы:', driver.title)
    time.sleep(10)
    driver.find_element(By.XPATH, "//i[@class='ico-cms']").click()
    time.sleep(5)
    driver.get('https://cmsbetconstruct.com/#/casinoGames/all')
    # print(f"[INFO] Страница: {driver.window_handles}")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    print('[INFO] Переходим на страницу:', driver.title)
    time.sleep(10)

    game_nums = driver.find_elements(By.XPATH, "//strong[@ng-show='pagination.totalItems']")
    games_count = game_nums[0].text.split()[-1]
    games_count = int(games_count)
    print(f"[INFO] Общее количество игр: {games_count}")

    game_last_num = game_nums[0].text.split()[3]
    game_last_num = int(game_last_num)
    print(f"[INFO] Последний номер игры на странице: {game_last_num}")

    pages_count = int(games_count) // 25
    print(f"[INFO] Количество страниц: {pages_count+1}")

    # date = datetime.now().strftime("%d-%m-%Y")

    for file in glob.glob("html_data/*.html"):
        os.remove(file)
        print("Deleted " + str(file))

    try:
        for i in range(pages_count + 1):
            cms_page = driver.title
            time.sleep(2)

            cms_page = cms_page.replace(" ", "_").strip()
            print(f"[INFO] Сохраняем страницу: {cms_page}_{i+1}")
            time.sleep(3)

            with open(f"html_data/{cms_page}_{i+1}.html", "w", encoding="utf8") as file:
                file.write(driver.page_source)

            driver.find_element(By.XPATH, "//li[@ng-class='{disabled: noNext()||ngDisabled}']").click()
            time.sleep(1)
    except Exception:
        print("[END] Все страницы обработаны")

    finally:
        driver.close()
        driver.quit()
        print('[INFO] Закрываем браузер')
        time.sleep(1)
        print('[INFO] Выходим из программы')
        time.sleep(1)
        exit()


def main():
    sign_in_url = 'https://www.accounts-bc.com/signin'
    get_game_data(sign_in_url)


if __name__ == '__main__':
    main()
    print('[INFO] Программа завершена!')
