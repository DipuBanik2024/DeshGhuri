import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.urls import reverse
from hotels.models import Hotel, HotelBooking, Notification, RoomType
from accounts.models import User
from tourists.models import Tourist

@pytest.fixture(scope="class")
def chrome_driver(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("chrome_driver")
class TestHotelBookingFlow:


    @pytest.mark.django_db
    def test_tourist_can_book_hotel(self, live_server):

        tourist_user = User.objects.create_user(
            username="tourist1",
            email="tourist1@example.com",
            password="Testpass123",
            role="tourist"
        )

        hotel_manager = User.objects.create_user(
            username="manager1",
            email="manager1@example.com",
            password="Manager123",
            role="hotel_manager"
        )


        Tourist.objects.create(
            user=tourist_user,
            phone_number="01712345678"
        )

        hotel = Hotel.objects.create(
            owner=hotel_manager,
            name="Sea Breeze Hotel",
            address="Cox's Bazar",
            phone="01712345678",
            description="A nice hotel near the beach",
            city="Cox's Bazar",
            area="Kolatoli",
            min_price=2000,
            max_price=4000
        )

        room_type = RoomType.objects.create(
            hotel=hotel,
            name="Deluxe Room",
            capacity=2,
            price_per_night=2500,
            available_rooms=5,
            has_ac=True
        )

        # --- Helper functions ---
        def login(username, password):
            self.driver.get(f"{live_server.url}{reverse('login')}")
            self.driver.find_element(By.NAME, "identifier").send_keys(username)
            self.driver.find_element(By.NAME, "password").send_keys(password)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(2)

        def logout():
            self.driver.get(f"{live_server.url}{reverse('logout')}")
            time.sleep(1)

        def book_hotel(hotel_id, room_type_id):

            self.driver.get(f"{live_server.url}{reverse('book_hotel', args=[hotel_id, room_type_id])}")

            self.driver.find_element(By.NAME, "check_in").send_keys("12/25/2025")
            self.driver.find_element(By.NAME, "check_out").send_keys("12/28/2025")
            self.driver.find_element(By.NAME, "number_of_rooms").clear()
            self.driver.find_element(By.NAME, "number_of_rooms").send_keys("1")
            self.driver.find_element(By.NAME, "total_guests").clear()
            self.driver.find_element(By.NAME, "total_guests").send_keys("2")
            self.driver.find_element(By.NAME, "guest_name").send_keys("John Doe")
            self.driver.find_element(By.NAME, "guest_email").send_keys("")
            self.driver.find_element(By.NAME, "guest_phone").send_keys("01712345678")
            self.driver.find_element(By.NAME, "special_requests").send_keys("Need sea view room")
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(2)


        login("tourist1", "Testpass123")

        self.driver.get(f"{live_server.url}{reverse('hotels_info')}")
        time.sleep(1)
        assert "Sea Breeze Hotel" in self.driver.page_source, "Hotel not listed on page"

        self.driver.get(f"{live_server.url}{reverse('hotel_detail', args=[hotel.id])}")
        time.sleep(1)
        book_hotel(hotel.id, room_type.id)

        logout()
