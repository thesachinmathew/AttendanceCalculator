from flask import Flask, render_template, request
import math
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    result_class = "info"
    bunk_info = None
    
    if request.method == "POST":
        try:
            attended = int(request.form["attended"])
            total = int(request.form["total"])
            min_percent = int(request.form["min_percent"])

            # Validation
            if total <= 0:
                result = "Total classes must be greater than zero."
                result_class = "error"
            elif attended < 0:
                result = "Attended classes cannot be negative."
                result_class = "error"
            elif attended > total:
                result = "Attended classes cannot be more than total classes."
                result_class = "error"
            elif min_percent <= 0 or min_percent > 100:
                result = "Required attendance must be between 1 and 100."
                result_class = "error"
            else:
                # Calculate current attendance
                current_percent = round((attended / total) * 100, 2)
                
                if current_percent >= min_percent:
                    result = f"🎉 Great! Your current attendance is {current_percent}%. You already meet the {min_percent}% requirement!"
                    result_class = "success"
                    
                    # Calculate how many classes can be bunked
                    # Formula: (attended - min_percent/100 * (total + bunks)) >= 0
                    # Solving: bunks <= (100 * attended - min_percent * total) / min_percent
                    max_bunks = math.floor((100 * attended - min_percent * total) / min_percent)
                    max_bunks = max(0, max_bunks)
                    
                    if max_bunks > 0:
                        # Verify calculation
                        future_total = total + max_bunks
                        future_percent = round((attended / future_total) * 100, 2)
                        bunk_info = f"🎯 You can bunk up to {max_bunks} more classes and still maintain {min_percent}% attendance (will drop to {future_percent}%)"
                    else:
                        bunk_info = "⚠️ You cannot bunk any more classes without falling below the requirement"
                        
                else:
                    # Calculate needed classes
                    numerator = min_percent * total - 100 * attended
                    denominator = 100 - min_percent
                    
                    if denominator <= 0:
                        result = "Cannot achieve 100% attendance requirement."
                        result_class = "error"
                    else:
                        needed_exact = numerator / denominator
                        needed_classes = max(0, math.ceil(needed_exact))
                        
                        # Verify calculation
                        future_attended = attended + needed_classes
                        future_total = total + needed_classes
                        future_percent = round((future_attended / future_total) * 100, 2)
                        
                        result = f"📚 Current attendance: {current_percent}%. You need to attend {needed_classes} more consecutive classes to reach {min_percent}% requirement."
                        bunk_info = f"🎯 After attending {needed_classes} classes, you'll have {future_percent}% attendance"
                        result_class = "info"
                    
        except ValueError:
            result = "Please enter valid numbers in all fields."
            result_class = "error"
        except Exception:
            result = "An error occurred. Please check your inputs."
            result_class = "error"
            
    return render_template("index.html", result=result, result_class=result_class, bunk_info=bunk_info)

if __name__ == "__main__":
    app.run(debug=True)
