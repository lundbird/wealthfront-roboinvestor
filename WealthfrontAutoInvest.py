'''
Created on Jul 4, 2017

@author: alex
'''
from selenium import webdriver
from bs4 import BeautifulSoup
import re,os,time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from pandas.core.datetools import BDay


def main():
    #for now im just going to account for the discover balance:just put balance on this one card in the future
    paycheckSpanDays=14
    paycheckDate=datetime.date(2017,6,2)
    rent=775
    rentDate=datetime.date(2017,6,1)
    discretionary=float(200)
    
    #discoverDate=datetime.date(2017,6,22)
    discoverDate=datetime.date(2017,6,13)
    chaseDate=datetime.date(2017,6,19)
    amexDate=datetime.date(2017,6,11)    
    liabilities=(discoverDate,chaseDate,amexDate)
      
    today=datetime.date.today()
    
    rentDate=rentDate.replace(month=today.month+1)
    if today==(rentDate-BDay(6)).date(): Withdraw(rent)
    print('rent Date: {}'.format(rentDate))
    
        #finds all the due dates
    i=0
    re
    for liability in liabilities:   #rent, discover,chase,amex  #not tested
        liability=liability.replace(month=today.month)
        print('liability-5bday {}'.format((liability-BDay(6)).date()))
        if today==(liability-BDay(6)).date():
            chase_pymt,amex_pymt,discover_pymt=FindCreditLiabilities() #turn this into class to cut out 10 lines of code
            if i==0:
                if float(discover_pymt)>250:
                    Withdraw(discover_pymt) 
                elif float(discover_pymt)>0:
                    Withdraw(250)
                    Deposit(250-discover_pymt)
            if i==1:
                if float(chase_pymt)>250:
                    Withdraw(chase_pymt) 
                elif float(chase_pymt)>0:
                    Withdraw(250)
                    Deposit(250-chase_pymt)
            if i==2:
                if float(amex_pymt)>250:
                    Withdraw(amex_pymt) 
                elif float(amex_pymt)>0:
                    Withdraw(250)
                    Deposit(250-amex_pymt)        
        i=i+1
        
        
           
    while paycheckDate< today: #finds next pay check date +1
        NextPayCheck=paycheckDate+datetime.timedelta(days=paycheckSpanDays)
    print('NextPayCheck: {}'.format(NextPayCheck))
    
    #finds if we will need to make a deposit
    doNotDeposit=False
    for liability in liabilities: #prevents depositing if you have a liability
        if today==liability-datetime.timedelta(days=1): doNotDeposit=True
    if today==paycheckDate & doNotDeposit==False:
        checking=FindChecking()
        Deposit(float(checking)-discretionary) 
    
    try:
        driver.close()
    except:
        print("driver not open")

def Login():   
    global driver
    driver=webdriver.Firefox()
    driver.get('https://www.wealthfront.com/dashboard')
    driver.find_element_by_id('username').send_keys('****')
    driver.find_element_by_id('password').send_keys('****')
    driver.find_element_by_xpath("//button[@type='submit']").click()
    
def FindChecking():
    Login()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Cash-subgroup')))
    soup=BeautifulSoup(driver.page_source,'html.parser')
    cash=soup.find('div',{'id':'Cash-subgroup'}).find_all('div',{'class':'dashboard-external-account-subgroup-component-value no-margin--bottom text-right'})[0].text
    print(cash)
    return(cash[1:])

def FindCreditLiabilities():
    Login()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Liabilities-subgroup")))
    soup=BeautifulSoup(driver.page_source,'html.parser')
    
    liabilities=soup.find('div',{'id':'Liabilities-subgroup'}).find_all('div',{'class':'dashboard-external-account-external-account-card-component widget-section widget-padded'})
    chase_pymt=liabilities[0].find('div',{'class':'dashboard-external-account-external-account-card-component-account-value no-margin--bottom text-right'}).text[1:]
    amex_pymt=liabilities[1].find('div',{'class':'dashboard-external-account-external-account-card-component-account-value no-margin--bottom text-right'}).text[1:]
    discover_pymt=liabilities[2].find('div',{'class':'dashboard-external-account-external-account-card-component-account-value no-margin--bottom text-right'}).text[1:]
    
    print(chase_pymt)
    print(amex_pymt)
    print(discover_pymt)
    
    return (chase_pymt,amex_pymt,discover_pymt)

def Deposit(amount):
    time.sleep(2)
    driver.get('https://www.wealthfront.com/fund/bank')
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "amount")))
    driver.find_element_by_id('amount').send_keys(str(amount))
    time.sleep(0.1)
    driver.find_element_by_css_selector("button.btn.btn-primary").click()

def Withdraw(amount): 
    Login()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Liabilities-subgroup")))
    driver.find_element_by_link_text("Transfer Funds").click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span")))
    driver.find_element_by_css_selector("span").click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[@name='withdrawal-reason'])[4]")))
    driver.find_element_by_xpath("(//input[@name='withdrawal-reason'])[4]").click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary")))
    driver.find_element_by_css_selector("button.btn.btn-primary").click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "amount")))
    driver.find_element_by_name("amount").send_keys(str(amount))
    driver.find_element_by_css_selector("button.btn.btn-primary").click()
    time.sleep(.5)
    driver.find_element_by_css_selector("button.btn.btn-primary").click()
    time.sleep(.5)
    driver.find_element_by_css_selector("button.btn.btn-primary").click()
    driver.close()
    
    
    

if __name__ == '__main__':
    main()