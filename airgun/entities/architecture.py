from navmazing import NavigateToSibling
from widgetastic.widget import View, Text, TextInput

from airgun.base import menu_click
from airgun.navigation import BaseNavigator, navigator


class Architecture(View):
    title = Text("//h1[text()='Architectures']")
    new = Text("//a[contains(@href, '/architectures/new')]")
    search = Text("//a[contains(., '{}')]")
    navigate_locator = "//a[@id='menu_item_architectures']"

    @property
    def is_displayed(self):
        return self.browser.wait_for_element(
            self.title, exception=False) is not None

    def create_architecture(self, values):
        navigator.navigate(self, 'New')
        new_view = ArchitectureDetails(self.browser)
        new_view.change_values(values)


class ArchitectureDetails(View):
    name = TextInput(locator="//input[@id='architecture_name']")
    submit = Text('//input[@name="commit"]')

    @property
    def is_displayed(self):
        return self.browser.wait_for_element(
            self.name, exception=False) is not None

    def change_values(self, values):
        self.fill(values)
        self.browser.click(self.submit)


@navigator.register(Architecture, 'All')
class ShowAllArchitectures(BaseNavigator):
    VIEW = Architecture

    # prerequisite = NavigateToSibling('Dashboard')

    def step(self, *args, **kwargs):
        menu_click(
            ["//a[@id='hosts_menu']", self.view.navigate_locator],
            self.view.browser
        )


@navigator.register(Architecture, 'New')
class AddNewArchitecture(BaseNavigator):
    VIEW = ArchitectureDetails

    prerequisite = NavigateToSibling('All')

    def step(self, *args, **kwargs):
        self.view.browser.wait_for_element(
            self.view.new, ensure_page_safe=True)
        self.view.browser.click(self.view.new)
