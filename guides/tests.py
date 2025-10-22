import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.urls import reverse
from guides.models import GuideProfile, TourRequest, Tour, Earning
from accounts.models import User
from hotels.models import Notification

@pytest.fixture(scope="class")
def chrome_driver(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)
    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("chrome_driver")
class TestGuideBookingFlow:

    @pytest.mark.django_db
    def test_tourist_can_book_guide(self, live_server):

        tourist = User.objects.create_user(
            username="tourist1",
            email="tourist1@example.com",
            password="Testpass123",
            role="tourist"
        )

        guide_user = User.objects.create_user(
            username="guide1",
            email="guide1@example.com",
            password="Guidepass123",
            role="guide"
        )

        guide_profile = GuideProfile.objects.create(
            user=guide_user,
            phone="01712345678",
            bio="Experienced guide",
            experience_years=5,
            is_completed=True,
            is_verified=True
        )

        def login(username, password):
            self.driver.get(f"{live_server.url}{reverse('login')}")
            self.driver.find_element(By.NAME, "identifier").send_keys(username)
            self.driver.find_element(By.NAME, "password").send_keys(password)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(2)


        def book_guide(guide_id):
            self.driver.get(f"{live_server.url}{reverse('book_guide', args=[guide_id])}")
            # Fill booking form
            self.driver.find_element(By.NAME, "destination").clear()
            self.driver.find_element(By.NAME, "destination").send_keys("Sundarbans")
            self.driver.find_element(By.NAME, "date").send_keys("12-25-2025")
            self.driver.find_element(By.NAME, "number_of_travelers").clear()
            self.driver.find_element(By.NAME, "number_of_travelers").send_keys("2")
            self.driver.find_element(By.NAME, "duration_hours").send_keys("4")
            self.driver.find_element(By.NAME, "places_to_explore").send_keys("Mangrove Forest, Wildlife Spot")
            self.driver.find_element(By.NAME, "price").clear()
            self.driver.find_element(By.NAME, "price").send_keys("5000")
            self.driver.find_element(By.NAME, "notes").send_keys("Please arrange boat ride.")
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(2)

        def logout():
            self.driver.get(f"{live_server.url}{reverse('logout')}")
            time.sleep(1)

        login("tourist1", "Testpass123")

        self.driver.get(f"{live_server.url}{reverse('guide_list')}")
        time.sleep(1)

        self.driver.get(f"{live_server.url}{reverse('guide_detail', args=[guide_profile.id])}")
        time.sleep(1)

        book_guide(guide_profile.id)

        assert TourRequest.objects.filter(tourist=tourist, guide=guide_user).exists()

        notification_exists = Notification.objects.filter(user=guide_user).exists()
        assert notification_exists

        logout()

@pytest.mark.usefixtures("chrome_driver")
class TestGuideDashboardFlow:

    @pytest.mark.django_db
    def test_guide_accepts_tour_request_and_my_tours(self, live_server):

        tourist = User.objects.create_user(
            username="tourist1",
            email="tourist1@example.com",
            password="Tourist123",
            role="tourist"
        )

        guide_user = User.objects.create_user(
            username="guide1",
            email="guide1@example.com",
            password="Guide123",
            role="guide"
        )

        guide_profile = GuideProfile.objects.create(
            user=guide_user,
            phone="01712345678",
            bio="Experienced guide",
            experience_years=5,
            is_completed=True,
            is_verified=True
        )


        tour_request = TourRequest.objects.create(
            tourist=tourist,
            guide=guide_user,
            destination="Sundarbans",
            date="2025-12-25",
            number_of_travelers=2,
            duration_hours=4,
            places_to_explore="Mangrove Forest, Wildlife Spot",
            price=5000,
            notes="Please arrange boat ride."
        )

        def login(username, password):
            self.driver.get(f"{live_server.url}{reverse('login')}")
            self.driver.find_element(By.NAME, "identifier").send_keys(username)
            self.driver.find_element(By.NAME, "password").send_keys(password)
            self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(2)


        def logout():
            self.driver.get(f"{live_server.url}{reverse('logout')}")
            time.sleep(1)


        login("guide1", "Guide123")

        self.driver.get(f"{live_server.url}{reverse('tour_requests')}")
        time.sleep(1)

        accept_url = reverse('accept_request', args=[tour_request.id])
        self.driver.get(f"{live_server.url}{accept_url}")
        time.sleep(1)

        tour_request.refresh_from_db()
        assert tour_request.status == "accepted"


        tour = Tour.objects.filter(guide=guide_user, tourists=tourist, destination="Sundarbans").first()
        assert tour is not None

        self.driver.get(f"{live_server.url}{reverse('my_tours')}")
        time.sleep(1)

        page_source = self.driver.page_source
        assert "Sundarbans" in page_source

        logout()

