from playwright.sync_api import sync_playwright, Playwright
from time import sleep
import subprocess
import psutil
import os

emails = []

def chrome_is_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            return True
    return False

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    user = os.getlogin()
    output_path = ''.join(('C:/Users/', os.getlogin(), '/Desktop/'))
    try:
        os.remove(f"{output_path}emails.txt")
    except:
        pass
    if chrome_is_running():
        alrt = input("The script will close all open instances of chrome. Do you want to continue (Y/n, Default = Y)? ...")
        if alrt.lower() == "n":
            print("[INFO] Aborting...")
            quit()
            exit()
        else:
            subprocess.call(["taskkill","/F","/IM","chrome.exe"])
        
    try:
        browser = chromium.launch_persistent_context(
            headless=True,
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            user_data_dir=f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data",
            timeout=100000
        )
        print("[INFO] Initializing...")
        page = browser.new_page()
    except:
        print("[ERROR] Please close all instances of Chrome and start again")
        exit()
    
    try:
        page.goto("https://console.firebase.google.com/u/0/project/cpaidevotionalserverdatabase/authentication/users")
        print("[SUCCESS] Page loaded\n")
    except:
        print("[ERROR] Unable to go to page. Reloading...")
        page.goto("https://console.firebase.google.com/u/0/project/cpaidevotionalserverdatabase/authentication/users")
    
    page.click('//*[@id="main"]/fire-router-outlet/authentication-index/ng-component/authentication-users/div/fire-mat-legacy-card/div[2]/fire-mat-legacy-card-actions/user-paginator/mat-paginator/div/div/div[1]/mat-form-field/div[1]/div[2]/div/div')
    page.click('//*[@id="mat-option-2"]')
    page.wait_for_selector('//*[@id="auth-users-table"]/tbody/tr[250]/td[1]')
    paginator = page.locator('//*[@id="main"]/fire-router-outlet/authentication-index/ng-component/authentication-users/div/fire-mat-legacy-card/div[2]/fire-mat-legacy-card-actions/user-paginator/mat-paginator/div/div/div[2]/div').text_content().split(" ")
    end = paginator[3]
    total = paginator[5]

    while int(end) != int(total):
        table = page.locator('//*[@id="auth-users-table"]/tbody')
        with open(f'{output_path}emails.txt', 'a') as file:
            for text in table.text_content().split(" "):
                if "@" in text:
                    file.write(f"{text}\n")
                    emails.append(text)
            

        page.click('//*[@id="main"]/fire-router-outlet/authentication-index/ng-component/authentication-users/div/fire-mat-legacy-card/div[2]/fire-mat-legacy-card-actions/user-paginator/mat-paginator/div/div/div[2]/button[2]')
        page.click('//*[@id="main"]/fire-router-outlet/authentication-index/ng-component/authentication-users/div/fire-mat-legacy-card/div[2]/fire-mat-legacy-card-actions/user-paginator/mat-paginator/div/div/div[2]')
        page.wait_for_load_state('domcontentloaded')
        paginator = page.locator('//*[@id="main"]/fire-router-outlet/authentication-index/ng-component/authentication-users/div/fire-mat-legacy-card/div[2]/fire-mat-legacy-card-actions/user-paginator/mat-paginator/div/div/div[2]/div').text_content().split(" ")
        end = paginator[3]
        print("[INFO] Gotten emails from page",end, "out of", total)

    print("[SUCCESS] Total emails gotten:", len(emails),"[LOADING] Printing emails")
    sleep(1)
    for id, email in enumerate(emails, start=1):
        print(f'{id}:', email)

    print(f"\n[INFO] Saved to {output_path}emails.txt")
    page.close()
    browser.close()



with sync_playwright() as playwright:
    run(playwright)