import Pyro4
import pyodbc

#Set SA1 Connection Details
# PORT = 51515
# SERVER = "localhost"
PORT = int(input("Enter SA1 port number (#####): "))
SERVER = input("Enter SA1 server IP address or localhost: ")
uri = "PYRO:taxCalc@"+SERVER+":"+str(PORT)
taxCalc=Pyro4.Proxy(uri)

def splashScreen():
    print("-------------------------------------")
    print("     == PITRE ==         ")
    print("   Tax Return Estimator  ")
    print("-------------------------------------")
    print("")

def checkTFN():
    while True:
        selection = input("Do you have a Tax File Number (TFN)? (y/n): ").lower()
        if selection == "y":
            return True
        elif selection == "n":
            return False

def checkHealthCover():
    while True:
        selection = input("Do you have private health insurance? (y/n): ").lower()
        if selection == "y":
            return True
        elif selection == "n":
            return False
        
# define a main function
def main():
    splashScreen()
    tfn_status = checkTFN()
    if tfn_status == True:
        person_id = input("Enter your Person ID: ")
        tfn = int(input("Enter your TFN: "))
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        PHIC = checkHealthCover()
        tax_return_estimate, tax_owed, total_tax_witheld, gross_pay, net_income = taxCalc.db_tax_return_estimate(tfn, PHIC)

    
    elif tfn_status == False:
        person_id = input("Enter your Person ID: ")
        n = int(input("Enter the number of pay slips you have: "))
        wages = []
        for i in range(0, n):
            wage = input("Enter your bi-weekly net wages and corresponding tax witheld for each in the form (net_wage, tax_witheld): ")
            wage = wage.split(",")
            income = float(wage[0]) 
            tax = float(wage[1])
            set = (income, tax)
            wages.append(set)
        print(wages)
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        PHIC = checkHealthCover()
        tax_return_estimate, tax_owed, total_tax_witheld, gross_pay, net_income = taxCalc.tax_from_payroll(wages, PHIC)

    print(f"\n\n",
        f"Given Name: {first_name} \n", 
        f"Surname: {last_name} \n",
        f"Taxable Income: {gross_pay} \n",
        f"Tax Witheld: {total_tax_witheld} \n",
        f"Net Income: {net_income} \n",
        f"Tax Return Estimate: {tax_return_estimate} \n",
        f"\n\n" )
    
    input('Press ENTER to continue... \n')


while __name__ == "__main__":
    main()