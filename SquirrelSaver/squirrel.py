import customtkinter as ctk
import math
import yfinance as yf

# Initialize the main window
app = ctk.CTk()
app.title("Squirrel Saver")
app.geometry("500x400")
app.resizable(False, False)
app.iconbitmap("SquirrelSaver\logo_SqSa.ico")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Dictionary to store user input data (age, income, savings, debts, etc.)
user_data = {
    "age": None,
    "income": 0,
    "expenses": 0,
    "has_savings": None,
    "savings": 0,
    "has_debts": None,
    "debts": 0,
    "money_to_save_month": 0,
    "wants_to_pay_debt": True,
    "investment": None
}

# Function for first set of questions (age, income, expenses)
def questions():
    user_data["age"] = age_entry.get()
    user_data["income"] = float(income_entry.get())
    user_data["expenses"] = float(expenses_entry.get())
    savings()

# Starting point: Ask for age, income, and expenses
label = ctk.CTkLabel(app, text="Enter your age, income, and expenses")
label.pack(pady=20)

age_entry = ctk.CTkEntry(app, placeholder_text="Age")
age_entry.pack(pady=5)

income_entry = ctk.CTkEntry(app, placeholder_text="Income")
income_entry.pack(pady=5)

expenses_entry = ctk.CTkEntry(app, placeholder_text="Expenses")
expenses_entry.pack(pady=5)

next_button = ctk.CTkButton(app, text="Next", command=questions)
next_button.pack(pady=20)

def savings():
    for widget in app.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(app, text="Do you have savings?")
    label.pack(pady=20)
    yes_button = ctk.CTkButton(app, text="Yes", command=has_savings)
    yes_button.pack(side="left", padx=20)
    no_button = ctk.CTkButton(app, text="No", command=no_savings)
    no_button.pack(side="right", padx=20)

def has_savings():
    user_data["has_savings"] = True
    for widget in app.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(app, text="How much savings do you have?")
    label.pack(pady=20)
    savings_entry = ctk.CTkEntry(app)
    savings_entry.pack(pady=10)
    next_button = ctk.CTkButton(app, text="Next", command=lambda: save_savings(savings_entry))
    next_button.pack(pady=20)

def save_savings(savings_entry):
    user_data["savings"] = float(savings_entry.get())
    debt_question()

def no_savings():
    user_data["has_savings"] = False
    debt_question()

def debt_question():
    for widget in app.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(app, text="Do you have debts?")
    label.pack(pady=20)
    yes_button = ctk.CTkButton(app, text="Yes", command=has_debts)
    yes_button.pack(side="left", padx=20)
    no_button = ctk.CTkButton(app, text="No", command=no_debts)
    no_button.pack(side="right", padx=20)

def has_debts():
    user_data["has_debts"] = True
    for widget in app.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(app, text="How much debt do you have?")
    label.pack(pady=20)
    debt_entry = ctk.CTkEntry(app)
    debt_entry.pack(pady=10)
    next_button = ctk.CTkButton(app, text="Next", command=lambda: save_debts(debt_entry))
    next_button.pack(pady=20)

def save_debts(debt_entry):
    user_data["debts"] = float(debt_entry.get())
    pay_off_debts()

def no_debts():
    user_data["has_debts"] = False
    final_investment_calculation()

def pay_off_debts():
    for widget in app.winfo_children():
        widget.destroy()
    income = user_data["income"]
    expenses = user_data["expenses"]
    savings = user_data["savings"]
    debt = user_data["debts"]
    available_money = income - expenses

    if savings >= debt:
        label = ctk.CTkLabel(app, text="Your savings can cover all your debts. Would you like to pay off your debts?")
        label.pack(pady=20)
        yes_button = ctk.CTkButton(app, text="Yes", command=lambda: confirm_debt_payment(True))
        yes_button.pack(side="left", padx=20)
        no_button = ctk.CTkButton(app, text="No", command=lambda: confirm_debt_payment(False))
        no_button.pack(side="right", padx=20)
    elif savings > 0 and savings < debt:
        label = ctk.CTkLabel(app, text=f"Your savings can partially cover your debts.\nYou would have {debt - savings}€ remaining in debt. Use savings?")
        label.pack(pady=20)
        yes_button = ctk.CTkButton(app, text="Yes", command=lambda: partial_debt_payment(savings))
        yes_button.pack(side="left", padx=20)
        no_button = ctk.CTkButton(app, text="No", command=ask_monthly_payment)
        no_button.pack(side="right", padx=20)
    else:
        label = ctk.CTkLabel(app, text=f"You should have {available_money}€ available after expenses to pay your {debt}€ in debts. Set monthly payment?")
        label.pack(pady=20)
        monthly_payment_entry = ctk.CTkEntry(app)
        monthly_payment_entry.pack(pady=10)
        next_button = ctk.CTkButton(app, text="Next", command=lambda: set_monthly_payment(monthly_payment_entry))
        next_button.pack(pady=20)

