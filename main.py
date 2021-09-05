import pandas as pd
import os
import sys


def main():
    menu() #call interactive menu method

def menu(): #interactive menu method
    print('### PERSONAL BUDGET ###')
    print('Welcome to your personal budget program')
    choice=input("""   
    1. RECORD A TRANSACTION
    2. CALCULATE THE CURRENT BUDGET
    3. EXIT
    
    Please type an option:
    """)
    if choice.isdigit(): #verify if the option typed is a positive integer number
        int_choice = int(choice)
    else:
        print('Your choice must be an integer number')
        print('Returning to the home menu...')
        print()
        menu()
    os.system('cls' if os.name == 'nt' else 'clear') #clean the screen

    if int_choice == 1: # option to record a transaction
        print('### PERSONAL BUDGET ###')
        record = input("""
        1. RECORD SINGLE TRANSACTION
        2. RECORD MULTIPLE TRANSACTION
        3. BACK
        """)
        int_record = 0 # assign int_record var to avoid UnboundLocalError
        if record.isdigit():  # verify if the option typed is a positive integer number
            int_record = int(record)
        else:
            print('Your choice must be an integer number')
            print('Returning to the home menu...')
            print()
            menu()
        os.system('cls' if os.name == 'nt' else 'clear')
        if int_record == 1:
            description = input('Insert the description:')
            #TODO: VALIDATE DATE INPUT
            date = input('Insert the date of the transaction (e.g.: 25/04/2021):')
            while True:
                try:
                    amount = input('Insert the amount of a transaction:')
                    amount = float(amount)
                    break
                except ValueError:
                    print("Amount invalid number")
            record_single_transaction(description, date, amount)
            menu()
        elif int_record == 2:
            print('### PERSONAL BUDGET ###')
            n = input("Enter the number of transactions: ")
            if n.isdigit():
                n = int(n)
                if n<2:
                    print()
                    print('Your choice must be an integer number greater than 1')
                    print('Returning to the home menu...')
                    print()
                    menu()
            else:
                n = 0  # assign n var to avoid TypeError
                print()
                print('Your choice must be an integer number')
                print('Returning to the home menu...')
                print()
                menu()
            d = {} #create a dictionary to store the entry of transactions
            for i in range(1, n+1): #loop the number of transactions chosen by the user
                transaction_header = f'description{i},date{i},amount{i}'
                keys = tuple(transaction_header.split(',')) #split the titles, convert to tuple and save as the dict keys
                values = list(map(str,input(
                    f"Transaction {i} - enter a description, date and amount separated by comma (e.g.: wage,25/04/2021,4000): "
                ).split(','))) #save the input as map and convert it to a list
                #TODO: VALIDATE DATE AND AMOUNT INPUT VALUES TYPE
                d[keys] = values #insert the keys and values into the dict
                if len(values) != 3:
                    print('Please, fill the 3 fields - description, date and amount separated following the e.g. pattern: wage,25/04/2021,4000')
                    print('Returning to the home menu...')
                    print()
                    menu()
            record_multiple_transactions(d) #BONUS: method where the user is able to insert multiple transactions at once
            menu()
        elif int_record == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            menu()
        else:
            print('You should select either 1, 2 or 3')
            print('Returning to the home menu...')
            menu()

    elif int_choice == 2: # option calculate the current budget && retrieve transactions
        print('### PERSONAL BUDGET ###')
        retrieve = input("""
                1. RETURN CURRENT BUDGET AND RETRIEVE LAST 10 TRANSACTIONS
                2. CHOOSE NUMBER OF TRANSACTIONS TO RETRIEVE
                3. CHOOSE DATE RANGE OF TRANSACTIONS TO RETRIEVE
                4. BACK 
                """)
        int_retrieve = 0  # assign int_retrieve var to avoid UnboundLocalError
        if retrieve.isdigit():  # verify if the option typed is a positive integer number
            int_retrieve = int(retrieve)
        else:
            print('Your choice must be an integer number')
            print('Returning to the home menu...')
            print()
            menu()
        os.system('cls' if os.name == 'nt' else 'clear')
        if int_retrieve == 1:
            return_current_budget() #method where the program returns the current budget and the last 10 transactions
            menu()
        elif int_retrieve == 2:
            print('### PERSONAL BUDGET ###')
            n = input("Enter the number of transactions: ")
            if n.isdigit():
                n = int(n)
                if n < 1:
                    print()
                    print(
                        'Your choice must be an integer number greater than 0')
                    print('Returning to the home menu...')
                    print()
                    menu()
            else:
                n = None  # assign n var to avoid TypeError
                print()
                print('Your choice must be an integer number')
                print('Returning to the home menu...')
                print()
                menu()
            retrieve_many_transactions(n) # method where user can specify how many transactions the program should return
            menu()
        elif int_retrieve == 3: #TODO: BONUS - The user can specify a date range for the transactions to be returned (e.g. all transactions in January 2021)
            print('BONUS feature: under construction')
            print()
            menu()
        elif int_retrieve == 4:
            os.system('cls' if os.name == 'nt' else 'clear')
            menu()
        else:
            print('You should select either 1, 2 or 3')
            print('Returning to the home menu...')
            print()
            os.system('cls' if os.name == 'nt' else 'clear')
            menu()

    elif int_choice == 3: #option exit the program
        sys.exit
    else:
        print('You should select either 1 or 2')
        print('Please try again')
        print()
        menu()

"""The program returns the current budget and the last 10 transactions"""
def return_current_budget():
    total = 0
    df = pd.read_excel('my_budget.xlsx', sheet_name='budget', dtype=str)
    for row in df.itertuples():
        if isinstance(row.amount, str):
            total +=  float(row.amount)
        else: total += row.amount
    print('Your last 10 transactions:')
    print(df.tail(10))
    print()
    print(f'Your current budget is: {total}')
    print('Returning to the home menu...')
    print()

"""The program should ask the user to insert the description, the date and the 
amount of a transaction (positive for income, negative for expenses)"""
def record_single_transaction(description, date, amount):
    total = 0
    df = pd.read_excel('my_budget.xlsx', sheet_name='budget', dtype=str)
    df2 = pd.DataFrame(
        {
            'description': [description],
            'date': [date],
            'amount': [amount]
        })
    df3 = df.append(df2)
    df3.to_excel('my_budget.xlsx', sheet_name='budget', index=False)
    for row in df3.itertuples():
        if isinstance(row.amount, str):
            total +=  float(row.amount)
        else: total += row.amount
    print()
    print('Transaction saved to file!')
    print(f'And your current budget is: {total}')
    print('Returning to the home menu...')
    print()

"""BONUS - The user is able to insert multiple transactions at once"""
def record_multiple_transactions(d):
    df = pd.read_excel('my_budget.xlsx', sheet_name='budget', dtype=str)
    for value in d.values(): #iterating through dict values
        df2 = pd.DataFrame(
            {
                'description': [value[0]],
                'date': [value[1]],
                'amount': [value[2]]
            })
        df = df.append(df2, ignore_index=True)
        df.to_excel('my_budget.xlsx', sheet_name='budget', index=False)
    print()
    print('Multiple transactions saved to file!')
    print('Returning to the home menu...')
    print()

"""BONUS - The user can specify how many transactions the program should return"""
def retrieve_many_transactions(n): #method to retrieve 'n' number of transactions
    df = pd.read_excel('my_budget.xlsx', sheet_name='budget', dtype=str)
    if n is not None:
        print(f'Your last {n} transaction(s):')
        print(df.tail(n))
        print()
        print('Returning to the home menu...')
        print()

if __name__ == '__main__':
    main()