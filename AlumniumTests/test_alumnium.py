import pytest
from selenium.webdriver import Chrome
from alumnium import Alumni
from dotenv import load_dotenv
load_dotenv()


@pytest.fixture(scope="function")
def alumni_session():
    """ Provides a Selenium Chrome driver and an Alumni object for each test function """
    driver = None
    al = None
    try:
        driver = Chrome()
        driver.get("https://todomvc.com/examples/vue/dist/#/")
        al = Alumni(driver)
        yield al
    finally:
        if driver:
            driver.quit()


def test_01(alumni_session: Alumni):
    al = alumni_session
    al.do("Add a task: 'Develop Alumnium test frameework'")
    al.do("Add a task: 'Do 10 pushups'")
    al.do("mark all tasks complete using 'Toggle All' button")
    al.check("task 'Develop Alumnium test frameework' is completed")
