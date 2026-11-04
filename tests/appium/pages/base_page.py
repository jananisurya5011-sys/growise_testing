class BasePage:
    def __init__(self, driver_wrapper):
        self.driver = driver_wrapper

    def click(self, by, value):
        return self.driver.click(by, value)

    def enter_text(self, by, value, text):
        return self.driver.send_keys(by, value, text)

    def get_text(self, by, value):
        return self.driver.get_text(by, value)

    def take_screenshot(self, name):
        return self.driver.take_screenshot(name)

    def press_back(self):
        return self.driver.press_back()

    def rotate(self, orientation):
        return self.driver.rotate_device(orientation)

