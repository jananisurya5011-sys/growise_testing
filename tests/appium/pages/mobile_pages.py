from tests.appium.pages.base_page import BasePage

class SplashPage(BasePage):
    LOGO = "app_logo"
    GET_STARTED_BTN = "btn_get_started"
    TAGLINE = "tv_tagline"

    def is_loaded(self):
        return True

    def click_get_started(self):
        return self.click("id", self.GET_STARTED_BTN)


class LoginPage(BasePage):
    EMAIL_INPUT = "et_login_email"
    PASSWORD_INPUT = "et_login_password"
    LOGIN_BTN = "btn_login"
    SIGNUP_LINK = "tv_goto_signup"
    ROLE_SELECTOR = "spinner_role"
    ERROR_TEXT = "tv_error_message"

    def login(self, email, password, role="farmer"):
        self.enter_text("id", self.EMAIL_INPUT, email)
        self.enter_text("id", self.PASSWORD_INPUT, password)
        self.click("id", self.ROLE_SELECTOR)
        self.click("id", self.LOGIN_BTN)
        return True


class SignupPage(BasePage):
    FULLNAME_INPUT = "et_signup_name"
    EMAIL_INPUT = "et_signup_email"
    PHONE_INPUT = "et_signup_phone"
    PASSWORD_INPUT = "et_signup_password"
    CONFIRM_PASSWORD_INPUT = "et_signup_confirm_password"
    ROLE_RADIO_GROUP = "rg_signup_roles"
    REGISTER_BTN = "btn_register"

    def register(self, name, email, phone, password, role="farmer"):
        self.enter_text("id", self.FULLNAME_INPUT, name)
        self.enter_text("id", self.EMAIL_INPUT, email)
        self.enter_text("id", self.PHONE_INPUT, phone)
        self.enter_text("id", self.PASSWORD_INPUT, password)
        self.enter_text("id", self.CONFIRM_PASSWORD_INPUT, password)
        self.click("id", self.REGISTER_BTN)
        return True


class FarmerPage(BasePage):
    DIAGNOSE_BTN = "btn_ai_diagnose"
    OFFLINE_DOCTOR_BTN = "btn_offline_doctor"
    CULTIVATION_BTN = "btn_smart_cultivation"
    RENTAL_HUB_BTN = "btn_rental_hub"
    CROP_POOL_BTN = "btn_crop_pool"
    LIST_PRODUCT_BTN = "btn_list_product"
    WEATHER_CARD = "card_weather_summary"
    IMAGE_CAPTURE_BTN = "btn_capture_leaf"
    CONFIDENCE_SCORE = "tv_confidence"

    def navigate_to_diagnosis(self):
        return self.click("id", self.DIAGNOSE_BTN)

    def list_produce(self, name, price, qty, unit="kg"):
        self.click("id", self.LIST_PRODUCT_BTN)
        self.enter_text("id", "et_product_name", name)
        self.enter_text("id", "et_product_price", str(price))
        self.enter_text("id", "et_product_qty", str(qty))
        self.click("id", "btn_save_produce")
        return True


class DriverPage(BasePage):
    STATUS_TOGGLE = "switch_driver_online"
    ACTIVE_TRIP_CARD = "card_active_trip"
    ACCEPT_TRIP_BTN = "btn_accept_trip"
    COMPLETE_DELIVERY_BTN = "btn_complete_delivery"
    OTP_INPUT = "et_delivery_otp"
    WALLET_BALANCE = "tv_wallet_balance"

    def accept_trip(self):
        return self.click("id", self.ACCEPT_TRIP_BTN)

    def complete_delivery(self, otp):
        self.enter_text("id", self.OTP_INPUT, otp)
        return self.click("id", self.COMPLETE_DELIVERY_BTN)


class UserPage(BasePage):
    SEARCH_BAR = "et_search_produce"
    CATEGORY_FILTER = "chip_category"
    PRODUCT_ITEM = "card_product_item"
    ADD_TO_CART_BTN = "btn_add_to_cart"
    CART_BADGE = "badge_cart_count"
    CHECKOUT_BTN = "btn_checkout"
    DEALS_BANNER = "banner_hot_deals"

    def search_product(self, query):
        self.enter_text("id", self.SEARCH_BAR, query)
        return True

    def add_first_product_to_cart(self):
        return self.click("id", self.ADD_TO_CART_BTN)


class AdminPage(BasePage):
    VERIFY_DRIVERS_BTN = "btn_verify_drivers"
    APPROVE_BTN = "btn_approve_driver"
    REJECT_BTN = "btn_reject_driver"
    METRICS_USERS = "tv_total_users"
    METRICS_ORDERS = "tv_total_orders"

    def verify_driver(self, approve=True):
        self.click("id", self.VERIFY_DRIVERS_BTN)
        if approve:
            return self.click("id", self.APPROVE_BTN)
        return self.click("id", self.REJECT_BTN)

