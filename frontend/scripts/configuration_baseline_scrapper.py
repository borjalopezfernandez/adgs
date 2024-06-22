"""
HMI scrapper utility for the reprocessing configuration baseline
"""
# Import python utilities
import time
import argparse
import glob
import os

# Import Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

####
# Logging
####
# Import python utilities
import logging
from logging.handlers import RotatingFileHandler

class RotatingFileHandlerAllUsers(RotatingFileHandler):

    def doRollover(self):
        """
        Override base class method to change the permissions to 666 of the new log file.
        """
        # Rotate the file first.
        RotatingFileHandler.doRollover(self)

        # Change permission of the log file to 666
        os.chmod(self.baseFilename, 0o0666)

class Log():

    def __init__(self, name = None):
        """
        Definition of the logging for the HMI scrapper
        
        :param name: name of the module
        :type name: string
        """
        
        # Define logging configuration
        if name == None:
            name = __name__
        # end if
        self.logger = logging.getLogger(name)

        self.logger.setLevel("INFO")

        # format for logs
        formatter = logging.Formatter("%(levelname)s\t; (%(asctime)s.%(msecs)03d) ; %(name)s(%(lineno)d) [%(process)d] -> %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")

        stream_handlers = [handler for handler in self.logger.handlers if type(handler) == logging.StreamHandler]
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        file_handlers = [handler for handler in self.logger.handlers if type(handler) == RotatingFileHandlerAllUsers]
        if len(file_handlers) < 1:
            # Set the path to the log file
            file_handler = RotatingFileHandlerAllUsers("/tmp/hmi_scrapper.log", maxBytes=50000000, backupCount=30)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        # end if

        return

specific_logging = Log(name = __name__)
logger = specific_logging.logger

def init_driver(display:bool = False) -> object:
    """
    Function to initialize the driver for scrapping

    :param display: flag to indicate if the execution of the task needs to be displayed in a browser
    :type display: bool

    :return: flag to indicate the activation of the display of the browser
    :rtype: bool
    """
    global final_download_directory_path

    logger.info("Initializing driver...")
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-notifications')

    # To avoid scrolls set the scale to 0.75
    options.add_argument("force-device-scale-factor=0.75")

    # Activate display if requested
    if not display:
        options.add_argument('--headless')
    else:
        logger.info("Display activated.")
    # end if
    
    driver = webdriver.Chrome(options=options)
    
    # Required change resolution to be able to select elements in some cases
    driver.set_window_size(2560, 1440)
    driver.maximize_window()

    logger.info("Driver initialized :-)")
    
    return driver

def terminate_scrapper(driver:object) -> None:  
    """
    Function to close chromedriver and sessions of selenium

    :param driver: driver to access to the browser
    :type driver: object
    """
    driver.stop_client()
    driver.quit()
    
    return

def find_xpath_elements(driver:object, xpath:str) -> list:
    """
    Function to find elements by xpath with infinite retrials

    :param driver: driver to access to the browser
    :type driver: object
    :param xpath: xpath to the element to find
    :type xpath: str

    :return: found element
    :rtype: object
    """
    elements = []
    done = False
    wait = WebDriverWait(driver, 10)
    while not done:
        elements = driver.find_elements(By.XPATH, xpath)
        if len(elements) > 0:
            done = True
        else:
            logger.warning(f"Elements with xpath {xpath} are not visible yet. Trying again its access after 1 s...")
            time.sleep(1)
        # end if
    # end while
    
    return elements

def find_xpath_element(driver:object, xpath:str) -> object:
    """
    Function to find an element by xpath with infinite retrials

    :param driver: driver to access to the browser
    :type driver: object
    :param xpath: xpath to the element to find
    :type xpath: str

    :return: found element
    :rtype: object
    """
    element = None
    done = False
    wait = WebDriverWait(driver, 10)
    
    while not done:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            done = True
        except:
            logger.warning(f"Element with xpath {xpath} is not visible yet. Trying again its access after 1 s...")
            time.sleep(1)
            pass
        # end try
    # end while
    
    return element

def dynamic_click(element):
    """
    Function to click an element with infinite retrials

    :param driver: driver to access to the browser
    :type driver: object
    :param xpath: xpath to the element to find
    :type xpath: str

    :return: found element
    :rtype: object
    """

    done = False
    while not done:
        try:
            element.click()
            done = True
        except ElementNotInteractableException:
            logger.warning(f"Element is not interactable. This is consider no issue as they are ussually hidden checkboxes. This element is skipped.")
            break
        except:
            logger.warning(f"Element not clickable yet. Trying again its click after 1 s...")
            time.sleep(1)
            pass
        # end try
    # end while

    # After clicking perform a little delay
    time.sleep(1)
    
    return

# Define dynamic_click for WebElement
WebElement.dynamic_click = dynamic_click

