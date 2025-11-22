import time
import os
import pickle


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print(Colors.CYAN + "=" * 50)
    print(f"{'🏦  PYTHON BANKING SYSTEM  🏦':^50}") 
    print("=" * 50 + Colors.RESET)
    print(f"\n{Colors.BOLD}>>> {title.upper()} <<<{Colors.RESET}\n")

def typewriter_print(text, delay=0.03):
    """Prints text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_valid_number(prompt):
    while True:
        value = input(prompt)
        clean_value = value.replace('$', '').strip()
        try:
            return float(clean_value)
        except ValueError:
            print(Colors.FAIL + "⚠ Invalid input. Please enter a number." + Colors.RESET)

class bank_account:


    def __init__(self,acc_holder,amount,acc_number):
        self.acc_holder = acc_holder
        self.balance = amount
        self.acc_number= acc_number
        self.transactions = []
    
           
    def deposit(self,amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append({
    "type": "deposit",
    "amount": amount,
    "final_balance": self.balance
})

            typewriter_print("---Deposit Successful!---")
            
            print(f"{self.acc_holder} deposited ${amount} in {self.acc_number}. New balance is ${self.balance}")
        else :
            print("Money can't be negative")
    
    def withdraw(self,amount):
        if amount > 0:
            if amount > self.balance:
                print(f"Insufficient balance!,you tried to withdraw ${amount} but your balance is ${self.balance}")
            else:
                self.balance -= amount
                self.transactions.append({
    "type": "withdraw",
    "amount": amount,
    "final_balance": self.balance
})

                typewriter_print("---Withdrawal Successful!---")
                print(f"{self.acc_holder} withdraw ${amount} from {self.acc_number}. New balance is ${self.balance}")

    def get_balance(self):
        print(f"Your balance in {self.acc_number} is ${self.balance}")

    def __str__(self):
        return f"Account holder : {self.acc_holder},Balance : ${self.balance:.2f}"
    
    def __repr__(self):
        return f"bank_account('{self.acc_holder}', {self.balance} , '{self.acc_number}')"
    
    def __eq__(self, other):
        return self.balance == other.balance

    def __gt__(self,other):
        return self.balance > other.balance
    
    def __lt__(self,other):
        return self.balance < other.balance

    def __add__(self,other):
        if not isinstance(other,bank_account):
            return NotImplemented
        
        new_holder = f"{self.acc_holder} & {other.acc_holder}"
        joint_number = "joint-007"
        new_balance = round(self.balance + other.balance, 2)
        return bank_account(new_holder,new_balance,joint_number)

    @classmethod
    def savings_account(cls,holder,number):
        saving_holder = holder
        saving_number = number
        saving_balance = 1000
        return cls(saving_holder,saving_balance,saving_number)
    
    @classmethod
    def checking_account(cls,holder,number):
        checking_holder = holder
        checking_number = number
        checking_balance = 500
        return cls(checking_holder,checking_balance,checking_number)
    
class Savings_Account(bank_account):

    def __init__(self,holder,amount,number,interest=3.0):
       
        super().__init__(holder,amount,number)
        self.interest = interest
        self.withdraw_limit = 1000
        

    def withdraw(self,amount):

        if amount > 1000:
            print("Withdrawal Limit for Savings reached, Can withdraw only till $1000/Transcation")
            return
        else:
            super().withdraw(amount)

    def apply_interest(self):

        interest_amount = self.balance * (self.interest/100)
        self.balance += interest_amount
        self.transactions.append({
    "type": "interest",
    "amount": interest_amount,
    "final_balance": self.balance
})


        return f"Added ${interest_amount}. New Balance ${self.balance}"
    

    def __str__(self):

        super().__str__()

        return f"Account holder : {self.acc_holder}, Balance : ${self.balance:.2f}, Interest_rate : {self.interest}"
    

class Checking_Account(bank_account) :

     def __init__(self,holder,amount,number, overdraft_limit=500):
         
         super().__init__(holder,amount,number)
         self.overdraft = overdraft_limit

     def withdraw(self,amount):
         
         available_amount = self.balance + self.overdraft

         if available_amount >= amount :
            self.balance -= amount
            self.transactions.append({
    "type": "withdraw",
    "amount": amount,
    "final_balance": self.balance
})

            typewriter_print("---Withdrawal Successful!---")
            print(f"{self.acc_holder} withdraw ${amount} from {self.acc_number}. New balance is ${self.balance}")

            return self.balance

         else :
              print(f"Insufficient balance!,you tried to withdraw ${amount} but your limit balance is ${available_amount}")


     def __str__(self):
         
         super().__str__()
         

         if int(self.balance) > 0 :
             return f"Account holder : {self.acc_holder}, Balance : ${self.balance:.2f}, Overdraft Limit : {self.overdraft}"
         
         else :
             
             overdraft_used = self.balance * -1
    
             return f"Account holder : {self.acc_holder}, Balance : ${self.balance:.2f}, Overdraft Used : {overdraft_used}/500.00"
             



exsisting_account = []
def create_account(account):
  print_header("Create New Account")
  
  if account == "1":
      holder = input("Enter Holder Name: ")
      balance = get_valid_number("Enter Initial Balance: ")
      number = input("Enter Account Number: ")
      acc = bank_account(holder,balance,number)
      exsisting_account.append(acc)
      print("✓ Account created successfully!")
      save_data()
      print(acc)
      typewriter_print("Press Enter to continue...", delay=0.05)
      input()
      
  elif account == "2":
      holder = input("Enter Holder Name: ")
      balance = get_valid_number("Enter Initial Balance: ")
      number = input("Enter Account Number: ")
      interest = input("Enter Interest or press enter for default (3.0): ")
      interest = float(interest) if interest.strip() else 3.0

      if interest < 0:
          print("Interest can't be negative")
          return
      acc = Savings_Account(holder,balance,number,interest)
      exsisting_account.append(acc)
      print("✓ Account created successfully!")
      save_data()
      print(acc)
      typewriter_print("Press Enter to continue...", delay=0.05)
      input()
      
  elif account == "3":
        holder = input("Enter Holder Name: ")
        balance = get_valid_number("Enter Initial Balance: ")
        number = input("Enter Account Number: ")
        overdraft = input("Enter Overdraft or press enter for default (500): ")
        overdraft = float(overdraft) if overdraft.strip() else 500

        if overdraft < 0:
          print("Overdraft can't be negative")
          return
        acc = Checking_Account(holder,balance,number,overdraft)
        exsisting_account.append(acc)
        print("✓ Account created successfully!")
        save_data()
        print(acc)
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
      
  else :
      print("Invalid Input! Please Select from the above options")
      


def view_accounts():
    print_header("All Accounts")

    if not exsisting_account:
        print("No Account Created Yet")
        print("'Create an Account first'")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return

    print("-----Saved Accounts-----")
    print(f"No of Accounts Exist: {len(exsisting_account)}")

    total_money = sum(acc.balance for acc in exsisting_account)
    print(f"Total Money in system: ${total_money:.2f}\n")

    for i, acc in enumerate(exsisting_account, start=1):
        print(f"{i}. {acc}  (Type: {type(acc).__name__})")
    
    typewriter_print("\nPress Enter to continue...", delay=0.05)
    input()
       



def deposit():
       
       print_header("Deposit Money")
       
       if not exsisting_account:
        print("No Account Created Yet")
        print("'Create an Account first'")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
       
       print("\n-----Select Account to Deposit-----\n")
       print("0. Cancel")
       for i, acc in enumerate(exsisting_account, start=1):
            print(f"{i}. {acc}  (Type: {type(acc).__name__})")

       print(f"\nSelect Account from 1 - {len(exsisting_account)}: ")
       select = int(input())
       if select == 0 :
           print("Deposit Cancelled")
           typewriter_print("Press Enter to continue...", delay=0.05)
           input()
           return
       
       if 1 <= select <= len(exsisting_account) :
           selected_account = exsisting_account[select - 1]
           print(f"\n-----Selected Account-----\n{selected_account}")
           amount = get_valid_number("\nEnter amount to Deposit: ")
           typewriter_print("\nProcessing Deposit...", delay=0.03)
           time.sleep(0.5)
           selected_account.deposit(amount)
           save_data()
           typewriter_print("\nPress Enter to continue...", delay=0.05)
           input()
           
       else :
           print("Invalid Account, Please select a valid Account")
           typewriter_print("Press Enter to continue...", delay=0.05)
           input()
    
def withdraw():
      print_header("Withdraw Money")
      
      if not exsisting_account:
        print("No Account Created Yet")
        print("'Create an Account first'")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
      
      print("\n-----Select Account to Withdraw-----\n")
      print("0. Cancel")
      for i, acc in enumerate(exsisting_account, start=1):
        print(f"{i}. {acc}  (Type: {type(acc).__name__})")

      print(f"\nSelect Account from 1 - {len(exsisting_account)}: ")
      select = int(input())
      if select == 0 :
        print("Withdrawal Cancelled")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
      if 1 <= select <= len(exsisting_account) :
           selected_account = exsisting_account[select - 1]
           print(f"\n-----Selected Account-----\n{selected_account}\n")

           if isinstance(selected_account, Savings_Account):
               print("⚠ Note: Savings accounts have $1000 withdrawal limit per transaction")
           elif isinstance(selected_account, Checking_Account):
               available_funds = selected_account.balance + selected_account.overdraft 
               print(f"Available Funds (including overdraft ${selected_account.overdraft}): ${available_funds:.2f}")
           else :
               print(f"Available Funds: ${selected_account.balance:.2f}")

           amount = get_valid_number("\nEnter amount to Withdraw: ")
           typewriter_print("\nProcessing Withdrawal...", delay=0.03)
           time.sleep(0.5)
           selected_account.withdraw(amount)
           save_data()
           typewriter_print("\nPress Enter to continue...", delay=0.05)
           input()
      else :
           print("Invalid Account, Please select a valid Account")
           typewriter_print("Press Enter to continue...", delay=0.05)
           input()

def compare_accounts():
    print_header("Compare Accounts")

    if len(exsisting_account) < 2 :
        print(f"Need at least 2 accounts to compare, but saved Accounts are only {len(exsisting_account)}")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    else :
        print("-----COMPARE ACCOUNTS-----\n")
        for i, acc in enumerate(exsisting_account, start=1):
            print(f"{i}. {acc}  (Type: {type(acc).__name__})")
        print(f"\nSelect Account from 1 - {len(exsisting_account)}: ")

        select_1 = int(input("Enter First account to compare: "))
        account_1 = exsisting_account[select_1 - 1]
        print(f"✓ Selected: {account_1}")

        select_2 = int(input("Enter Second account to compare: "))
        if select_2 == select_1:
            print("✗ Error: Cannot compare account with itself!")
            typewriter_print("Press Enter to continue...", delay=0.05)
            input()
            return
        else :
            account_2 = exsisting_account[select_2 - 1]
            print(f"✓ Selected: {account_2}")

        typewriter_print("\nComparing Accounts...", delay=0.02)
        time.sleep(0.3)

        print("\n-----COMPARISON TEST-----")
        bal1 = account_1.balance
        bal2 = account_2.balance
        name1 = account_1.acc_holder
        name2 = account_2.acc_holder

        print("├─ Equal Balance (==)?")
        if account_1 == account_2 :
            print(f"│  ✓ YES - Both have ${bal1:.2f}")
        else:
            print(f"│  ✗ NO - Account 1: ${bal1:.2f}, Account 2: ${bal2:.2f}")

        print(f"├─ {name1} > {name2}?")
        if account_1 > account_2:
            print(f"│  ✓ YES - ${bal1:.2f} > ${bal2:.2f}")
        else:
            print(f"│  ✗ NO - ${bal1:.2f} ≤ ${bal2:.2f}")

        print(f"├─ {name1} < {name2}?")
        if account_1 < account_2:
            print(f"│  ✓ YES - ${bal1:.2f} < ${bal2:.2f}")
        else:
            print(f"│  ✗ NO - ${bal1:.2f} ≥ ${bal2:.2f}")

        print("├─ Balance Comparison:")
        print(f"│  Balance ({name1}): ${account_1.balance:.2f}")
        print(f"│  Balance ({name2}): ${account_2.balance:.2f}")
        
        difference = abs(bal1 - bal2)
        print(f"└─ Balance Difference: ${difference:.2f}")

        print("\n-----Summary-----")
        if bal1 == bal2:
            print("→ These accounts have equal balances")
        elif bal1 > bal2:
            print(f"→ {name1} has ${difference:.2f} more than {name2}")
        else:
            print(f"→ {name2} has ${difference:.2f} more than {name1}")

        type1 = type(account_1).__name__
        type2 = type(account_2).__name__

        if type1 == type2:
            print(f"→ Both are {type1} accounts")
        else:
            print(f"→ Different account types: {type1} vs {type2}")

    typewriter_print("\nPress Enter to continue...", delay=0.05)
    input()

def apply_interest():
    print_header("Apply Interest")
    
    Savings_accounts = []
    savings_indices = []

    for i, acc in enumerate(exsisting_account):
        if isinstance(acc, Savings_Account):
            Savings_accounts.append(acc)
            savings_indices.append(i)

    if len(Savings_accounts) == 0:
        print("⚠ No savings accounts found!")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    
    print("-----Apply Interest-----\n")
    print("0. Cancel")
    for i, acc in enumerate(Savings_accounts, 1):
        print(f"{i}. {acc}  (Type: {type(acc).__name__})")

    choice = int(input(f"\nSelect Savings Account 1 - {len(Savings_accounts)}: "))
    if choice == 0:
        print("Cancelled")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    
    selected_account = Savings_accounts[choice - 1]
    interest_amount = selected_account.balance * (selected_account.interest / 100)
    new_balance = selected_account.balance + interest_amount
    
    print("\n-----Interest Calculation-----")
    print(f"├─ Principal: ${selected_account.balance:.2f}")
    print(f"├─ Interest Rate: {selected_account.interest}%")
    print(f"├─ Interest Earned: ${interest_amount:.2f}")
    print(f"└─ New Balance: ${new_balance:.2f}")

    print("\nApply this interest? (Yes/No): ")
    cho = input()
    cho = cho.strip().lower()
    if cho not in ('yes', 'y'):
        print("Interest not applied.")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    
    typewriter_print("\nApplying interest...", delay=0.03)
    time.sleep(0.5)
    result = selected_account.apply_interest()
    save_data()
    typewriter_print("✓ Interest applied successfully!", delay=0.03)
    typewriter_print("Press Enter to continue...", delay=0.05)
    input()


def Account_details():
    print_header("Account Details")
    
    if not exsisting_account:
        print("No accounts found!")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    
    print("-----Select Account to View Details-----\n")
    for i,acc in enumerate(exsisting_account,1):
        print(f"{i}. {acc}  (Type: {type(acc).__name__})")

    choice = int(input(f"\nSelect Account 1 - {len(exsisting_account)}: "))
    if choice == 0:
        print("Cancelled")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    
    selected_account = exsisting_account[choice - 1]
    
    typewriter_print("\nLoading Account Details...", delay=0.02)
    time.sleep(0.3)
    
    print("\n-----String Representation-----")
    print(selected_account)
    print()
    print("-----Developer Representation-----")
    print(repr(selected_account))
    print()
    print("-----Account Balance-----")
    print(f"Account Balance: ${selected_account.balance:.2f}")
    print()
    print("-----Full Details-----")
    print(f"├─ Account Holder: [{selected_account.acc_holder}]")
    print(f"├─ Account Number: [{selected_account.acc_number}]")
    print(f"├─ Account Type: [{type(selected_account).__name__}]")
    print(f"└─ Current Balance: ${selected_account.balance:.2f}")
    print()
    print("-----Special Attributes-----")
    
    if isinstance(selected_account, Savings_Account):
        print(f"Special Attribute - Interest: [{selected_account.interest}%]")
        interest_amount = selected_account.balance * ((selected_account.interest) / 100)
        print(f"Expected Annual Interest: [${interest_amount:.2f}]")
        print("Note: This is according to your current balance")
        print("Your Limit per transaction is $1000.00")
    elif isinstance(selected_account, Checking_Account):
        print(f"Special Attribute - Overdraft: [${selected_account.overdraft}]")
        balance_available = selected_account.balance + selected_account.overdraft
        print(f"Available Balance (Including overdraft): [${balance_available:.2f}]")
        if selected_account.balance < 0:
            used = -1 * selected_account.balance
            print(f"Overdraft Used: [${used:.2f}]")
    else:
        print("No special attributes")

    print("\n-----Transaction History-----")
    if not selected_account.transactions:
        print("No transactions yet.")
    else:
        for t in selected_account.transactions:
            print(f"• {t['type'].title()}: ${t['amount']:.2f} → Balance: ${t['final_balance']:.2f}")

    print("\n-----Recommendations-----")
    if isinstance(selected_account, Savings_Account):
        print("Consider depositing to maximize interest earnings")
    elif isinstance(selected_account, Checking_Account):
        if selected_account.balance < 0:
            print('⚠ Account in overdraft! Deposit soon to avoid fees')

    typewriter_print("\nPress Enter to continue...", delay=0.05)
    input()


def delete_account():
    print_header("Delete Account")
     
    if not exsisting_account:
        print("No accounts found!")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
     
    print("⚠ WARNING: This action cannot be undone!\n")

    for i,acc in enumerate(exsisting_account,1):
        print(f"{i}. {acc}  (Type: {type(acc).__name__})")
    print("0. Cancel")

    choice = int(input(f"\nSelect Account 1 - {len(exsisting_account)}: "))
    if choice == 0:
        print("Cancelled")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    selected_account = exsisting_account[choice - 1]
    print("\n-----Full Details-----")
    print(f"├─ Account Holder: [{selected_account.acc_holder}]")
    print(f"├─ Account Number: [{selected_account.acc_number}]")
    print(f"├─ Account Type: [{type(selected_account).__name__}]")
    print(f"└─ Current Balance: ${selected_account.balance:.2f}")

    print("\nAre you sure you want to delete this Account? (yes/no): ")
    cho = input()
    cho = cho.strip().lower()
    if cho not in ('yes', 'y'):
        print("Deletion Cancelled")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
     
    de = input("Type 'Delete' to confirm: ")
    de = de.strip().lower()
    if de == 'delete':
        typewriter_print("\nProcessing Deletion...", delay=0.03)
        time.sleep(0.5)
        exsisting_account.remove(selected_account)
        save_data()
        print("✓ Account deleted successfully!")
        print(f"Current Saved Accounts: {len(exsisting_account)}")
        typewriter_print("\nPress Enter to continue...", delay=0.05)
        input()
        return
    else :
        print("Deletion Cancelled")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()


def banking_statistics():
    print_header("Banking Statistics")

    if not exsisting_account:
        print("No accounts found!")
        return
     
    print("-----System Overview-----")
    regular_count = 0
    savings_count = 0
    checking_count = 0
    for i,acc in enumerate(exsisting_account,1):
        if isinstance(acc,Savings_Account):
            savings_count += 1
        elif isinstance(acc,Checking_Account):
            checking_count += 1
        else :
            regular_count += 1

    print(f"├─ Total Account: [{len(exsisting_account)}]")
    print(f"├─ Regular Accounts: [{regular_count}]")
    print(f"├─ Savings Accounts: [{savings_count}]")
    print(f"└─ Checking Accounts: [{checking_count}]")

    total_money = 0
    positive_acc = 0
    negative_acc = 0

    for i,acc in enumerate(exsisting_account,1):
        total_money += acc.balance

        if acc.balance >= 0:
            positive_acc += 1
        else :
            negative_acc += 1
     
    print(f"\n├─ Total Money in System: ${total_money:.2f}")
    print(f"├─ Average Balance: ${total_money/len(exsisting_account):.2f}")
    print(f"├─ Accounts in Credit: [{positive_acc}]")
    print(f"└─ Accounts in Debt: [{negative_acc}]")

    print("\n-----Richest Account-----")
    richest = exsisting_account[0]
    for acc in exsisting_account:
        if acc > richest:     # uses __gt__
            richest = acc

    print(f"Richest Account: {richest.acc_holder} with ${richest.balance:.2f}")


    print("\n-----Poorest Account-----")
    poorest = exsisting_account[0]
    for acc in exsisting_account:
        if acc < poorest:     # uses __lt__
            poorest = acc

    print(f"Poorest Account: {poorest.acc_holder} with ${poorest.balance:.2f}")

    print("\n-----Account Rankings (By Balance)-----")
    ranked = sorted(exsisting_account, key=lambda x: x.balance, reverse=True)

    medals = ["🥇", "🥈", "🥉"]

    for i, acc in enumerate(ranked, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        print(f"{medal} {acc.acc_holder} - ${acc.balance:.2f}")


    print("\n-----Accounts in Overdraft/Negative balance-----")
    overdraft_accounts = [acc for acc in exsisting_account if acc.balance < 0]

    if not overdraft_accounts:
        print("→ No accounts in overdraft")
    else:
        for acc in overdraft_accounts:
            used = -acc.balance
            print(f"{acc.acc_holder} ({acc.acc_number}) | Balance: ${acc.balance:.2f} | Overdraft Used: ${used:.2f}")


    
    print("\n-----Interest-Earning Accounts-----")
    savings_list = [acc for acc in exsisting_account if isinstance(acc, Savings_Account)]

    if not savings_list:
        print("→ No savings accounts")
    else:
        for acc in savings_list:
            yearly = acc.balance * (acc.interest / 100)
            print(f"{acc.acc_holder}: {acc.interest}% → Earning ${yearly:.2f}/year")

    print("\n-----Comparison Tests-----")
    found_equal = False

    for i in range(len(exsisting_account)):
        for j in range(i + 1, len(exsisting_account)):
            if exsisting_account[i] == exsisting_account[j]:  # uses __eq__
                acc1 = exsisting_account[i]
                acc2 = exsisting_account[j]
                print(f"Accounts with Equal Balances: {acc1.acc_holder} and {acc2.acc_holder}")
                found_equal = True

    if not found_equal:
        print("No accounts have equal balances")


    print("\n-----Total System Value-----")
    total_acc = exsisting_account[0]
    for acc in exsisting_account[1:]:
        total_acc = total_acc + acc   # uses __add__

    print(f"Total Balance in System: ${total_acc.balance:.2f}")


    print("\n-----Balance Distribution-----")

    under_100 = sum(1 for acc in exsisting_account if acc.balance < 100)
    b100_1000 = sum(1 for acc in exsisting_account if 100 <= acc.balance < 1000)
    b1000_5000 = sum(1 for acc in exsisting_account if 1000 <= acc.balance < 5000)
    over_5000 = sum(1 for acc in exsisting_account if acc.balance >= 5000)

    print(f"Under $100:     {under_100} accounts")
    print(f"$100-$1000:     {b100_1000} accounts")
    print(f"$1000-$5000:    {b1000_5000} accounts")
    print(f"Over $5000:     {over_5000} accounts")


    avg_balance = sum(acc.balance for acc in exsisting_account) / len(exsisting_account)

    if avg_balance < 500:
        print("\n-----Recommendations-----")
        print("💡 Tip: Average balance is low — encourage saving more.")

    if overdraft_accounts:
        print("\n-----Recommendations-----")
        print("⚠ High overdraft usage detected.")

    if not savings_list:
        print("\n-----Recommendations-----")
        print("Use savings accounts for more benefits.")

    typewriter_print("\nPress Enter to continue...", delay=0.05)
    input()


def merge_account():
    print_header("Merge Accounts")
    
    if len(exsisting_account) < 2:
        print("Need at least 2 accounts to merge")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    
    print("-----TRANSFER/MERGE ACCOUNTS-----\n")

    for i, acc in enumerate(exsisting_account, 1):
        print(f"{i}. {acc}  (Type: {type(acc).__name__})")

    print("0. Cancel")
    print(f"\nSelect Account from 1 - {len(exsisting_account)}: ")

    try:
        select_1 = int(input("Enter First account to merge: "))
    except ValueError:
        print("Invalid input.")
        return
    if select_1 == 0:
        print("Cancelled")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    account_1 = exsisting_account[select_1 - 1]
    print(f"✓ Selected: {account_1}")

    try:
        select_2 = int(input("Enter Second account to merge: "))
    except ValueError:
        print("Invalid input.")
        return
    if select_2 == select_1:
        print("✗ Error: Cannot merge account with itself!")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    else:
        account_2 = exsisting_account[select_2 - 1]
        print(f"✓ Selected: {account_2}")

    print("\n-----Merge Summary-----")
    print(f"├─ Account 1: [{account_1.acc_holder}] - ${account_1.balance:.2f}")
    print(f"└─ Account 2: [{account_2.acc_holder}] - ${account_2.balance:.2f}")

    combined = account_1.balance + account_2.balance
    print(f"\n├─ Combined Balance: ${combined:.2f}")
    print(f"├─ Primary Holder: [{account_1.acc_holder}]")
    print(f"└─ Account Type: Joint")

    print("\n⚠ Note: This will create a new joint account")
    print("You can choose to keep or delete original accounts")
    print("Proceed with merge? (Yes/No): ")
    cho = input()
    cho = cho.strip().lower()
    if cho not in ('yes', 'y'):
        print("Merge cancelled.")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    
    joint_account = account_1 + account_2
    
    typewriter_print("\nProcessing Merge...", delay=0.03)
    time.sleep(0.5)
    typewriter_print("✓ Accounts merged successfully!", delay=0.03)
    print(joint_account)

    print("\n-----What would you like to do?-----")
    print("1. Delete both original accounts")
    print("2. Keep both original accounts")
    print("3. Delete first account only")
    print("4. Delete second account only")
    print("5. Cancel (don't add joint account)\n")
    ca = input("Enter your choice: ")
    
    if ca == '1':
        exsisting_account.remove(account_1)
        exsisting_account.remove(account_2)
        exsisting_account.append(joint_account)
        save_data()
        print(f"✓ Deleted: {account_1.acc_holder}")
        print(f"✓ Deleted: {account_2.acc_holder}")
    elif ca == '2':
        exsisting_account.append(joint_account)
        save_data()
        print("✓ Kept both original accounts")
    elif ca == '3':
        exsisting_account.remove(account_1)
        exsisting_account.append(joint_account)
        save_data()
        print(f"✓ Deleted: {account_1.acc_holder}")
    elif ca == '4':
        exsisting_account.remove(account_2)
        exsisting_account.append(joint_account)
        save_data()
        print(f"✓ Deleted: {account_2.acc_holder}")
    elif ca == '5':
        print("Merge cancelled!")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return
    else:
        print("Invalid Choice")
        typewriter_print("Press Enter to continue...", delay=0.05)
        input()
        return

    print(f"\n✓ Total Accounts Now: [{len(exsisting_account)}]")

    typewriter_print("Press Enter to continue...", delay=0.05)
    input()
def save_data():
    """Saves the list of account objects to a binary file."""
    try:
        with open("bank_data.pkl", "wb") as f:
            pickle.dump(exsisting_account, f)
        
    except Exception as e:
        print(Colors.FAIL + f"Error saving data: {e}" + Colors.RESET)

def load_data():
    """Loads the list of account objects from the file."""
    global exsisting_account
    try:
        if os.path.exists("bank_data.pkl"):
            with open("bank_data.pkl", "rb") as f: 
                exsisting_account = pickle.load(f)
    except Exception as e:
        print(Colors.FAIL + f"Error loading data: {e}" + Colors.RESET)

def main():
    load_data()
    print("\n\n-----WELCOME TO PYTHON BANKING SYSTEM-----\n\n")

    while True:

        clear_screen()
        print(Colors.CYAN + """
    ╔═════════════════════════════════════════╗
    ║       🏦  PYTHON BANKING SYSTEM  🏦     ║
    ╚═════════════════════════════════════════╝
        """ + Colors.RESET)

        print("  1. 🆕 Create Account")
        print("  2. 📜 View All Accounts")
        print("  3. 💵 Deposit Money")
        print("  4. 💸 Withdraw Money")
        print("  5. 🤝 Merge Accounts")
        print("  6. ⚖️  Compare Accounts")
        print("  7. 📈 Apply Interest (Savings)")
        print("  8. 🔍 Account Details")
        print("  9. 🗑️  Delete Account")
        print("  10. 📊 Banking Statistics")
        print(Colors.FAIL + "  0. 🚪 Exit" + Colors.RESET)


        choice = input("\nEnter your choice: ")

        match choice:
            case "1":
                print("\n-----Select Account Type-----\n")
                print("1. Regular Account")
                print("2. Savings Account")
                print("3. Checking Account\n")
                account = input("Enter your choice: ")
                create_account(account)
                save_data()
            case "2":
                view_accounts()
            case "3":
                deposit()
                save_data()
            case "4":
                withdraw()
                save_data()
            case "5":
                merge_account()
            case "6":
                compare_accounts()
            case "7":
                apply_interest()
                save_data()
            case "8":
                Account_details()
            case "9":
                delete_account()
                save_data()
            case "10":
                banking_statistics()
            case "0":
                print()
                typewriter_print("Thank you for choosing us!", delay=0.05)
                save_data()
                break

            case _:
                print("Invalid choice!, please choose from the options above")

if __name__ == "__main__":
    main()