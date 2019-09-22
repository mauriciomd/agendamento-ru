import sys
import os
import datetime
import time
from selenium import webdriver
from selenium.webdriver.support import select
from selenium.webdriver.chrome.options import Options


def find_login_input(page):
    btn = page.find_element_by_name('enter')
    login = page.find_element_by_id('login')
    password = page.find_element_by_id('senha')

    return login, password, btn


def find_booking_meal_link(page):
    links = page.find_elements_by_css_selector('a')

    for link in links:
        if link.get_attribute('href').find('agendamento/form.html') != -1:
            return link.get_attribute('href')

    return None


def find_lunch_input(page):
    btn = page.find_element_by_id('btnSubmit')
    begin = page.find_element_by_id('periodo_inicio')
    end = page.find_element_by_id('periodo_fim')
    restaurant = select.Select(page.find_element_by_id('restaurante'))
    lunch = page.find_element_by_id('tiposRefeicao_1')

    return btn, begin, end, restaurant, lunch


def get_next_monday():
    MONDAY = 7
    today = datetime.date.today()
    delta = MONDAY - today.weekday()
    next_monday = today + datetime.timedelta(days=delta)

    return next_monday.strftime('%d/%m/%Y')


def get_next_friday():
    FRIDAY = 11
    today = datetime.date.today()

    delta = FRIDAY - today.weekday()
    next_monday = today + datetime.timedelta(days=delta)

    return next_monday.strftime('%d/%m/%Y')


def get_browser_headless():
    options = Options()
    options.add_argument("--headless")

    return webdriver.Chrome(options=options)


def ru_booking(enrollment, password):
    browser = get_browser_headless()
    browser.get('https://portal.ufsm.br/ru/')

    try:
        enrollment_input, password_input, btn_login = find_login_input(browser)

        enrollment_input.send_keys(enrollment)
        password_input.send_keys(password)
        btn_login.click()

        booking_link = find_booking_meal_link(browser)
        browser.get(booking_link)
        reserve_btn, begin, end, restaurant, lunch = find_lunch_input(browser)

        begin.send_keys(get_next_monday())
        end.send_keys(get_next_friday())
        restaurant.select_by_value('41')
        lunch.click()
        reserve_btn.click()

        browser.close()
        return True

    except:
        return False


if __name__ == '__main__':
    enrollment = os.environ.get('RU_ENROLLMENT')
    password = os.environ.get('RU_PASSWORD')

    if enrollment == None and password == None:
        if len(sys.argv) < 3:
            print('Execution: python3 booking.py <matricula> <senha>')
            exit(1)
        else:
            enrollment = sys.argv[1]
            password = sys.argv[2]

    successed = ru_booking(enrollment, password)
    if not successed:
        print('Fail to book RU :(')
