from ftw.builder import Builder
from ftw.builder import create
from ftw.labels.testing import LABELS_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase


class LabelJarPortletFunctionalTest(TestCase):

    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    @browsing
    def test_portlet_is_disabled_per_default(self, browser):
        browser.visit()

        self.assertFalse(browser.css('labelJarPortlet'))

    @browsing
    def test_protlet_is_enabled_if_ILabelRoot_is_provided(self, browser):
        folder = create(Builder('label root'))
        browser.visit(folder)

        self.assertTrue(browser.css('.labelJarPortlet'))

    @browsing
    def test_list_all_labels_in_the_jar(self, browser):
        folder = create(Builder('label root')
                        .with_labels(('Label 1', ''), ('Label 2', '')))

        browser.visit(folder)

        self.assertItemsEqual(
            ['Label 1', 'Label 2'],
            browser.css('.labelJarPortletListingItemTitle').text)

    @browsing
    def test_add_color_to_each_listing_item(self, browser):
        folder = create(Builder('label root').with_labels(('James', 'red')))

        browser.visit(folder)

        self.assertEqual(
            ['background-color=red'],
            [browser.css('.labelJarPortletListingItem')
                .first.attrib.get('style')])