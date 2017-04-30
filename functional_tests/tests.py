from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
  
  def setUp(self):
    self.browser = webdriver.Firefox()

  def wait_for_row_in_list_table(self,row_text):
    start_time = time.time()
    while True:
      try:
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('row_text', [row.text for row in rows])
        return
      except (AssertionError, WebDriverException) as e:
        if time.time() - start_time > MAX_WAIT:
          raise e
        time.sleep(0.5)
  
  def tearDown(self):
    self.browser.quit()
    
  def test_can_start_a_list_and_retrieve_it_later(self):
    # edith opens the todo homepage
    self.browser.get(self.live_server_url)
    
    # she notices the page and title header mentions to-do lists
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text

    # she is invited to enter a todo
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a to-do item'
    )

    # she types "Buy feathers" into a text box
    inputbox.send_keys('Buy feathers')

    #when she hits enter, the page updates with the item as #1
    inputbox.send_keys(Keys.ENTER)

    self.wait_for_row_in_list_table('1.Buy feathers')

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    self.wait_for_row_in_list_table('1.Buy feathers')
    self.wait_for_row_in_list_table('2.Use peacock feathers to make a fly')

    # Edith wonders whether the site will remember her list. Then she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect.
    self.fail('Finish the test!')

    # She visits that url - her to do list is still there
