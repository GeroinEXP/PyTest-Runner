from argparse import Action
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.keys import Keys

@pytest.fixture(scope="module")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome()
    driver.get("https://demoqa.com/buttons")
    yield driver
    time.sleep(10)
    driver.quit()
    
def wait_for_page_load_and_refresh(browser, url, element_locator, timeout=1, max_retries=3):
    browser.get(url)
    
    for _ in range(max_retries):
        try:
            WebDriverWait(browser, timeout).until(
                EC.presence_of_element_located(element_locator)
            )
            print(f"Страница {url} успешно загружена.")
            return True
        except TimeoutException:
            print(f"Не удалось загрузить страницу {url}. Пробуем обновить...")
            browser.refresh()
    
    print(f"Не удалось загрузить страницу {url} после {max_retries} попыток.")
    return False

def test_example(browser):
        wait = WebDriverWait(browser, 5) 
        actions = ActionChains(browser)
        
        #Клик по кнопке   
        buttons = browser.find_elements(By.CSS_SELECTOR, "button")
        exact_button = next((b for b in buttons if b.text.strip() == "Click Me"), None)
        exact_button.click()
        
        #Проверка на выполнение обычного клика
        wait.until(EC.presence_of_element_located((By.ID, "dynamicClickMessage")))
        print("Обычный клик выполнен")

        #Двойной клик
        double_click_button = wait.until(EC.element_to_be_clickable((By.ID, "doubleClickBtn")))
        actions.double_click(double_click_button).perform()
        
        #Проверка на выполнение двойного клика
        wait.until(EC.presence_of_element_located((By.ID, "doubleClickMessage")))
        print("Двойной клик выполнен")
        
        #Клик правой кнопки мыши
        right_click_button = wait.until(EC.element_to_be_clickable((By.ID, "rightClickBtn")))
        actions.context_click(right_click_button).perform()
        
        #Проверка на выполнение клика правой кнопки мыши
        wait.until(EC.presence_of_element_located((By.ID, "rightClickMessage")))
        print("Клик правой кнопки мыши выполнен")
        
def test_second_example(browser):
        wait = WebDriverWait(browser, 5) 
        url = "https://demoqa.com/links"
        element_locator = (By.ID, "created")
        
        #Переход на страницу со ссылками   
        if wait_for_page_load_and_refresh(browser, url, element_locator):
            try:
        
                #Проверка наличия ссылки
                wait.until(EC.presence_of_element_located((By.ID, "created")))
                print("Ссылка присутствует")
        
                #Клик по ссылке
                created_link = wait.until(EC.element_to_be_clickable((By.ID, "created")))
                created_link.click()
        
                #Проверка на выполнение клика по ссылке
                wait.until(EC.presence_of_element_located((By.ID, "linkResponse")))
                print("Клик по ссылке выполнен")
            except TimeoutException as e:
                pytest.fail(f"Тест не прошел: {str(e)}")
        else:
            pytest.fail("Не удалось загрузить страницу с ссылками")
            
def test_radio_example(browser):
        wait = WebDriverWait(browser, 5)
        url = "https://demoqa.com/radio-button"
        element_locator = (By.ID, "yesRadio")
        
        #Переход на страницу с Radio Button
        if wait_for_page_load_and_refresh(browser, url, element_locator):
            try:
                #Клик по кнопке
                radio_button = wait.until(EC.presence_of_element_located((By.ID, "yesRadio")))
                browser.execute_script("arguments[0].click();", radio_button)
                
                #Проверка на выполнение клика по кнопке
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "text-success")))
                print("Клик по кнопке выполнен")
            except TimeoutException as e:
                pytest.fail(f"Тест не прошел: {str(e)}")
        else:
            pytest.fail("Не удалось загрузить страницу с Radio Button")
        
# def test_3_example(browser):
#         wait = WebDriverWait(browser, 5) 
        
#         #Переход на страницу с Radio Button
#         browser.get("https://demoqa.com/radio-button")
        
#         #Клик по кнопке
#         radio_button = wait.until(EC.presence_of_element_located((By.ID, "yesRadio")))
#         browser.execute_script("arguments[0].click();", radio_button)
        
#         wait.until(EC.presence_of_element_located((By.CLASS_NAME, "text-success")))
#         print("Выбор Radio Button выполнен")
        
        print(browser.page_source)
        browser.save_screenshot("before_radio_click.png")
        
        #Сохранение скриншота
        browser.save_screenshot("after_click.png")
        
        
if __name__ == "__main__":
    pytest.main(["-v"])