import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from packages.models import Package, Booking, Review
from accounts.models import User

@pytest.fixture(scope="class")
def chrome_driver(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("chrome_driver")
class TestPackageFlow:

    @pytest.mark.django_db
    def test_tourist_package_flow(self, live_server):

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
        dummy_image = SimpleUploadedFile("dummy.jpg", image_content, content_type="image/jpeg")

        package = Package.objects.create(
            destination_name="Cox's Bazar",
            image=dummy_image,
            people_limit=5,
            price=10000,
            days=3,
            description="Test tour package",
            itinerary="Day1: Beach, Day2: Market",
            included_services="Transport, Hotel",
            exclusions="Flight"
        )

        def login(username, password):
            self.driver.get(f"{live_server.url}{reverse('login')}")
            self.driver.find_element(By.NAME, "identifier").send_keys(username)
            self.driver.find_element(By.NAME, "password").send_keys(password)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(2)

        def book_package(package_id):
            self.driver.get(f"{live_server.url}{reverse('book_package', args=[package_id])}")
            # Fill booking form
            self.driver.find_element(By.NAME, "people_count").clear()
            self.driver.find_element(By.NAME, "people_count").send_keys("2")
            self.driver.find_element(By.NAME, "tour_date").send_keys("12-25-2025")
            self.driver.find_element(By.NAME, "mobile_number").send_keys("01712345678")
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(2)

        def logout():
            self.driver.get(f"{live_server.url}{reverse('logout')}")
            time.sleep(1)

        login("tourist1", "Testpass123")
        self.driver.get(f"{live_server.url}{reverse('package_list')}")
        time.sleep(1)


        self.driver.get(f"{live_server.url}{reverse('package_detail', args=[package.id])}")
        time.sleep(1)

        book_package(package.id)

        assert Booking.objects.filter(tourist=tourist, package=package).exists()


        logout()
