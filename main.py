from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

URL = "http://59.144.74.15/scheme18/studentresult/index.asp"
PATH = "./chromedriver"
options = Options()
options.binary_location = "/usr/bin/brave-browser-stable" ### Place the executable file of your browser
driver = webdriver.Chrome(options = options, executable_path= PATH)

driver.get(URL)

############Config##########################
rollNosNotPresent = []
minRoll = 184001
maxRoll = 184095
#############################################

rollNos = [x for x in range(minRoll,maxRoll+1) if x not in rollNosNotPresent]
output  = [] 

for roll in rollNos:
    try:
        rollNoInput = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/form/p[4]/input'))
                )
        rollNoInput.clear()
        rollNoInput.send_keys(roll)

        submit = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/form/p[6]/input[2]'))
            )
        submit.click()

        cgpi = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[8]/div[2]/div/div/table[2]/thead/tr[2]/td[4]'))
            )


        output.append([roll, cgpi.text.split('=')[1]])

        print(str(roll) + ": " + cgpi.text.split('=')[1])
        driver.back()


    except:
        print(f"data relevant to {roll} not found!")
        driver.get(URL)
    

data = pd.DataFrame(data=output, columns=["RollNo", "Cgpi"])
print(data)
data.to_csv("./Updatedcgpi.csv")

driver.quit()

