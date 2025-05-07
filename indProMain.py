from indProFunction import verify_user, calculate_tax, save_to_csv, file_read_from_csv
import os

def show_main_menu():
    print("\n^O^ ||     Malaysian Tax Calculator    || ^O^ ")           #content in menu
    print("(1) Register new user :D")
    print("(2) Login and calculate tax +/-")
    print("(3) View all tax records ^-^")
    print("(4) Exit program")
    while True:
        choice = input("Please choose (1-4): ")
        if choice in ("1", "2", "3", "4"):
            return choice
        print("Invalid choice. Please enter 1-4.")                      #make sure they choose only functions in menu

def get_ic_number():
    while True:
        ic = input("Please enter your IC number (12 digits): ").strip() #input to enter IC
        if len(ic) == 12 and ic.isdigit():                              #ensure length and number
            return ic
        print("IC is invalid! IC must be exactly 12 digits. :/")

def get_income():
    while True:
        try:
            income = float(input("Please enter your yearly income: RM")) #convert string into floating-point number, string can't be used for calculations
            if income >= 0:
                return income
            print("Income can't be negative!")
        except ValueError:
            print("Please enter a valid yearly income :D")

def get_tax_relief():
    total_relief = 9000.0
    print(f"\n//Personal relief auto-added: RM{total_relief}")              #automatically add personal relief

    spouse = input("\nDo you have a spouse? (y/n) :D : ").lower()     #ask for y/n and return is in lowercase always
    if spouse == 'y':
        while True:
            try:
                spouse_income = float(input("Please enter your spouse's income: RM "))
                if spouse_income <= 4000:
                    total_relief += 4000.0
                    print("Spouse relief +RM4,000")                  #if spouse has higher income than 4000, no relief
                break
            except ValueError:
                print("Please enter valid amount")

    while True:
        try:
            children = int(input("\nPlease enter your number of children (maximum no. of children = 12): "))
            if 0 <= children <= 12:
                total_relief += children * 8000
                print(f"//Child relief +RM{children * 8000}")
                break
            else:
                print("only maximum of 12 children allowed :D ")
        except ValueError:
            print("Please enter a number")

    def ask_relief(prompt, max_amount):
        while True:
            try:
                amount = float(input(prompt))
                relief_amount = min(amount, max_amount)             #compare actual ammount of expenses to maximum relief, and choose the min of both.
                print(f"//Relief +RM{relief_amount}")
                return relief_amount
            except ValueError:
                print("Please enter valid amount")

    total_relief += ask_relief("\nMedical expenses (RM): ", 8000)
    total_relief += ask_relief("Lifestyle expenses (RM): ", 2500)
    total_relief += ask_relief("Education fees (RM): ", 7000)
    total_relief += ask_relief("Parental care expenses (RM): ", 5000)

    print(f"\n//TOTAL RELIEF: RM{total_relief:,.2f}")                    #add commas to big numbers, make it 2 d.p.
    return total_relief

def main():
    print("||   Welcome to Malaysian Tax Calculator! :D   ||")
    filename = "data/indpro_tax_records.csv"
    os.makedirs("data", exist_ok=True)                              #create file and make sure it exist

    all_users = file_read_from_csv(filename) or []

    while True:
        user_choice = show_main_menu()

        if user_choice == "1":
            print("\n||   ~REGISTRATION~   ||")
            ic = get_ic_number().zfill(12)                          #make sure it stays as 12 charc when saved in CSV

            if any(user["IC Number"] == ic for user in all_users):
                print("This IC is already registered! :O ")
                continue

            password = ic[-4:].zfill(4)                             #make sure it stays as 4 charc when saved in CSV
            new_user = {
                "IC Number": ic,
                "Password": password,
                "Income": 0.0,
                "Tax Relief": 0.0,
                "Tax Payable": 0.0
            }
            all_users.append(new_user)
            save_to_csv(all_users, filename)
            print(f"Registered successfully! Your password is: {password}")

        elif user_choice == "2":
            print("\n||   ~LOGIN~   ||")
            ic = get_ic_number().zfill(12)
            password = input("Please enter your password (last 4 digits of your IC): ")

            if not verify_user(ic, password):
                print("UH OH! Wrong IC or password!")
                continue

            current_user = next((user for user in all_users if user["IC Number"] == ic), None)
            if not current_user:
                print("Hmm, user not found!")
                continue

            print("\nLogin successful!")
            income = get_income()
            relief = get_tax_relief()
            tax = calculate_tax(income, relief)

            current_user.update({
                "Income": income,
                "Tax Relief": relief,
                "Tax Payable": tax
            })
            save_to_csv(all_users, filename)

            print("\n||   ~FINAL CALCULATION~   ||")
            print(f"Chargeable Income: RM{income - relief:,.2f}")
            print(f"Tax Payable: RM{tax:,.2f}")

        elif user_choice == "3":
            print("\n||   ~TAX RECORDS~   ||")
            if not all_users:
                print("Hmm, it looks empty here!")
                continue

            print(f"{'IC Number':<15} {'Income':>12} {'Relief':>12} {'Tax':>12}")
            print("_" * 55)
            for user in all_users:
                print(f"{user['IC Number']:<15} "
                      f"RM{user['Income']:>10,.2f} "
                      f"RM{user['Tax Relief']:>10,.2f} "
                      f"RM{user['Tax Payable']:>10,.2f}")

        elif user_choice == "4":
            print("Thank you for using the tax calculator! Have a nice day! :D ")
            break

if __name__ == "__main__":
    main()
