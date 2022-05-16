import time
from numpy import roll
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tkinter import *


URL = "http://14.139.56.19/scheme18/studentresult/index.asp"
PATH = "./chromedriver"
options = Options()
options.binary_location = "/usr/bin/brave-browser-stable" ### Place the executable file of your browser


output  = [] 
f_name = ""
semester = 1
branch = ""

def takeInps():
    global sem, semester
    global rolls_fname, f_name
    global br, branch
    semester = int(sem.get())
    f_name = rolls_fname.get()
    branch = br.get()
    root.destroy()


#Take Input
root = Tk()
root.title("Result Scrapper NITH")
root.geometry("200x200")

# Semester block:
l = Label(root, text="Semester Count:")
l.pack()
sem = Entry(root)
sem.pack()
sem.focus_set()

# Filename block
l = Label(root, text="Roll No filename")
l.pack()
rolls_fname = Entry(root)
rolls_fname.pack()

# branch
l = Label(root, text="Branch")
l.pack()
br = Entry(root)
br.pack()

#Submit Button
sbmt = Button(root, text="Submit",command=takeInps)
sbmt.pack(side="bottom")

# start app
root.mainloop()

table_no = semester*2+2
rollNos =  pd.read_csv(f_name)["RollNo"].to_numpy()



driver = webdriver.Chrome(options = options, executable_path= PATH)
driver.get(URL)


for roll in rollNos:
    roll = int(roll)
    
    try:
        rollNoInput = WebDriverWait(driver, 7).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/form/p[4]/input'))
                )
        rollNoInput.clear()
        rollNoInput.send_keys(roll)

        submit = WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/form/p[6]/input[2]'))
            )
        submit.click()

        cgpi_xpath = f'/html/body/div/table[{table_no}]/tbody/tr/td[4]/p[2]'
        cgpi = WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.XPATH, cgpi_xpath))
            )


        output.append([roll, cgpi.text.split('=')[1]])

        print(str(roll) + ": " + cgpi.text.split('=')[1])
        driver.back()


    except:
        output.append([roll, "NF"])
        print(f"[ERROR LOG] - Data relevant to {roll} not found! Request Failed!!!")
    
    

data = pd.DataFrame(data=output, columns=["RollNo", "Cgpi"])
print(data)
data.to_csv(f'{semester}_result_{branch}.csv')

driver.quit()

