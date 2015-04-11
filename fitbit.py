from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import json
import re
import time

USERNAME = "chan.hyeo.ni.3698@gmail.com"
PASSWORD = "tpxkr369*"

if __name__ == "__main__":
  display = Display(visible=0, size=(800, 600))
  display.start()

  browser = webdriver.Firefox()
  browser.get("http://www.fitbit.com/login")
  assert "Fitbit Login" in browser.title
  delay = 3

  try:
    print "Page is ready!"

    form = browser.find_element_by_css_selector("form#loginForm")
    input_username = browser.find_element_by_name("email")
    input_password = browser.find_element_by_name("password")

    browser.execute_script("$('input.field.email').val('" + USERNAME + "')")
    browser.execute_script("$('input.field.password').val('" + PASSWORD + "')")

    browser.find_element_by_css_selector("button.common-btn.common-btn-submit.track-Auth-Login-ClickFitbit").click()
    literal_source = browser.page_source

    # Optional: Save entire source code into an external .html file
    # html_source = browser.page_source.encode('utf-8')
    # fo = open("index.html", "wb")
    # fo.write(html_source)
    # fo.close()

    html_string = repr(literal_source.encode("utf-8"))
    # Heart Rate JSON Data - Regex Expression: (\{\"bpm\".*?\})
    match_data = re.findall(r'(\{\"bpm\".*?\})', html_string)
    """  WE HAVE TO PUT the newline character to make seperation between """
    print json.loads(match_data[0])["dateTime"]

    fo = open('./Analytics/' + json.loads(match_data[0])["dateTime"][0:json.loads(match_data[0])["dateTime"].index(" ")] + ".json", "wb")
    fo.write('['+''.join(match_data)+']')
    filename = fo.name
    fo.close()

    # open .json file again to parse the data readable for the 
    json_file = open(filename, 'r')
    content = json_file.read()
    json_file.close()     
    content = content.replace("}{", "},\n{")
    d = open(filename, 'w')
    d.write(content)
    d.close()

    browser.find_element_by_css_selector("div.nav-item:nth-child(1)").click()
    browser.find_element_by_css_selector("#header-settings-subnav > li:nth-child(15) > a:nth-child(1)").click()
  except NoSuchElementException:
    print "Error... An element was not found."
  except NoSuchElementException:
    print "Element is not found."

  browser.close()
  display.stop()
