import aiohttp
import asyncio
import requests
import os
import pickle
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
import urllib3
import socket
import datetime
import platform
import re
from PyPDF2 import PdfReader
from selenium_stealth import stealth
import undetected_chromedriver as uc
from fake_useragent import UserAgent

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


def extract_text_pdf(pdf_file_path):
    try:
        # Open the PDF file in binary read mode
        with open(pdf_file_path, 'rb') as file:
            # Create a PdfReader object
            pdf_reader = PdfReader(file)

            # Get document information (metadata)
            doc_info = pdf_reader.metadata

            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            return text
    except FileNotFoundError:
        print(f"Error: File not found at {pdf_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class DynamicScraper(ABC):
    """Generalized scraper for dynamic webpages"""
    driver = None

    def start(self, headless=False, debug=False, mask=False):
        """Opens a chrome browser and connects to the url"""
        opts = Options()
        if headless:
            opts.add_argument("--headless")
        opts.add_argument("−−incognito")
        if debug:
            opts.add_experimental_option("detach", True)
        if mask:
            # fork_mask()
            opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(
            options=opts,
            service=Service(ChromeDriverManager().install()),
        )

    def connect(self, url):
        self.driver.get(url)


    def collect(self) -> dict:
        """Collects the data from the webpage"""
        values = {}
        # soup = BS(self.driver.page_source, features="lxml")
        soup = BS(self.driver.page_source, 'html.parser')
        return soup.findall("a")

    def get_cookies(self, name=""):
        # Save the cookie if applicable
        with open(os.getcwd()+"/webcrawler/pickles/"+name+"cookies.pkl", 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)
    
    def load_cookies(self, name=""):
        # Loads the cookies
        cookies = pickle.load(open(os.getcwd()+"/webcrawler/pickles/"+name+"cookies.pkl", "rb"))
        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                print("Unable to store cookie:", cookie)
                print(e)
        self.driver.refresh()


class LinkedInBot(DynamicScraper):
    def __init__(self):
        self.genie = GPTBot()
        self.genie.start(mask=True)
        self.genie.connect("https://chatgpt.com/")
        self.genie.login()


    def login(self) -> None:
        try:
            self.load_cookies()
            return
        except Exception as e:
            print(e)
            pass
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
        element = self.driver.find_element("xpath", '//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button')
        try:
            element.click()
        except urllib3.exceptions.ReadTimeoutError:
            return
        self.get_cookies()

    def auto_apply(self, information):
        #Get a list of all job applications
        applications_list = WebDriverWait(self.driver, 2000).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@dir="ltr" and contains(@class, "job-card-container__link")]')))
        applications = self.driver.find_elements(By.XPATH, '//a[@dir="ltr" and contains(@class, "job-card-container__link")]')

        for i, application in enumerate(applications):
            try:
                print(f"Clicking job {i + 1}/{len(applications)}")
                self.driver.execute_script("arguments[0].scrollIntoView();", application)
                application.click()
                
                #Starts the application process
                easy_apply = WebDriverWait(self.driver, 2000).until(
                    EC.element_to_be_clickable((By.ID, 'jobs-apply-button-id')))
                easy_apply.click()
                self.recursive_apply(information)
                done = WebDriverWait(self.driver, 2000).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[@class="artdeco-button__text"]')))
                done.click()
                time.sleep(2)

            except Exception as e:
                print(f"Error on job {i + 1}: {e}")
                #TODO potentially save the html for future testing?
                print("quitting...")
                exit_out = self.driver.find_elements(By.XPATH, '//button[@aria-label="Dismiss"]')[0]
                exit_out.click()
                print("discarding...")

                discard = WebDriverWait(self.driver, 2000).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="Discard"]')))
                discard.click()
                print("done!")

    def recursive_apply(self, information):
        # Things to fill out before clicking to the next slide
        phone_number = self.driver.find_elements(By.XPATH, '//input[@class=" artdeco-text-input--input" and contains(@id, "phoneNumber")]') 
        resume = self.driver.find_elements(By.XPATH, "//input[@type='file' and contains(@name, 'file')]")
        check_box = self.driver.find_elements(By.XPATH, '//label[@for="follow-company-checkbox"]')
        title = self.driver.find_elements(By.XPATH, '//h3')
        # print(title[0].text, phone_number, resume, check_box)

        if len(phone_number) > 0:
            phone_number[0].send_keys(information["phone"])
        if len(resume) > 0:
            resume[0].send_keys(os.getcwd()+"/users/resumes/"+information["resume_name"])
        if len(check_box) > 0:
            check_box[0].click()
        if title[0].text.lower() == 'work authorization':
            self.work_auth()
        if title[0].text.lower() == 'additional questions':
            self.additional()

        # Clicks to the next slide
        submit = self.driver.find_elements(By.XPATH, '//button[@aria-label="Submit application"]')
        next_button = self.driver.find_elements(By.XPATH, '//button[@aria-label="Continue to next step"]')
        review = self.driver.find_elements(By.XPATH, '//button[@aria-label="Review your application"]')
        # print(submit, next_button, review)
        
        if len(submit) > 0:
            submit[0].click()
            return
        if len(next_button) > 0:
            # click next step button
            next_button[0].click()
            return self.recursive_apply(information)
        if len(review) > 0:
            # click review button
            review[0].click()
            return self.recursive_apply(information)
        time.sleep(3)
        return self.recursive_apply(information)
    
    def work_auth(self):
        current = 0
        questions = self.driver.find_elements(By.XPATH, '//span[@class="visually-hidden"]')

        for question in questions:
            check = True
            if "require" in question.text:
                answer = self.driver.find_elements(By.XPATH, '//label[@data-test-text-selectable-option__label="No"]')
                answer[current].click()
                check = False
            if "citizen" in question.text or "authorized to work" in question.text:
                answer = self.driver.find_elements(By.XPATH, '//label[@data-test-text-selectable-option__label="Yes"]')
                answer[current].click()
                check = False
            if check and question.text != "":
                print(question.text)
            current += 1
    

    def additional(self):
        current = 0
        click_questions = self.driver.find_elements(By.XPATH, '//span[@aria-hidden="true"]')
        answer_questions = self.driver.find_elements(By.XPATH, '//label[@class="artdeco-text-input--label"]')

        for question in click_questions:
            check = True
            if "onsite" in question.text or "commuting" in question.text or "Bachelor's" in question.text or "office" in question.text or "following license or certification: Software Engineer" in question.text or "drug test" in question.text  or "background check" in question.text  or "hybrid" in question.text:
                answer = self.driver.find_elements(By.XPATH, '//label[@data-test-text-selectable-option__label="Yes"]')
                answer[current].click()
                check = False
            if check and question.text != "":
                print(question.text)
            current += 1

        current = 0
        for question in answer_questions:
            check = True
            if "years of" in question.text:
                prompt = """
                    For your answer I want it you to put brackets [] around your final answer. Here is my resume: {resume} From the resume, answer the following response double checking that you've only included work experience. Give the answer as a singular digit: {question} 

                """
                resume_str = extract_text_pdf(os.getcwd()+"/users/resumes/"+information["resume_name"])
                prompt = prompt.format(resume=resume_str, question=question.text)
                self.genie.ask(prompt)
                response = self.genie.collect_response()
                answer = "0"
                for r in response:
                    if '[' in r.text:
                        answer = re.findall("(?!\[)[0-9]+(?<!\])", r.text)[-1]
                print("Current and answer:", current, answer)
                answer_box = self.driver.find_elements(By.XPATH, '//input[@class=" artdeco-text-input--input"]') 
                answer_box[current].send_keys(answer)
                check = False
            if check and question.text != "":
                print("Could not find additional question:", question.text)
            current += 1

    def set_genie(self, genie):
        self.genie = genie

    def close(self):
        self.genie.driver.close()
        self.driver.close()



class GPTBot(DynamicScraper):
    def start(self, mask=True):
        """Opens a chrome browser and connects to the url"""
        user_agent = UserAgent().random
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("user-agent={}".format(user_agent))
        self.driver = uc.Chrome(
            # options=chrome_options,
            service=Service(ChromeDriverManager().install()),
        )
        
        # Disable WebDriver flag
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # Execute Cloudflare's challenge script
        self.driver.execute_script("return navigator.language")

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
        )
        
    def login(self) -> None:
        try:
            self.load_cookies("gpt")
            return
        except Exception as e:
            print(e)
            pass
        """Logs in given the information in UserInfo"""
        input("Press ENTER after you have logged in")
        self.get_cookies("gpt")

    def collect_response(self) -> dict:
        """Collects the response from the webpage"""
        return self.driver.find_elements(By.XPATH, '//*[@data-start]')
    
    def ask(self, prompt) -> None:
        """Asks ChatGPT a question"""
        time.sleep(3)
        ask = WebDriverWait(self.driver, 2000).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="prompt-textarea"]')))
        ask.send_keys(prompt)

        time.sleep(3)
        button = WebDriverWait(self.driver, 2000).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="composer-submit-button"]')))
        button.click()



