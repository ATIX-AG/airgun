from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import do_not_read_this_widget, TextInput, Widget


class ResourceList(Widget):
    filter = TextInput(locator=ParametrizedLocator(
        "//div[contains(@id, ms-{@parent_entity}) and "
        "contains(@id, {@affected_entity}_ids)]/input[@class='ms-filter']"
    ))
    LIST_FROM = ParametrizedLocator(
        "//div[contains(@id, ms-{@parent_entity}) and "
        "contains(@id, {@affected_entity}_ids)]/div[@class='ms-selectable']"
        "//li[not(contains(@style, 'display: none'))]/span[contains(.,'%s')]"
    )
    LIST_TO = ParametrizedLocator(
        "//div[contains(@id, ms-{@parent_entity}) and "
        "contains(@id, {@affected_entity}_ids)]/div[@class='ms-selection']"
        "//li[not(contains(@style, 'display: none'))]/span[contains(.,'%s')]"
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
                self.browser.element(self.LIST_FROM.locator % value))

    def unassign_resource(self, values):
        for value in values:
            self._filter_value(value)
            self.browser.click(
                self.browser.element(self.LIST_TO.locator % value))

    def manage_resource(self, dict_values):
        if dict_values['operation'] == 'Add':
            self.assign_resource(dict_values['values'])
        if dict_values['operation'] == 'Remove':
            self.unassign_resource(dict_values['values'])

    def read(self):
        do_not_read_this_widget()
