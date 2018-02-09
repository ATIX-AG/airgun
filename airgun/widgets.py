from widgetastic.exceptions import NoSuchElementException
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Text, TextInput, Widget
from widgetastic.xpath import quote


class ResourceList(Widget):
    filter = TextInput(locator=ParametrizedLocator(
        "//div[contains(@id, ms-{@parent_entity}) and "
        "contains(@id, {@affected_entity}_ids)]/input[@class='ms-filter']"
    ))
    ITEM_FROM = ParametrizedLocator(
        "//div[contains(@id, ms-{@parent_entity}) and "
        "contains(@id, {@affected_entity}_ids)]/div[@class='ms-selectable']"
        "//li[not(contains(@style, 'display: none'))]/span[contains(.,'%s')]"
    )
    ITEM_TO = ParametrizedLocator(
        "//div[contains(@id, ms-{@parent_entity}) and "
        "contains(@id, {@affected_entity}_ids)]/div[@class='ms-selection']"
        "//li[not(contains(@style, 'display: none'))]/span[contains(.,'%s')]"
    )
    LIST_FROM = ParametrizedLocator(
        "//div[contains(@id, ms-{@parent_entity}) and "
        "contains(@id, {@affected_entity}_ids)]/div[@class='ms-selectable']"
        "//li[not(contains(@style, 'display: none'))]"
    )
    LIST_TO = ParametrizedLocator(
        "//div[contains(@id, ms-{@parent_entity}) and "
        "contains(@id, {@affected_entity}_ids)]/div[@class='ms-selection']"
        "//li[not(contains(@style, 'display: none'))]"
    )

    def __init__(self, parent, parent_entity, affected_entity, logger=None):
        Widget.__init__(self, parent, logger=logger)
        self.parent_entity = parent_entity.lower()
        self.affected_entity = affected_entity.lower()

    def _filter_value(self, value):
        self.filter.fill(value)

    def assign_resource(self, values):
        for value in values:
            self._filter_value(value)
            self.browser.click(
                self.browser.element(self.ITEM_FROM.locator % value))

    def unassign_resource(self, values):
        for value in values:
            self._filter_value(value)
            self.browser.click(
                self.browser.element(self.ITEM_TO.locator % value))

    def fill(self, values):
        if values['operation'] == 'Add':
            self.assign_resource(values['values'])
        if values['operation'] == 'Remove':
            self.unassign_resource(values['values'])

    def read(self):
            return {
                'free': [
                    el.text for el in self.browser.elements(self.LIST_FROM)],
                'assigned': [
                    el.text for el in self.browser.elements(self.LIST_TO)]
            }


class Search(Widget):
    search_field = TextInput(id='search')
    search_button = Text("//button[contains(@type,'submit')]")
    default_result_locator = Text("//a[contains(., '%s')]")

    def fill(self, value):
        self.search_field.fill(value)

    def read(self, value, result_locator=None):
        if result_locator is None:
            result_locator = self.default_result_locator
        return self.browser.element(result_locator.locator % value).text

    def search(self, value, result_locator=None):
        self.fill(value)
        self.search_button.click()
        return self.read(value, result_locator)


class HorizontalNavigation(Widget):
    """The Patternfly style horizontal top menu.

    Use :py:meth:`select` to select the menu items. This takes IDs.
    """
    LEVEL_1 = (
        '//ul[contains(@class, "navbar-menu")]/li/a[normalize-space(.)={}]')
    LEVEL_2 = (
        '//ul[contains(@class, "navbar-menu")]/li[./a[normalize-space(.)={}]'
        ' and contains(@class, "open")]/ul/li/a[normalize-space(.)={}]')
    ACTIVE = (
        '//ul[contains(@class, "navbar-menu")]/li[contains(@class, "active")]'
        '/a')

    def select(self, level1, level2=None):
        l1e = self.browser.element(self.LEVEL_1.format(quote(level1)))
        if not level2:
            # Clicking only the main menu item
            self.browser.click(l1e)
            return

        # Hover on the menu on the right spot
        self.browser.move_to_element(l1e)
        l2e = self.browser.wait_for_element(
            self.LEVEL_2.format(quote(level1), quote(level2)))
        self.browser.click(l2e)

    @property
    def currently_selected(self):
        try:
            # Currently we cannot figure out the submenu selection as it is not
            # marked in the UI
            return [self.browser.text(self.ACTIVE)]
        except NoSuchElementException:
            return []
