from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from datetime import datetime

# TODO: test a table of packages is displayed if package is good
# TODO: test table can be sorted on columns if package is good


class HomePageTests(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_home_page_displays_title(self):
        self.browser.get('http://127.0.0.1:8000/')
        time.sleep(1)
        # user sees the main title
        self.assertIn('PyPI typosquatting browser demo', self.browser.title)

    def test_home_page_contains_default_package(self):
        self.browser.get('http://127.0.0.1:8000/')
        time.sleep(1)
        input_box = self.browser.find_element_by_name("package_name")
        self.assertEqual(
            input_box.get_attribute('value'),
            'pandas')

    def test_submit_good_package_name(self):
        self.browser.get('http://127.0.0.1:8000/')
        time.sleep(2)
        # user enters a name of a package that is in PyPI and submits
        input_box = self.browser.find_element_by_name("package_name")
        input_box.clear()
        input_box.send_keys('numpy' + Keys.ENTER)
        time.sleep(5)

        title_elements = self.browser.find_elements_by_tag_name("h2")
        titles = []
        for t in title_elements:
            titles.append(t.text)

        # user should see the following titles:
        self.assertIn('Selected package name:', titles)
        self.assertIn('Closest package names:', titles)
        self.assertIn('Some popular PyPI packages are:', titles)
        self.assertIn('References:', titles)

    def test_submit_bad_package_name(self):
        # user enters a name of a package that is not in PyPI and submits
        self.browser.get('http://127.0.0.1:8000/')
        time.sleep(2)
        # user enters a name of a package that is in PyPI and submits
        input_box = self.browser.find_element_by_name("package_name")
        bad_package_name = 'numpy_alksjfalskjfjdfadsf'
        input_box.clear()
        input_box.send_keys(bad_package_name + Keys.ENTER)
        time.sleep(2)

        title_elements = self.browser.find_elements_by_tag_name("h2")
        titles = []
        for t in title_elements:
            titles.append(t.text)

        # user should see the following titles:
        self.assertIn(f'Package {bad_package_name} not found:', titles)
        self.assertIn('Some popular PyPI packages are:', titles)
        self.assertIn('References:', titles)


if __name__ == '__main__':
    unittest.main()
