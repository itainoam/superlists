from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
  
  def setUp(self):
    self.browser = webdriver.Firefox()
  def tearDown(self):
    self.browser.quit()
  def test_can_start_a_list_and_retrieve_it_later(self):
    # edith opens the todo homepage
    self.browser.get('http://localhost:8000')
    
    # she notices the page and title header mentions to-do lists
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text

    # she is invited to enter a todo
    inputbox = self.browser.find_element_by_id('ud')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a to-do item'
    )
    # she types "Buy feathers" into a text box
    inputbox.send_keys('Buy feathers')

    #when she hits enter, the page updaates with the item as #1
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)

    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertTrue(
      any(row.text == '1: Buy feathers' for row in rows)
    )

    self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()