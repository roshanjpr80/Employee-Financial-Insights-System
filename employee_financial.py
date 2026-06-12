
from colorama import Fore, Style, init
import json
from pathlib import Path

init(autoreset=True)

# JSON & Report Directory
DATA_FILE = Path("employees.json")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


# ---------------------- Input Helper Functions -------------------------

def get_string(prompt):
    return input(Fore.GREEN + prompt)

def get_int(prompt):
    while True:
        try:
            return int(input(Fore.GREEN + prompt))
        except:
            print(Fore.RED + "❌ Invalid number! Enter an integer.")

def get_float(prompt):
    while True:
        try:
            return float(input(Fore.GREEN + prompt))
        except:
            print(Fore.RED + "❌ Invalid amount! Enter a numeric value.")


# ---------------------- Financial Calculations -------------------------

def compute_financials(salary):
    tax_rate = 0.12
    growth_rate = 0.05
    save_rate = 0.20

    annual_salary = salary * 12
    tax = salary * tax_rate
    take_home = salary - tax

    # 5-year salary growth
    growth = []
    temp = salary
    for _ in range(5):
        temp *= (1 + growth_rate)
        growth.append(round(temp, 2))

    annual_savings = take_home * save_rate
    five_year_savings = annual_savings * 5

    return {
        "annual_salary": annual_salary,
        "post_tax": take_home,
        "growth": growth,
        "annual_savings": annual_savings,
        "five_year_savings": five_year_savings
    }


# ---------------------- Export Functions -------------------------

def save_json(data):
    existing = []
    if DATA_FILE.exists():
        existing = json.loads(DATA_FILE.read_text())

    existing.append(data)
    DATA_FILE.write_text(json.dumps(existing, indent=4))


def save_text_report(employee):
    file_path = REPORT_DIR / f"{employee['name'].replace(' ', '_')}_report.txt"

    with open(file_path, "w") as f:
        f.write("----- Employee Financial Report -----\n")
        for k, v in employee.items():
            f.write(f"{k}: {v}\n")


def save_csv(employee):
    file_path = REPORT_DIR / f"{employee['name'].replace(' ', '_')}.csv"

    with open(file_path, "w") as f:
        for k, v in employee.items():
            f.write(f"{k},{v}\n")


# ---------------------- UI & Menu -------------------------

def banner():
    print(Fore.CYAN + "\n" + "-" * 70)
    print(Fore.YELLOW + "           Employee Financial Insights System (Pro Version)")
    print(Fore.CYAN + "-" * 70)


def menu():
    print(Fore.MAGENTA + "\nMenu Options:")
    print("1. Add Employee Financial Report")
    print("2. Export Last Report (TXT/CSV)")
    print("3. Exit")
    return get_int("Choose an option: ")


# ---------------------- Main Program -------------------------

last_employee = None

while True:
    banner()
    choice = menu()

    # ADD EMPLOYEE
    if choice == 1:
        name = get_string("Enter full name: ")
        dept = get_string("Enter department: ")
        exp = get_int("Enter years of experience: ")
        salary = get_float("Enter current monthly salary ($): ")

        report = compute_financials(salary)

        print(Fore.CYAN + "\n--- Employee Financial Report Generated ---")
        print(Fore.YELLOW + f"Name: {name}")
        print(f"Department: {dept}")
        print(f"Experience: {exp} years")
        print(f"Monthly Salary: ${salary:.2f}")
        print(f"Annual Salary: ${report['annual_salary']:.2f}")
        print(f"Post-Tax Salary: ${report['post_tax']:.2f}")

        print(Fore.MAGENTA + "\nSalary Growth for 5 Years:")
        for i, g in enumerate(report["growth"], 1):
            print(f" Year {i}: ${g}")

        print(Fore.GREEN + f"\nAnnual Savings: ${report['annual_savings']:.2f}")
        print(Fore.GREEN + f"5-Year Savings: ${report['five_year_savings']:.2f}")

        last_employee = {
            "name": name,
            "department": dept,
            "experience": exp,
            "current_salary": salary,
            **report
        }

        save_json(last_employee)
        print(Fore.GREEN + "\n✔ Employee data saved to JSON!")

    # EXPORT REPORT
    elif choice == 2:
        if not last_employee:
            print(Fore.RED + "❌ No report generated yet! Please add an employee first.")
        else:
            print(Fore.YELLOW + "\nExport Options:")
            print("1. Save as TXT")
            print("2. Save as CSV")
            print("3. Save Both")

            op = get_int("Choose: ")

            if op == 1:
                save_text_report(last_employee)
                print(Fore.GREEN + "✔ Saved as TXT!")
            elif op == 2:
                save_csv(last_employee)
                print(Fore.GREEN + "✔ Saved as CSV!")
            elif op == 3:
                save_text_report(last_employee)
                save_csv(last_employee)
                print(Fore.GREEN + "✔ Saved TXT + CSV!")

    # EXIT SYSTEM
    elif choice == 3:
        print(Fore.CYAN + "\nThank you for using the Financial Insights System!")
        break

    else:
        print(Fore.RED + "❌ Invalid choice! Try again.")
