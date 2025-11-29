
#!/usr/bin/env python3
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



















































# import streamlit as st
# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# from pathlib import Path

# # Data file path
# DATA_FILE = Path("employees_data.json")


# # ---------------------- Financial Calculations -------------------------

# def compute_financials(salary):
#     tax_rate = 0.12
#     growth_rate = 0.05
#     save_rate = 0.20

#     annual_salary = salary * 12
#     tax = salary * tax_rate
#     take_home = salary - tax

#     # 5-year salary growth
#     growth = []
#     temp = salary
#     for _ in range(5):
#         temp *= (1 + growth_rate)
#         growth.append(round(temp, 2))

#     annual_savings = take_home * save_rate
#     five_year_savings = annual_savings * 5

#     return {
#         "annual_salary": annual_salary,
#         "post_tax": take_home,
#         "growth": growth,
#         "annual_savings": annual_savings,
#         "five_year_savings": five_year_savings
#     }


# # ---------------------- Save Data -------------------------

# def save_to_json(entry):
#     existing = []
#     if DATA_FILE.exists():
#         existing = json.loads(DATA_FILE.read_text())

#     existing.append(entry)
#     DATA_FILE.write_text(json.dumps(existing, indent=4))


# def generate_txt_report(employee):
#     content = "----- Employee Financial Report -----\n"
#     for k, v in employee.items():
#         content += f"{k}: {v}\n"
#     return content


# def generate_csv(employee):
#     df = pd.DataFrame(employee.items(), columns=["Field", "Value"])
#     return df.to_csv(index=False).encode("utf-8")


# # ---------------------- Streamlit UI -------------------------

# st.title("💼 Employee Financial Insights System (Streamlit Pro Version)")
# st.write("---")

# st.subheader("📌 Enter Employee Details")

# name = st.text_input("Full Name")
# department = st.text_input("Department")
# experience = st.number_input("Years of Experience", min_value=0, step=1)
# salary = st.number_input("Current Monthly Salary ($)", min_value=0.0, step=100.0)


# if st.button("Generate Financial Report"):
#     if name == "" or salary == 0:
#         st.error("❌ Please enter all required fields!")
#     else:
#         report = compute_financials(salary)

#         st.success("✔ Financial report generated successfully!")

#         # Display Results
#         st.write("## 📊 Financial Summary")
#         st.write(f"**Name:** {name}")
#         st.write(f"**Department:** {department}")
#         st.write(f"**Experience:** {experience} years")
#         st.write(f"**Monthly Salary:** ${salary:.2f}")
#         st.write(f"**Annual Salary:** ${report['annual_salary']:.2f}")
#         st.write(f"**Post-Tax Monthly Salary:** ${report['post_tax']:.2f}")

#         # 5-year salary growth table
#         st.write("### 📈 5-Year Salary Growth")
#         growth_df = pd.DataFrame({
#             "Year": [1, 2, 3, 4, 5],
#             "Projected Salary ($)": report["growth"]
#         })
#         st.dataframe(growth_df)

#         # Plot Growth Graph
#         st.write("### 📉 Salary Growth Chart")
#         fig, ax = plt.subplots()
#         ax.plot(growth_df["Year"], growth_df["Projected Salary ($)"])
#         ax.set_xlabel("Year")
#         ax.set_ylabel("Salary ($)")
#         ax.set_title("5-Year Salary Growth Trend")
#         st.pyplot(fig)

#         st.write("### 💰 Savings Forecast")
#         st.write(f"**Annual Savings:** ${report['annual_savings']:.2f}")
#         st.write(f"**5-Year Savings:** ${report['five_year_savings']:.2f}")

#         # Prepare data for export
#         employee_entry = {
#             "name": name,
#             "department": department,
#             "experience": experience,
#             "current_salary": salary,
#             **report
#         }

#         save_to_json(employee_entry)

#         st.success("✔ Employee data saved to JSON!")

#         # Download Buttons
#         st.write("## 📥 Download Report")

#         # TXT
#         txt_data = generate_txt_report(employee_entry)
#         st.download_button(
#             label="📄 Download TXT Report",
#             data=txt_data,
#             file_name=f"{name.replace(' ', '_')}_report.txt"
#         )

#         # CSV
#         csv_data = generate_csv(employee_entry)
#         st.download_button(
#             label="📊 Download CSV Report",
#             data=csv_data,
#             file_name=f"{name.replace(' ', '_')}_report.csv",
#             mime="text/csv"
#         )

# st.write("---")
# st.info("Made with ❤️ using Streamlit — AI-powered Financial Insights System")
