# Description: This script is used to change the guest network password of the router.
# It uses the selenium library to automate the process of changing the password.
# The script opens the router login page, enters the password, navigates to the guest network settings,
# and sets the new passkey that is newly generated.
from tools import PasswordFrequency, PasswordStyle

# ======== CONFIGURATION ========
# The router login page URL
router_login_page = 'http://192.168.0.1'
# The password of the router
router_password = 'FaridSahedTelLagan4'
# The URL of the server where the new passkey will be saved
server_url = 'http://localhost:5000/set_new_key'
# The password to set the new passkey
server_password = 'sample_password'
verbose = True # Set to True to see the logs
# ================================

# ======== PASSKEY CONFIGURATION ========
# The characters that will be used to generate the passkey
characters = '0123456789'  # or '0123456789abcdef', '0123456789abcdefABCDEF', etc.
length = 8                 # The length of the passkey
# The frequency of the passkey generation
# if selected frequency is MINUTE, The passkey will remain the same for each minute 
# For multiple passkey generation, the passkey will be generated same for each minute
frequency = PasswordFrequency.SECOND  
password_styles = PasswordStyle.FOUR_ALTERNATE
# ================================

# ======== OPTIONAL CONFIGURATION ========
window_width = 1920
window_height = 1080
# ================================

import hashlib
import datetime

def generate_passkey():
    time_string = datetime.datetime.utcnow().isoformat()
    pf = PasswordFrequency()
    time_string = time_string[:pf.get_truncate_length(frequency)]
    hash_object = hashlib.sha256(time_string.encode())
    digest = hash_object.digest()
    array = list(digest)
    components = [characters[byte % len(characters)] for byte in array]
    passkey = ''.join(components)
    passkey = passkey[:length]

    if password_styles == PasswordStyle.TWO_ALTERNATE:
        # Two alternate characters for variable length passkey
        new_passkey = ''
        for i in range(0, length):
            if(i % 2 == 0):
                new_passkey += passkey[i]
            else:
                new_passkey += passkey[i - 1]
        passkey = new_passkey
    elif password_styles == PasswordStyle.FOUR_ALTERNATE:
        # Four alternate characters for variable length passkey
        new_passkey = ''
        for i in range(0, length):
            if(i % 4 == 0):
                new_passkey += passkey[i]
            elif(i % 4 == 1):
                new_passkey += passkey[i - 1]
            elif(i % 4 == 2):
                new_passkey += passkey[i - 2]
            else:
                new_passkey += passkey[i - 3]
        passkey = new_passkey
    return passkey

# Importing the required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests as rq
import warnings

# Ignore the DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set up the webdriver with headless option
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Optional: Disable GPU acceleration
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(window_width, window_height)

driver.get(router_login_page)
if verbose:
    print("[+] --- Opened the router login page")

time.sleep(6) # Wait for the page to load (You can increase the time if your internet connection is slow)

password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"].text-text.password-text.password-hidden')
password_input.send_keys(router_password)
login_button = driver.find_element(By.CSS_SELECTOR, 'a.button-button[title="LOG IN"]')
login_button.click()

time.sleep(8) # Wait for the page to load (You can increase the time if your internet connection is slow)

advanced_button = driver.find_element(By.XPATH, "//span[text()='Advanced']")
advanced_button.click()

time.sleep(1.5)

wireless_link = driver.find_elements(By.XPATH, "//span[@class='sub-navigator-text' and text()='Wireless']")[1]
wireless_link.click()

time.sleep(1.5)

guestNetworkAdv = driver.find_element(By.XPATH, "//li[@navi-value='guestNetworkAdv']").find_element(By.XPATH, '//span[text()="Guest Network"]')
guestNetworkAdv.click()

time.sleep(2.5)

guest_network_header = driver.find_element(By.XPATH, "//h3[@class='panel-title']//span[@class='panel-title-text' and text()='Guest Network']")
guest_main = guest_network_header.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
text_input = guest_main.find_elements(By.CSS_SELECTOR, 'div.widget-wrap-outer.text-wrap-outer input[type="text"]')[3]

# Clear the input field before entering the new passkey
text_input.send_keys('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')

passkey = generate_passkey()
text_input.send_keys(passkey)

time.sleep(1)

save_button = driver.find_elements(By.XPATH, "//a[@href='javascript:void(0);' and @class='button-button' and @type='button' and @title='SAVE']")[1]
save_button.click()

time.sleep(2.5)

if verbose:
    print('[+] --- New Passkey Set to :', passkey)
# Close the browser
driver.quit()
if verbose:
    print("[+] --- Browser Closed")

# Send the new passkey to the server
if server_url and server_password:
    if verbose:
        print("[+] --- Sending the new passkey to the server")

    try:
        res = rq.post(server_url, data={'password': server_password, 'new_key': passkey})
        res.raise_for_status()
    except rq.exceptions.RequestException as e:
        # Handle the exception (e.g., log the error, retry the request, etc.)
        print(f"[!] --- An error occurred: {e}")
    if res.status_code == 200 and verbose:
        print("[+] --- New Passkey sent to the server successfully")
