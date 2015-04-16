from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import json
import re
import time
from pandas.io.json import read_json

USERNAME = "chan.hyeo.ni.3698@gmail.com"
PASSWORD = "tpxkr369*"


def connect():
    # Substitute the 5 pieces of information you got when creating
    # the Mongo DB Database (underlined in red in the screenshots)
    # Obviously, do not store your password as plaintext in practice
    
    connection = MongoClient("ds062097.mongolab.com",62097)
    handle = connection["fitbit"]
    handle.authenticate("root","root")
    return handle


def get_splitted_column_for_datetime(new_column_name, datetime_string):
    # split the string by special characters, and return the element depending on the name of new_column_name
    # for example, if new_column_name = 'year', then it will return the zeroth element of the splitting string
    
    # Parmater 
    # new_column_name : the name of the column
    # datetime_string : the string version of datetime (e.g. 2015-4-10 00:00:00)
    
    # Returns
    # the date, if the new_column_name is not matched with the appropriate column name, it should return -1
    
    date_elements = re.findall(r"[\w']+", str(datetime_string))
    
    if (new_column_name == 'year'):
        return int(date_elements[0])
    elif (new_column_name == 'month'):
        return int(date_elements[1])
    elif (new_column_name == 'day'):
        return int(date_elements[2])
    elif (new_column_name == 'hr'):
        return int(date_elements[3])
    elif (new_column_name == 'min'):
        return int(date_elements[4])
    elif (new_column_name == 'sec'):
        return int(date_elements[5])
    
    return -1
    

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

    fo = open('./data/fitbit/' + json.loads(match_data[0])["dateTime"][0:json.loads(match_data[0])["dateTime"].index(" ")] + ".json", "wb")
    fo.write('['+''.join(match_data)+']')
    filename = fo.name
    fo.close()

    # open .json file again to parse the data readable for the dataFrame in the future
    json_file = open(filename, 'r')
    content = json_file.read()
    json_file.close()     
    content = content.replace("}{", "},\n{")
    d = open(filename, 'w')
    d.write(content)
    d.close()
    
    e = open(filename, 'r')
    data_df = read_json(e, orient='records')
    data_df['year'] = data_df["dateTime"].apply(lambda x: get_splitted_column_for_datetime('year', x))
    data_df['month'] = data_df["dateTime"].apply(lambda x: get_splitted_column_for_datetime('month', x))
    data_df['day'] = data_df["dateTime"].apply(lambda x: get_splitted_column_for_datetime('day', x))
    data_df['hr'] = data_df["dateTime"].apply(lambda x: get_splitted_column_for_datetime('hr', x))
    data_df['min'] = data_df["dateTime"].apply(lambda x: get_splitted_column_for_datetime('min', x))
    data_df['sec'] = data_df["dateTime"].apply(lambda x: get_splitted_column_for_datetime('sec', x))
    del data_df["dateTime"] 
    e.close()
    
    data_df.to_json(filename, orient='records')
    
    # do the same process again
    json_file = open(filename, 'r')
    content = json_file.read()
    json_file.close()     
    content = content.replace("},{", "},\n{")
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


  # write the mongodb client to write the data to the mongodb database server
  handle = connect()







