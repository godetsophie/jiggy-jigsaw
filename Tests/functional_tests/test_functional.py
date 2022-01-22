import pytest
from selenium import webdriver
import unittest
import os
import sys
import pytest
import time

class FunctionalTests(unittest.TestCase):

	def setUp(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--no-sandbox')
		self.driver = webdriver.Chrome(os.path.join(os.environ["ChromeWebDriver"], 'chromedriver.exe'), chrome_options=options)
		self.driver.implicitly_wait(300)

	def test_selenium(self):
		pass;

	def tearDown(self):
		try:
			self.driver.quit()
		except Exception as e:
			print('tearDown.Error occurred while trying to close the selenium chrome driver: ' + str(e))
