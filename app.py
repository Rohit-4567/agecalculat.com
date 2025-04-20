from flask import Flask, render_template, request
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

def calculate_age(day, month, year):
    today = date.today()
    dob = date(year, month, day)
    
    years = today.year - dob.year
    months = today.month - dob.month
    days = today.day - dob.day

    # Adjusting if days or months are negative
    if days < 0:
        months -= 1
        days += 30  # approximate days in a month

    if months < 0:
        years -= 1
        months += 12

    total_days = (today - dob).days
    total_seconds = total_days * 86400

    return {
        'years': years,
        'months': months,
        'days': days,
        'total_time_lived': {
            'days': total_days,
            'hours': total_seconds // 3600,
            'minutes': total_seconds // 60,
            'seconds': total_seconds
        },
        'days_until_birthday': (
            (dob.replace(year=today.year) - today).days
            if dob.replace(year=today.year) >= today
            else (dob.replace(year=today.year + 1) - today).days
        ),
        'birthday_message': "🎉 Happy Birthday!" if today.month == dob.month and today.day == dob.day else None
    }

def calculate_difference(age1, age2):
    # Calculate total days for both
    total_days1 = age1['total_time_lived']['days']
    total_days2 = age2['total_time_lived']['days']
    
    # Calculate the absolute difference in days
    difference_in_days = abs(total_days1 - total_days2)
    
    # Convert days back to years, months, days
    years = difference_in_days // 365
    remaining_days = difference_in_days % 365
    months = remaining_days // 30  # approximate number of months
    days = remaining_days % 30  # approximate number of days

    return f"{years} years, {months} months, and {days} days"

@app.route('/', methods=['GET', 'POST'])
def index():
    age = None
    if request.method == 'POST':
        try:
            day = int(request.form['day'])
            month = int(request.form['month'])
            year = int(request.form['year'])
            
            # Calculate age
            age = calculate_age(day, month, year)

        except Exception as e:
            return f"Error: {e}"
    
    current_year = date.today().year
    return render_template('index.html', age=age, current_year=current_year)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        try:
            # Get form data for both birthdays
            day1 = int(request.form['day1'])
            month1 = int(request.form['month1'])
            year1 = int(request.form['year1'])
            
            day2 = int(request.form['day2'])
            month2 = int(request.form['month2'])
            year2 = int(request.form['year2'])
            
            # Calculate age for both birthdays
            age1 = calculate_age(day1, month1, year1)
            age2 = calculate_age(day2, month2, year2)

            # Calculate the difference between the two
            age_difference = calculate_difference(age1, age2)

            return render_template('compare.html', compare_result=age_difference)
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template('compare.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
