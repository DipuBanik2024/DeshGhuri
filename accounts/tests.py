import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.urls import reverse
from accounts.models import User


@pytest.fixture(scope="class")
def chrome_driver(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("chrome_driver")
@pytest.mark.django_db
class TestUserAuth:

    def signup_user(self, username, email, password, role, live_server):
        self.driver.get(f"{live_server.url}{reverse('signup')}")
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "first_name").send_keys("Test")
        self.driver.find_element(By.NAME, "last_name").send_keys("User")
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "role").send_keys(role)
        self.driver.find_element(By.NAME, "password1").send_keys(password)
        self.driver.find_element(By.NAME, "password2").send_keys(password)
        self.driver.find_element(By.NAME, "agree_terms").click()
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(1)  # wait for redirect

    def login_user(self, identifier, password, live_server):
        self.driver.get(f"{live_server.url}{reverse('login')}")
        self.driver.find_element(By.NAME, "identifier").send_keys(identifier)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(1)

    def logout_user(self, live_server):
        self.driver.get(f"{live_server.url}{reverse('logout')}")
        time.sleep(1)


    def test_tourist_signup_login_logout(self, live_server):
        username = "tourist1"
        email = "tourist1@example.com"
        password = "Testpass123"
        role = "tourist"

        self.signup_user(username, email, password, role, live_server)
        assert User.objects.filter(username=username).exists()

        self.logout_user(live_server)
        self.login_user(username, password, live_server)
        assert "/home/" in self.driver.current_url
        self.logout_user(live_server)


    def test_guide_signup_login_logout(self, live_server):
        username = "guide1"
        email = "guide1@example.com"
        password = "Testpass123"
        role = "guide"

        self.signup_user(username, email, password, role, live_server)
        assert User.objects.filter(username=username).exists()

        self.logout_user(live_server)
        self.login_user(email, password, live_server)  # login by email
        assert "/dashboard/" in self.driver.current_url
        self.logout_user(live_server)


    def test_hotel_manager_signup_login_logout(self, live_server):
        username = "manager1"
        email = "manager1@example.com"
        password = "Testpass123"
        role = "hotel_manager"

        self.signup_user(username, email, password, role, live_server)
        assert User.objects.filter(username=username).exists()

        self.logout_user(live_server)
        self.login_user(username, password, live_server)
        assert "/dashboard/" in self.driver.current_url
        self.logout_user(live_server)
