from selenium import webdriver
from testcases.login_page import LoginPage

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.root_uri = "https://192.168.15.112:9090"
    login_page = LoginPage(driver)
    login_page.get("/")
    
    assert login_page.login_btn.text == "Log In"

    driver.close()