def confirm_debt_payment(pay_debt):
    if pay_debt:
        user_data["savings"] -= user_data["debts"]
        user_data["debts"] = 0
        user_data["has_debts"] = False
    final_investment_calculation()

def partial_debt_payment(savings):
    user_data["debts"] -= savings
    user_data["savings"] = 0
    ask_monthly_payment()

def ask_monthly_payment():
    for widget in app.winfo_children():
        widget.destroy()
    remaining_debt = user_data["debts"]
    available_money = user_data["income"] - user_data["expenses"]
    label = ctk.CTkLabel(app, text=f"You still have {remaining_debt}€ in debt. Set monthly payment?")
    label.pack(pady=20)
    monthly_payment_entry = ctk.CTkEntry(app)
    monthly_payment_entry.pack(pady=10)
    next_button = ctk.CTkButton(app, text="Next", command=lambda: set_monthly_payment(monthly_payment_entry))
    next_button.pack(pady=20)

def set_monthly_payment(monthly_payment_entry):
    user_data["money_to_save_month"] = float(monthly_payment_entry.get())
    months_to_pay_off = math.ceil(user_data["debts"] / user_data["money_to_save_month"])
    for widget in app.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(app, text=f"You will be debt-free in {months_to_pay_off} months with {user_data['money_to_save_month']}€ per month.")
    label.pack(pady=20)
    final_investment_calculation()

# Final investment calculation function with slider and result display
def final_investment_calculation():
    for widget in app.winfo_children():
        widget.destroy()
    
    available_income = user_data["income"] - user_data["expenses"]
    label = ctk.CTkLabel(app, text=f"Du hast monatlich {available_income}€ nach Ausgaben zur Verfügung.")
    label.pack(pady=20)

    # Label to display selected investment amount
    slider_value_label = ctk.CTkLabel(app, text=f"Investitionsbetrag: 0€")
    slider_value_label.pack(pady=5)

    # Slider for selecting investment amount
    investment_slider = ctk.CTkSlider(app, from_=0, to=available_income, orientation="horizontal", number_of_steps=available_income)
    investment_slider.pack(pady=10)

    # Update slider label dynamically
    def update_slider_label(value):
        slider_value_label.configure(text=f"Investitionsbetrag: {int(value)}€")

    investment_slider.configure(command=update_slider_label)

    # Button to confirm investment amount
    confirm_button = ctk.CTkButton(app, text="Investieren", command=lambda: calculate_etf_investment(int(investment_slider.get())))
    confirm_button.pack(pady=20)

# Function to calculate ETF investment and open a result window
def calculate_etf_investment(monthly_investment):
    tickers = ["IWDA.AS", "SSAC.L"]
    data = yf.download(tickers, start="2014-10-01", end="2024-10-01", interval="1mo")
    iwda_close = data["Adj Close"]["IWDA.AS"]
    ssac_close = data["Adj Close"]["SSAC.L"]
    iwda_invested = 0
    ssac_invested = 0
    total_savings = 0

    # Simulate 10 years of monthly investments
    for i in range(len(iwda_close)):
        iwda_investment = monthly_investment * 0.7
        ssac_investment = monthly_investment * 0.3
        iwda_invested += iwda_investment / iwda_close[i]
        ssac_invested += ssac_investment / ssac_close[i]
        total_savings += monthly_investment

    # Final value calculation
    total_value = (iwda_invested * iwda_close[-1]) + (ssac_invested * ssac_close[-1])
    growth_value = total_value - total_savings  # ETF growth

    # Open a new window to display results
    result_window = ctk.CTkToplevel(app)
    result_window.title("Investment Ergebnis")
    result_window.geometry("400x300")

    # Display total amount and breakdown of savings vs. investment growth
    result_label = ctk.CTkLabel(result_window, text=f"Gesamtbetrag nach 10 Jahren: {total_value:.2f}€")
    result_label.pack(pady=10)

    breakdown_label = ctk.CTkLabel(result_window, text=f"Durch reines Sparen: {total_savings:.2f}€\nGewinn durch ETF-Wachstum: {growth_value:.2f}€")
    breakdown_label.pack(pady=10)

# Run the application
app.mainloop()

