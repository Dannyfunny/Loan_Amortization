from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def generate_amortization_schedule(principal, rate_per_annum, years, payments_per_annum=12):
    rate_per_month = rate_per_annum / payments_per_annum
    total_payments = years * payments_per_annum
    monthly_payment = (principal * rate_per_month) / (1 - (1 + rate_per_month) ** -total_payments)

    remaining_balance = principal
    schedule = []

    for payment_number in range(1, total_payments + 1):
        interest_amount = remaining_balance * rate_per_month
        principal_amount = monthly_payment - interest_amount
        remaining_balance -= principal_amount
        remaining_balance = max(remaining_balance, 0)

        schedule.append({
            'Payment Number': payment_number,
            'Payment Amount': round(monthly_payment, 2),
            'Principal Payment': round(principal_amount, 2),
            'Interest Payment': round(interest_amount, 2),
            'Remaining Balance': round(remaining_balance, 2),
        })

    return schedule

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate']) / 100
        years = int(request.form['years'])

        schedule = generate_amortization_schedule(principal, rate, years)
        return render_template('schedule.html', schedule=schedule)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
