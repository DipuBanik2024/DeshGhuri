import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.urls import reverse
from destinations.models import Destination
from accounts.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture(scope="class")
def chrome_driver(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("chrome_driver")
class TestDestinationLive:

    @pytest.mark.django_db
    def test_tourist_browse_destinations(self, live_server):

        tourist = User.objects.create_user(
            username="tourist1",
            email="tourist1@example.com",
            password="Testpass123",
            role="tourist"
        )


        image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00'
            b'\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x0A\x00\x01\x00\x2C\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B'
        )
        dummy_image = SimpleUploadedFile("test.jpg", image_content, content_type="image/jpeg")

        dest = Destination.objects.create(
            name="Cox's Bazar",
            division="Chattogram",
            type="Natural",
            best_time="November to March",
            description="Famous for long sandy beaches.",
            main_image=dummy_image
        )


        def login_tourist(username, password):
            self.driver.get(f"{live_server.url}{reverse('login')}")
            self.driver.find_element(By.NAME, "identifier").send_keys(username)
            self.driver.find_element(By.NAME, "password").send_keys(password)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(1)


        def logout_tourist():
            self.driver.get(f"{live_server.url}{reverse('logout')}")
            time.sleep(1)


        login_tourist("tourist1", "Testpass123")


        self.driver.get(f"{live_server.url}{reverse('destination_list')}")
        time.sleep(1)
        page_text = self.driver.page_source
        assert "Cox's Bazar" in page_text, "Destination not found in list page"


        self.driver.get(f"{live_server.url}{reverse('destination_detail', args=[dest.id])}")
        time.sleep(1)
        page_text = self.driver.page_source
        assert "Cox's Bazar" in page_text, "Destination detail not showing correctly"

        logout_tourist()
