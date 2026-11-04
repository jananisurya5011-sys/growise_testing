from tests.selenium.pages.base_page import BaseWebPage

class SplashLoginPage(BaseWebPage):
    EMAIL_INPUT = "input[type='email']"
    PASSWORD_INPUT = "input[type='password']"
    LOGIN_BTN = "button[type='submit']"
    SIGNUP_LINK = "a[href='/signup']"
    ROLE_SELECT = "select[name='role']"

    def open_splash(self):
        return self.navigate("/")

    def open_login(self):
        return self.navigate("/login")

    def open_signup(self):
        return self.navigate("/signup")

    def login(self, email, password, role="farmer"):
        self.open_login()
        self.enter_text("css", self.EMAIL_INPUT, email)
        self.enter_text("css", self.PASSWORD_INPUT, password)
        self.click("css", self.LOGIN_BTN)
        return True


class FarmerWebPage(BaseWebPage):
    DIAGNOSE_NAV = "a[href='/farmer/ai-diagnose']"
    INVENTORY_NAV = "a[href='/farmer/inventory']"
    RENTAL_NAV = "a[href='/farmer/rental']"
    CULTIVATION_NAV = "a[href='/farmer/cultivation']"
    POOL_NAV = "a[href='/farmer/crop-pool']"
    WEATHER_NAV = "a[href='/farmer/weather']"

    def open_farmer_home(self):
        return self.navigate("/home/farmer")

    def open_ai_diagnose(self):
        return self.navigate("/farmer/ai-diagnose")

    def open_inventory(self):
        return self.navigate("/farmer/inventory")

    def open_rental(self):
        return self.navigate("/farmer/rental")

    def open_crop_pool(self):
        return self.navigate("/farmer/crop-pool")


class DriverWebPage(BaseWebPage):
    ACTIVE_TRIP_NAV = "a[href='/driver/status']"
    WALLET_NAV = "a[href='/driver/wallet']"
    DELIVERY_NAV = "a[href='/driver/standard-delivery']"

    def open_driver_home(self):
        return self.navigate("/home/driver")

    def open_wallet(self):
        return self.navigate("/driver/wallet")

    def open_active_trip(self):
        return self.navigate("/driver/status")


class UserWebPage(BaseWebPage):
    SEARCH_INPUT = "input[placeholder*='Search']"
    PRODUCT_CARD = ".product-card"
    CART_BTN = "button.cart-btn"
    CHECKOUT_BTN = "button.checkout-btn"

    def open_marketplace(self):
        return self.navigate("/user/shop")

    def open_deals(self):
        return self.navigate("/deals")

    def open_tracking(self, order_id=None):
        if order_id:
            return self.navigate(f"/track/{order_id}")
        return self.navigate("/track")


class AdminWebPage(BaseWebPage):
    VERIFY_NAV = "a[href='/admin/verify']"
    LIST_FARMERS = "a[href='/admin/list/farmer']"
    LIST_DRIVERS = "a[href='/admin/list/driver']"

    def open_admin_dashboard(self):
        return self.navigate("/home/admin")

    def open_driver_verification(self):
        return self.navigate("/admin/verify")

