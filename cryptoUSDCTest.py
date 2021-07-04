# coding=utf-8
import time
from selenium import webdriver
import unittest
from selenium.webdriver.common.action_chains import ActionChains

class CryptoTest(unittest.TestCase):

    def setUp(self):
        # create WebDriver
        self.cryptoDriver = webdriver.Chrome(r'./chromedriver')
        self.cryptoDriver.implicitly_wait(300)
        # webDriver.getpage
        self.cryptoDriver.get('https://crypto.com/exchange')
        self.tabS = self.cryptoDriver.find_elements_by_class_name("e-tabs__nav-item")
        self.croUsdcIsExist = False
        self.cryptoDriver.maximize_window()

    def test_cro_usdc(self):
        try:
            for tab in self.tabS:
                if(tab.text != "CRO"):
                    continue
                ActionChains(self.cryptoDriver).move_to_element(tab)
                time.sleep(1)
                # active CRO tab
                ActionChains(self.cryptoDriver).click(tab).perform()
                # get table one row
                currencyPairs = self.cryptoDriver.find_elements_by_class_name("home-tbody-li")
                for currencyPair in currencyPairs:
                    coinPair = currencyPair.find_element_by_class_name('coin-pair')
                    tradeButton = currencyPair.find_element_by_tag_name('button')
                    targetCurrency = coinPair.find_element_by_class_name("target")
                    sourceCurrency = coinPair.find_element_by_class_name("source")
                    # find CRO/USDC
                    if(targetCurrency.text == "/USDC" and  sourceCurrency.text =="CRO" ):
                        self.croUsdcIsExist = True
                        time.sleep(2)
                        tradeButton.send_keys("\n")
                        time.sleep(2)
                        pairDisplay = self.cryptoDriver.find_element_by_class_name("pair-toggle")
                        print("displayCurrencyPair:", pairDisplay.text)
                        # check click right
                        assert pairDisplay.text == "CRO/USDC", "curreycyPair not equal click Trade"
                        # self.high_bigger_than_low()
            assert self.croUsdcIsExist, "CRO/USDC notExist"
        except Exception,e:
            print("Exception:", e)
            self.cryptoDriver.quit()

    def high_bigger_than_low(self):
        items = self.cryptoDriver.find_elements_by_class_name("item")
        high_value = None
        low_value = None
        for item in items:
            item_title = item.find_element_by_class_name("item-title")
            if(item_title.text == "High"):
                high_value = item.find_element_by_class_name("item-value").text
            if(item_title.text == "Low"):
                low_value = item.find_element_by_class_name("item-value").text
        assert high_value > low_value, "hige Price not bigger than low Price"

    def tearDown(self):
        self.cryptoDriver.quit()

if __name__ == '__main__':
    unittest.main()
