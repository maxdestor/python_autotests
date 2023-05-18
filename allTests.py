from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

driver = webdriver.Chrome()
web_address = "https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all"


def clickOnRunSql():
        button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/button')
        button.click()

def sql_input (sql):
    input_sql = driver.find_element(By.CLASS_NAME, "CodeMirror")
    script = "arguments[0].CodeMirror.setValue(\"{}\");"
    driver.execute_script(script.format(sql), 
                                input_sql)
        
def openBrowser():
    driver.get(web_address)

class autotestsClass():
    def checkAddressTest():

        openBrowser()

        sql_input("select * from Customers")
        clickOnRunSql()
        time.sleep(2)

        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

        for row in rows:
            cells = row.find_elements(By.XPATH, "//td")
            for cell in cells:
                cell_text = cell.text
                expected_text = "Giovanni Rovelli"
                if cell_text == expected_text:
                    found_cell_id = cells.index(cell)
                    text_found = True
                    break
            if text_found:
                break
        actual_address = cells[found_cell_id+1].text
        expected_adress = "Via Ludovico il Moro 22"

        if actual_address == expected_adress:
            print("Test Passed")
        else:
            print("Test Failed")

        driver.quit()

    def londonSixRowsTest():

        openBrowser()

        sql_input("select * from Customers where City = \'London\'")
        clickOnRunSql()
        time.sleep(2)

        rows = driver.find_elements(By.CSS_SELECTOR, "#divResultSQL > div > table > tbody > tr")

        if len(rows) - 1 == 6:
            print("Test Passed")
        else: 
            print("Test Failed")

        driver.quit()

    def newRowInsertTest():

        openBrowser()
        input_sql = driver.find_element(By.CLASS_NAME, "CodeMirror")
        driver.execute_script("arguments[0].CodeMirror.setValue\
                            (\"insert into Customers (CustomerName, Address, City, PostalCode, Country)\
                            values ('Nikolay Karavaev', 'Nor Aresh 42', 'Yerevan', '00013', 'Yerevan')\");", 
                                input_sql)
        
        clickOnRunSql()   

        time.sleep(2)

        driver.execute_script("arguments[0].CodeMirror.setValue(\"select * from Customers where CustomerName = 'Nikolay Karavaev'\");", input_sql)
        clickOnRunSql()

        time.sleep(2)
        rows = driver.find_elements(By.CSS_SELECTOR, "#divResultSQL > div > table > tbody > tr")

        if len(rows) - 1 == 1:
            print("Test Passed")
        else: 
            print("Test Failed")

        driver.execute_script("arguments[0].CodeMirror.setValue\
                                ('delete from Customers where CustomerName = \"Nikolay Karavaev\"');",
                                input_sql)
        time.sleep(2)
        clickOnRunSql()

        driver.quit()

    def changeInRowTest():

        referenceTable = ['1', 'Nikolay Karavaev', 'Nikolay', 'Nor Aresh 42', 'Yerevan', '00013', 'Armenia']

        openBrowser()
        input_sql = driver.find_element(By.CLASS_NAME, "CodeMirror")
        driver.execute_script("arguments[0].CodeMirror.setValue" \
                            "(\"update Customers " \
                            "set CustomerName = 'Nikolay Karavaev', ContactName = 'Nikolay', "\
                            "Address = 'Nor Aresh 42', City = 'Yerevan', PostalCode = '00013', "\
                            "Country = 'Armenia' "\
                            "where CustomerID = 1 \");", 
                            input_sql)

        clickOnRunSql()
        time.sleep(2)

        driver.execute_script("arguments[0].CodeMirror.setValue\
                            (\"select * from Customers where CustomerName = 'Nikolay Karavaev'\");", 
                            input_sql)
        
        clickOnRunSql()
        time.sleep(2)

        rows = driver.find_elements(By.CSS_SELECTOR, "#divResultSQL > div > table > tbody > tr")
        
        actualTable = []
        
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "#divResultSQL > div > table > tbody > tr > td")
            for cell in cells:
                cell_text = cell.text
                actualTable.append(cell_text)

        if actualTable == referenceTable:
            print("Test Passed")
        else: 
            print("Test Failed")
            driver.quit()

        driver.quit()

    def rowsCounterTest():

        openBrowser()

        sql_input("select City from Customers Group by City")
        clickOnRunSql()
        time.sleep(2)

        rows = driver.find_elements(By.CSS_SELECTOR, "#divResultSQL > div > table > tbody > tr")
        
        actualCounter = driver.find_element(By.XPATH, "//*[@id=\"divResultSQL\"]/div/div")

        if str(len(rows) - 1) == re.findall('\d+',actualCounter.text)[0]:
            print("Test Passed")
        else: 
            print("Test Failed")