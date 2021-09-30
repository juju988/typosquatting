from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from datetime import datetime


class HomePageTests(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_home_page_displays_title(self):
        self.browser.get('http://127.0.0.1:8000/')
        # user sees the main title
        self.assertIn('PyPI typosquatting browser demo', self.browser.title)

    def test_home_page_contains_default_package(self):
        self.browser.get('http://127.0.0.1:8000/')
        # user sees the main title
        self.assertIn('PyPI typosquatting browser demo', self.browser.title)
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter SAP Notification No.')



    def test_submit_good_package_name(self):
        # user enters a name that is in PyPI
        text_box = self.browser.find_element_by_name("package_name")
        text_box.send_keys('numpy')
        time.sleep(0.5)
        # user submits
        submit = self.browser.find_element_by_name('submit').click()
        submit.click()

        time.sleep(1)
        titles = self.browser.find_elements_by_tag_name("h2")
        # user should see the following titles:
        self.assertIn('Selected package name:', titles)
        self.assertIn('Closest package names:', titles)
        self.assertIn('Some popular PyPI packages are:', titles)
        self.assertIn('References:', titles)




        table = self.browser.find_element_by_id('open_reports_table')
        self.assertIsNotNone(table)
        rows = table.find_elements_by_tag_name('tr')
        # print(type(rows))
        self.assertIsNotNone(rows)
        self.assertTrue(
            any('JSON Report 1' in row.text for row in rows),
            'Table does not contain \'JSON Report 1\''
        )

        # Bob notices the reports are hyperlinked
        link = self.browser.find_element_by_link_text('Pollution Incident Form')
        self.assertIsNotNone(link)

        # Bob clicks on a report and is taken to the report itself
        self.browser.find_element_by_link_text('Pollution Incident Form').click()
        time.sleep(2)

        titles = self.browser.find_elements_by_tag_name("h2")
        self.assertEqual(title.text, "Edit Report")'''

 
 


if __name__ == '__main__':
    unittest.main()
