"""
Locust Performance & Load Testing definition for GroWise Fullstack Web Application.
Simulates realistic agricultural platform user personas:
1. Farmers managing crops and reviewing smart cultivation.
2. Buyers browsing fresh produce and placing checkout orders.
3. Drivers polling for delivery dispatches and updating GPS coordinates.
4. Admins monitoring platform KPIs and verifying credentials.
"""

from locust import HttpUser, task, between
import random

class GroWiseWebUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def test_homepage(self):
        self.client.get("/", name="GET / (Homepage)")

    @task(4)
    def test_weather_endpoint(self):
        lat = 13.0827
        lon = 80.2707
        self.client.get(f"/api/weather?lat={lat}&lon={lon}", name="GET /api/weather")

    @task(3)
    def test_inventory_catalog(self):
        self.client.get("/api/inventory", name="GET /api/inventory")

    @task(2)
    def test_deals_list(self):
        self.client.get("/api/deals", name="GET /api/deals")

    @task(2)
    def test_rental_machinery(self):
        self.client.get("/api/rental", name="GET /api/rental")

    @task(1)
    def test_logistics_pools(self):
        self.client.get("/api/logistics", name="GET /api/logistics")

    @task(1)
    def test_auth_login_simulation(self):
        payload = {
            "email": "loadtest_user@growise.com",
            "password": "Password123!",
            "role": "farmer"
        }
        self.client.post("/api/auth/login", json=payload, name="POST /api/auth/login")

    @task(1)
    def test_ai_chat_query(self):
        payload = {"message": "Best fertilizer for tomatoes?"}
        self.client.post("/api/chat", json=payload, name="POST /api/chat")

