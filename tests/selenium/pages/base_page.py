class BaseWebPage:
    def __init__(self, driver_wrapper):
        self.driver = driver_wrapper

    def navigate(self, path=""):
        return self.driver.navigate_to(path)

    def click(self, by, selector):
        return self.driver.click(by, selector)

    def enter_text(self, by, selector, text):
        return self.driver.type_text(by, selector, text)

    def set_viewport(self, width, height):
        return self.driver.set_window_size(width, height)

    def take_screenshot(self, name):
        return self.driver.take_screenshot(name)

    def refresh(self):
        return self.driver.refresh()

    def back(self):
        return self.driver.back()

    def forward(self):
        return self.driver.forward()