def execute_scrapper(url:str, mission:str, output_path:str, display:bool = False, applicability:bool = False) -> None:
    """
    Function to execute a scrapper in a 4EO HMI

    :param url: url of the web reprocessing configuration baseline
    :type url: str
    :param mission: mission of the web reprocessing configuration baseline
    :type mission: str
    :param output_path: path to the output file
    :type output_path: str
    :param display: flag to indicate if the execution of the task needs to be displayed in a browser
    :type display: bool
    :param applicability: flag to indicate if the application of the time window needs to be used
    :type applicability: bool
    """

    # Open output file
    f= open(output_path,"w+")

    # Write header
    f.write('''Application From,Application To,Product Level,Product Type,Auxiliary Type,Auxiliary File,IPF Version
''')
    
    # Initialize driver
    driver = init_driver(display)

    # Access to the web
    driver.get(url)

    # Give time to the page to load
    time.sleep(2)

    # Select relevant mission
    mission_selector = find_xpath_elements(driver, "//select[@id='select_mission']")[0]
    mission_selector.send_keys(mission)
    
    # Activate the application of dates
    if applicability:
        application_dates = find_xpath_elements(driver, "//*[contains(@class,'lcs_switch')]")[0]
        application_dates.dynamic_click()
    # end if

    # Give time for datatables module to start
    time.sleep(2)

    # Go to next page
    while True:

        # Wait until  Loading is not visible
        loading = driver.find_elements(By.XPATH, "//div[@id='table_id_processing' and @style='display: block;']")
        loading_retries = 0
        while len(loading) > 0:
            if loading_retries == 3:
                logger.error("Page got blocked loading products")
                break
            # end if
            time.sleep(1)
            loading = driver.find_elements(By.XPATH, "//div[@id='table_id_processing' and @style='display: block;']")
            logger.warning("Page is still loading products. Waiting 1 s for the products to be listed")
            loading_retries += 1
        # end while

        if loading_retries == 3:
            break
        # end if
            
        auxiliary_data_rows = driver.find_elements(By.XPATH, "//table[@id = 'table_id']/tbody/tr[count(td) > 1]")
        if len(auxiliary_data_rows) == 0:
            break
        # end if
        for auxiliary_data_row in auxiliary_data_rows:
            application_from = auxiliary_data_row.find_elements(By.XPATH, "td[2]")[0].text
            application_to = auxiliary_data_row.find_elements(By.XPATH, "td[3]")[0].text
            associated_product_level = auxiliary_data_row.find_elements(By.XPATH, "td[4]")[0].text
            associated_product_types = auxiliary_data_row.find_elements(By.XPATH, "td[5]")[0].text
            auxiliary_type = auxiliary_data_row.find_elements(By.XPATH, "td[6]")[0].text
            auxiliary_file = auxiliary_data_row.find_elements(By.XPATH, "td[7]")[0].text
            ipf_version = auxiliary_data_row.find_elements(By.XPATH, "td[8]")[0].text
            f.write(f'''"{application_from}","{application_to}","{associated_product_level}","{associated_product_types}","{auxiliary_type}","{auxiliary_file}","{ipf_version}"
''')
        # end for

        next_button_disabled = driver.find_elements(By.XPATH, "//*[@id='table_id_next' and contains(@class,'disabled')]")
        if len(next_button_disabled) > 0:
            logger.info("There are no more auxiliary data products displayed. Stopping scanning...")
            break
        else:
            next_button = find_xpath_elements(driver, "//*[@id='table_id_next']")[0]
            next_button.dynamic_click()
            logger.info("Retrieving next batch of auxiiliary products")
        # end if
    # end while

    # Close output file
    f.close()
    
    # Terminate selenium driver
    terminate_scrapper(driver)

    return

def main():
    """
    Function to manage the scrapper of the web reprocessing configuration baseline
    """
    
    parser = argparse.ArgumentParser(prog="adgs_scrapper", description="An automation tool to scrape the reprocessing configuration baseline")

    parser.add_argument("-m", dest="mission", required=True,
                        help="Mission to filter")    
    parser.add_argument("-u", dest="url", required=True,
                        help="Url to access to the web of the reprocessing configuration baseline")
    parser.add_argument("-o", dest="output_path", type=str, nargs=1,
                             help="path to the output file", required=True)
    parser.add_argument("-d", "--display", required=False,
                        help="Show the browser while executing the relevant task", action="store_true")
    parser.add_argument("-a", "--applicability", required=False,
                        help="Activate applicability window", action="store_true")
    args = parser.parse_args()

    # Data from arguments
    mission = args.mission
    url = args.url
    display = args.display
    applicability = args.applicability
    # Output path
    output_path = args.output_path[0]
    # Check if file exists
    if not os.path.isdir(os.path.dirname(output_path)):
        logger.error(f"The specified path to the output file {output_path} does not exist")
        exit(-1)
    # end if

    logger.info("Welcome to the scrapper of the web reprocessing configuration baseline. You have requested to execute it with the following parameters:")
    logger.info("Mission: {}".format(mission))
    logger.info("Url: {}".format(url))
    logger.info("Display: {}".format(display))
    logger.info("Applicability: {}".format(applicability))
    logger.info("Output path: {}".format(output_path))

    # Execute scrapper
    execute_scrapper(url, mission, output_path, display, applicability)
    
    return

if __name__ == "__main__":
    main()
