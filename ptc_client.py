import Pyro4
import pyodbc

#Set SA1 Connection Details
# PORT = 51515
# SERVER = "192.168.0.105"
PORT = int(input("Enter SA1 port number (#####): "))
SERVER = input("Enter SA1 server IP address or localhost: ")

uri = "PYRO:taxCalc@"+SERVER+":"+str(PORT)
taxCalc=Pyro4.Proxy(uri)

def splashScreen():
    print("-------------------------------------")
    print("     == PCT ==         ")
    print("   Payroll Tax Client  ")
    print("-------------------------------------")
    print("")

def checkTFN():
    while True:
        selection = input("Does the employee have a Tax File Number (TFN)? (y/n): ").lower()
        if selection == "y":
            return True
        elif selection == "n":
            return False
        
def checkHealthCover():
    while True:
        selection = input("Does the employee have private health insurance? (y/n): ").lower()
        if selection == "y":
            return True
        elif selection == "n":
            return False

# define a main function
def main():
    splashScreen()
    mode = int(input("Do you follow weekly or bi-weekly wage structures? (1/2): "))
    if mode == 1:
        #enter employee info
        w = 52
    elif mode == 2:
        #enter employee info
        w = 26

    print('Enter employee info-------------------')
    tfn = int(input("Enter employee TFN: "))
    person_id = int(input("Enter employee Person ID: "))
    first_name = input("Enter employee first name: ")
    last_name = input("Enter employee last name: ")
    email = input("Enter employee email: ")
    date = input("Enter salary pay date: (YYYY-MM-DD): ")
    gross_pay = float(input("Enter employee gross pay: "))
    PHIC = checkHealthCover()
    tax_witheld = (taxCalc.income_tax(gross_pay*w))/w
    net_pay = gross_pay - tax_witheld
    print('--------------------------------------')
    
    if tax_witheld < gross_pay:
        print(
            f"Given Name: {first_name} \n", 
            f"Surname: {last_name} \n",
            f"Taxable Income: {gross_pay} \n",
            f"Tax Owed: {tax_witheld} \n",
            f"Net Income: {net_pay}\n")
    else:
        print("ERROR: Tax greater than income")

    print("Adding record to database...")
    record_update = taxCalc.add_record(tfn, date, gross_pay,  net_pay, tax_witheld)
    print('RECORD CHECK: ', record_update)

    input('Press ENTER to continue... \n')



while __name__ == "__main__":
    main()