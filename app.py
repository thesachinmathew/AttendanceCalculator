from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    extra_info = ""
    if request.method == 'POST':
        attended = int(request.form['attended'])
        total = int(request.form['total'])
        min_required = int(request.form['required'])

        current_percentage = (attended / total) * 100
        current_percentage = round(current_percentage, 2)

        if current_percentage >= min_required:
            # Max classes you can bunk and still stay above required percentage
            bunkable = 0
            max_total = attended
            while (attended / (max_total + 1)) * 100 >= min_required:
                max_total += 1
                bunkable += 1
            result = f"✅ You're meeting the attendance requirement! ({current_percentage}%)"
            extra_info = f"You can safely bunk <strong>{bunkable}</strong> more class{'es' if bunkable != 1 else ''}."
        else:
            # Classes required to reach desired percentage
            needed = ((min_required * total) - (attended * 100)) / (100 - min_required)
            needed = max(0, int(needed + 0.99))  # round up
            result = f"⚠️ Your current attendance is {current_percentage}%. Below requirement!"
            extra_info = f"You need to attend at least <strong>{needed}</strong> more class{'es' if needed != 1 else ''} to reach {min_required}%."

    return render_template('index.html', result=result, extra_info=extra_info)

if __name__ == '__main__':
    app.run(debug=True)
