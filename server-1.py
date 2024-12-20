import pyodbc 
import Pyro4
import json



@Pyro4.expose
class tax_calc(object):
    def income_tax(self, income):
        print("Calculating income tax...")
        if income in range(0, 18201):
            tax = 0
        elif income in range(18201, 45001):
            over = income - 18200
            tax = over * 0.19
        elif income in range(45001, 120001):
            over = income - 45000
            tax = 5092 + (over * 0.325)
        elif income in range(120001, 180001):
            over = income - 120000
            tax = 29467 + (over * 0.37)
        elif income >= 180001:
            over = income - 180000
            tax = 51667 + (over * 0.45)
        return tax 

    def medicare_levy(self, income):
        print("Calculating medicare levy...")
        medicare_levy = income * 0.02
        return medicare_levy

    def medicare_levy_surcharge(self, income):
        print("Calculating medicare levy surcharge...")
        if income <= 90000:
            mls = 0
        elif income in range(90001, 105001):
            mls = income * 0.01
        elif income in range(105001, 140001):
            mls = income * 0.0125
        elif income >= 140001:
            mls = income * 0.015
        return mls
    
    def get_tax_owed(self, income, PHIC):
        print("Calculating tax owed...")
        if PHIC == True:
            tax_owed = self.income_tax(income) + self.medicare_levy(income)
        elif PHIC == False:
            tax_owed = self.income_tax(income) + self.medicare_levy(income) + self.medicare_levy_surcharge(income)
        return tax_owed
    
    def check_database(self, person_id):
        sa2Uri = "PYRO:taxDb@"+ SA2_SERVER + ":" + str(SA2_PORT)
        tax_database = Pyro4.Proxy(sa2Uri) 
        print("SERVER 2: ", tax_database)
        return tax_database.getUserDetails(person_id)
    
    def add_record(self, tfn, date, gross_pay,  net_pay, tax_witheld):
        sa2Uri = "PYRO:taxDb@"+ SA2_SERVER + ":" + str(SA2_PORT)
        tax_database = Pyro4.Proxy(sa2Uri) 
        print("SERVER 2: ", tax_database)
        if tax_database.addRecord(tfn, date, gross_pay,  net_pay, tax_witheld) == True:
            return "Payroll record added successfully."
        elif tax_database.addRecord(tfn, date, gross_pay,  net_pay, tax_witheld) == False:
            return "Failed to add payroll record"
    
    def db_tax_return_estimate(self, tfn, PHIC):
        sa2Uri = "PYRO:taxDb@"+ SA2_SERVER + ":" + str(SA2_PORT)
        tax_database = Pyro4.Proxy(sa2Uri) 
        print("SERVER 2: ", tax_database)
        payrolls = tax_database.getPayrollRecords(tfn)
        tax_witheld = 0
        tax_return = 0
        gross_pay = 0
        for i in payrolls:
            tax_witheld += i[3]
            gross_pay += i[1]
        tax_owed = self.get_tax_owed(gross_pay, PHIC)
        tax_return = tax_witheld - tax_owed
        net_income = gross_pay - tax_witheld
        return tax_return, tax_owed, tax_witheld, gross_pay, net_income
    
    def tax_from_payroll(self, wages, PHIC):
        gross_income = sum([pair[0] + pair[1] for pair in wages])  # Calculate gross income per pay period
        annual_gross_income = gross_income * len(wages) / 26  # Convert to annual income assuming bi-weekly pay
        tax_owed = self.get_tax_owed(annual_gross_income, PHIC)
        annual_net_income = annual_gross_income - tax_owed
        total_tax_withheld = sum([pair[1] for pair in wages])
        tax_return = total_tax_withheld - tax_owed
        return tax_return, tax_owed, total_tax_withheld, annual_gross_income, annual_net_income

            
            
        
# 51516
# localhost
# 51515
#Set SA2 Connection Details
SA2_PORT = int(input("Enter SA2 port number (#####): "))
SA2_SERVER = input("Enter SA2 server IP address or localhost: ")

#Set SA1 Serving Details
SA1_PORT = int(input("Enter SA1 port number (#####): "))
HOST = input("Enter SA1 server IP address or localhost: ")
tax_calc=tax_calc()
daemon=Pyro4.Daemon(host=HOST, port = SA1_PORT)                
uri=daemon.register(tax_calc, "taxCalc")

print("--------------------")
print(" Server 1: Interface")
print("--------------------")
print()
print("Ready. Object uri =", uri)
daemon.requestLoop()
