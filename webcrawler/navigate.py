import aiohttp
import asyncio
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    TimeoutException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from abc import ABC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

headers = {
    "Accept": "application/vnd.linkedin.normalized+json+2.1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-us",
    "Host": "www.linkedin.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Referer": "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3826174215&discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII",
    "Connection": "keep-alive",
    "Cookie": 'UserMatchHistory=AQJBCVMdv_1jPQAAAY4W2R-d1CZA3fcIkXqhAeaxnJ6S153dIOyGOKe5H4ULK_P5M0PoxPWYBzUQ_7WyhG762zv1GQci9X9qQzuKxGlPlrIka4fCJovMvW52UOFrI4szcrnQzk9Od2RFmbgSvrfBIezS8kMp2kUyanM27XsAXrQWX3CXUarjVfZynKzNWzAMIkMABkhAbQZl2jlj8ykKdGlpczV-8yZ_d5R8cEw-2y940a_Q8vLJ85TfAS5fUSdFpo_a4T2xHmiHdM2Bdcm44cDzYdTar_CUfckEI6oSYA; li_theme=light; li_theme_set=app; timezone=America/Los_Angeles; bcookie="v=2&7362594f-4688-4f7e-8b44-021e019759a0"; sdsc=22%3A1%2C1709780153031%7EJAPP%2C0JYOC8raShbDzDPs07nLPV6JlTZA%3D; bscookie="v=1&2023120504552404008dd3-9fc0-4f84-819d-3cdec44a1e80AQH6FkATA72wShRiFj4Kr9WlhF2jlVLe"; fptctx2=taBcrIH61PuCVH7eNCyH0Iitb%252bEMfwlgK%252fM8w%252f28Ebcwewi1iI48QF8fhUizo2JkDO3Te2Fq9kseHcqt11PR38FTzupHIPx9AMLHjXCabUyCMpwWHrndQA2CK3qcYHmgB1YpDjBIB0RTO4Nrfg9wb5AEczRjiTi3FBfLlqDUzJs7cw88xIGTOoSuTeoSn1VhFNzXQy7njoHbHKW5zY4h7wv%252fzrSzK1tycjSLM0hxikF7i0f%252bVlaH5eMRx3sZ2vYYRQ9LjVTPdgJ3w69bOBrDvH1P42fN826cD1NaWB6SDDSwtD6oyx96CMuWkNKPqglYCpOw%252fqpxWdYRBVslRDbd6gT6dd%252feDA6NwXeVWourr8s%253d; lang=v=2&lang=en-us; _gcl_au=1.1.129708492.1709261421; aam_uuid=87913290023092399222140104961849285998; __cf_bm=wDbcd1SPPyGsbiPNsu6y4vRNPe6jhhS635bwhLAh9_4-1709779246-1.0.1.1-XrmDaHf1ZdwMr9K3rnBP9qsE.pOrKYSqR8NzExXiYnNNqVPgWzKdUA6r2V0fpHk78czbYZ86Xp0Wq4xdiqxT4Q; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19790%7CMCMID%7C88490764026591128892124574376159424165%7CMCAAMLH-1710384032%7C9%7CMCAAMB-1710384032%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1709786432s%7CNONE%7CMCCIDH%7C-1332772680%7CvVersion%7C5.1.1; lidc="b=OB32:s=O:r=O:a=O:p=O:g=4306:u=153:x=1:i=1709779225:t=1709865625:v=2:sig=AQGNWnZDCwxgPZKwpXE5xrs29hdGeTcS"; dfpfpt=12f887bcf0c846b18f05711eba6200ad; liap=true; JSESSIONID="ajax:0632936745455031738"; li_at=AQEDASmJRIgFQS60AAABjejmnEcAAAGOMQ0Qc1YALmNp5hLzUed-ALhe7YbYR-_IukfQOuxsFOSp_yXbzkfOMw08hsUe7HTfHnlhKUBtdnU1sY6MnkXkyN-Pg5y7BPQh0a_bIHI9Q6B0xc8n93QEBj0J',
    "csrf-token": "ajax:0632936745455031738",
    "x-li-lang": "en_US",
    "x-restli-protocol-version": "2.0.0",
    "x-li-page-instance": "urn:li:page:d_flagship3_job_collections_discovery_landing;oy0yv3MKRLCT1VuYZhBRYA==",
    "x-li-track": '{"clientVersion":"1.13.11889","mpVersion":"1.13.11889","osName":"web","timezoneOffset":-8,"timezone":"America/Los_Angeles","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":2880,"displayHeight":1800}'
}

class DynamicScraper(ABC):
    """Generalized scraper for dynamic webpages"""
    driver = None

    def start(self, headless=False, debug=False):
        """Opens a chrome browser and connects to the url"""
        opts = Options()
        if headless:
            opts.add_argument("--headless")
        opts.add_argument("−−incognito")
        if debug:
            opts.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(
            options=opts,
            service=Service(ChromeDriverManager().install()),
        )

    def connect(self, url):
        self.driver.get(url)


    def collect(self) -> dict:
        """Collects the data from the webpage"""
        values = {}
        #TODO log-in
        # soup = BS(self.driver.page_source, features="lxml")
        soup = BS(self.driver.page_source, 'html.parser')
        return soup.findall("a")

    def login(self) -> None:
        """Logs in given the information in UserInfo"""
        with open("webcrawler/user_info.txt", "r") as f:
            username = f.readline().replace("\n", "")
            password = f.readline().replace("\n", "")

        element = WebDriverWait(self.driver, 2000).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')))
        element.click()

        # Enters the username
        element = WebDriverWait(self.driver, 2000).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="base-sign-in-modal_session_key"]')))
        element.send_keys(username)

        # Enters the password
        send_password = self.driver.find_element("xpath", '//*[@id="base-sign-in-modal_session_password"]')
        send_password.send_keys(password)

        # Login button
        self.driver.find_element("xpath", '//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button').click()

    def auto_apply(self, information):
        element = WebDriverWait(self.driver, 2000).until(
        EC.element_to_be_clickable((By.ID, 'jobs-apply-button-id')))
        element.click()
        self.recursive_apply(information)

    def recursive_apply(self, information):
        #TODO need a way to look through all the html and find the specific values
        print(1)
        try:
            self.driver.find_element(By.XPATH, '//input[@class=" artdeco-text-input--input"]').send_keys(information["phone"])
        except Exception as e:
            print("No question about phone number found", e)
        try:
            self.driver.find_element("xpath", '//label[@class="jobs-document-upload__upload-button artdeco-button artdeco-button--secondary artdeco-button--2 mt2"]').click()
        except:
            print("No question about resume found")
        try:
            self.driver.find_element("xpath", '//input[@id="follow-company-checkbox"]').click()
        except:
            print("No checkbox found")
        
        # try:
        #     self.driver.find_element("xpath", '//*[@id="ember220"]').click()
            # return
        # except:
        #     print("No submit button found")
        try:
            self.driver.find_element("xpath", '//button[@aria-label="Submit application"]').click()
            return
        except:
            print("No submit application button found")
        
        try:
            self.driver.find_element("xpath", '//button[@aria-label="Continue to next step"]').click()
            self.recursive_apply()
        except:
            print("No next button found")
        try:
            self.driver.find_element("xpath", '//button[@aria-label="Review your application"]').click()
            self.recursive_apply()
        except:
            print("No review button found")