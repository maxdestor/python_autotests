from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

driver = webdriver.Chrome()
web_address = "https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all"

class sqlData: 
    
    allRows = "select * from Customers"
    byLondon = "select * from Customers where City = \'London\'"
    insertRow = "insert into Customers (CustomerName, Address, City, PostalCode, Country)"\
                    "values (\'Nikolay Karavaev\', \'Nor Aresh 42\', \'Yerevan\', \'00013\', \'Yerevan\')"
    findNikolay = "select * from Customers where CustomerName = \'Nikolay Karavaev\'"
    deleteNikolay = "delete from Customers where CustomerName = \'Nikolay Karavaev\'"
    updateRow = "update Customers " \
                    "set CustomerName = 'Nikolay Karavaev', ContactName = 'Nikolay', "\
                    "Address = 'Nor Aresh 42', City = 'Yerevan', PostalCode = '00013', "\
                    "Country = 'Armenia' "\
                    "where CustomerID = 1"
    groupCities = "select City from Customers Group by City"

class selectors:

    cssTableRows = "#divResultSQL > div > table > tbody > tr"
    cssTableCells = "#divResultSQL > div > table > tbody > tr > td"
    xpathRunSQLButton = "/html/body/div[2]/div/div[1]/div[1]/button"
    xpathRowsCounter = "//*[@id=\"divResultSQL\"]/div/div"

class utility:

    def clickOnRunSql():
            button = driver.find_element(By.XPATH, selectors.xpathRunSQLButton)
            button.click()
            time.sleep(2)

    def sqlInput (sql):
        input_sql = driver.find_element(By.CLASS_NAME, "CodeMirror")
        script = "arguments[0].CodeMirror.setValue(\"{}\");"
        driver.execute_script(script.format(sql), 
                                    input_sql)
            
    def openBrowser():
        driver.get(web_address)

    def checkTestResult(passed):
        if passed == True:
            print("Test Passed")
        else:
            print("Test Failed")

class autotestsClass():

    def checkAddressTest():

        utility.openBrowser()

        utility.sqlInput(sqlData.allRows)
        utility.clickOnRunSql()

        rows = driver.find_elements(By.CSS_SELECTOR, selectors.cssTableRows)

        text_found = False
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, selectors.cssTableCells)
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

        utility.checkTestResult(actual_address == expected_adress)
        driver.quit()

    def londonSixRowsTest():

        utility.openBrowser()

        utility.sqlInput(sqlData.byLondon)
        utility.clickOnRunSql()

        rows = driver.find_elements(By.CSS_SELECTOR, selectors.cssTableRows)

        utility.checkTestResult(len(rows) - 1 == 6)
        driver.quit()

    def newRowInsertTest():

        utility.openBrowser()

        utility.sqlInput(sqlData.insertRow)
        utility.clickOnRunSql()   

        utility.sqlInput(sqlData.findNikolay)
        utility.clickOnRunSql()

        rows = driver.find_elements(By.CSS_SELECTOR, selectors.cssTableRows)

        utility.checkTestResult(len(rows) - 1 == 1)

        utility.sqlInput(sqlData.deleteNikolay)
        utility.clickOnRunSql()

        driver.quit()

    def changeInRowTest():

        referenceTable = ['1', 'Nikolay Karavaev', 'Nikolay', 'Nor Aresh 42',
                            'Yerevan', '00013', 'Armenia']

        utility.openBrowser()
        utility.sqlInput(sqlData.updateRow)
        utility.clickOnRunSql()

        utility.sqlInput(sqlData.findNikolay)
        utility.clickOnRunSql()

        rows = driver.find_elements(By.CSS_SELECTOR, selectors.cssTableRows)
        
        actualTable = []
        
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, selectors.cssTableCells)
            for cell in cells:
                cell_text = cell.text
                actualTable.append(cell_text)

        utility.checkTestResult(actualTable == referenceTable)
        driver.quit()

    def rowsCounterTest():

        utility.openBrowser()

        utility.sqlInput(sqlData.groupCities)
        utility.clickOnRunSql()

        rows = driver.find_elements(By.CSS_SELECTOR, selectors.cssTableRows)
        
        actualCounter = driver.find_element(By.XPATH, selectors.xpathRowsCounter)

        utility.checkTestResult(str(len(rows) - 1) == re.findall('\d+',actualCounter.text)[0])
        driver.quit()