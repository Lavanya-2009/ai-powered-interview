from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Predefined list of aptitude questions
QUESTIONS = [
    {"question": "What is the next number in the sequence: 3, 6, 12, 24, ...?",
     "options": ["A) 36", "B) 48", "C) 30", "D) 50"],
     "correct_answer": "B"},
     
    {"question": "What is the square root of 225?",
     "options": ["A) 10", "B) 15", "C) 20", "D) 25"],
     "correct_answer": "B"},
    
    {"question": "If a train is moving at 90 km/h, how far will it travel in 2.5 hours?",
     "options": ["A) 200 km", "B) 180 km", "C) 225 km", "D) 240 km"],
     "correct_answer": "C"},
    
    {"question": "What is 15% of 240?",
     "options": ["A) 36", "B) 40", "C) 48", "D) 60"],
     "correct_answer": "C"},
    
    {"question": "A shopkeeper gives a 20% discount on a ₹500 item. What is the final price?",
     "options": ["A) ₹400", "B) ₹450", "C) ₹420", "D) ₹480"],
     "correct_answer": "B"},
    
    {"question": "What is the perimeter of a square with side length 7 cm?",
     "options": ["A) 14 cm", "B) 21 cm", "C) 28 cm", "D) 35 cm"],
     "correct_answer": "C"},
    
    {"question": "Solve: 2^5 ÷ 2^3",
     "options": ["A) 2", "B) 4", "C) 6", "D) 8"],
     "correct_answer": "B"},
    
    {"question": "A car travels 180 km in 3 hours. What is its speed?",
     "options": ["A) 50 km/h", "B) 55 km/h", "C) 60 km/h", "D) 65 km/h"],
     "correct_answer": "C"},
    
    {"question": "Find the missing number: 2, 5, 10, 17, ?",
     "options": ["A) 24", "B) 26", "C) 30", "D) 35"],
     "correct_answer": "A"},
    
    {"question": "If the sum of three consecutive numbers is 60, what is the middle number?",
     "options": ["A) 19", "B) 20", "C) 21", "D) 22"],
     "correct_answer": "C"},
    
    {"question": "Which is the largest prime number below 50?",
     "options": ["A) 43", "B) 47", "C) 49", "D) 45"],
     "correct_answer": "B"},
    
    {"question": "If a triangle has angles 40° and 65°, what is the third angle?",
     "options": ["A) 55°", "B) 60°", "C) 75°", "D) 80°"],
     "correct_answer": "C"},
    
    {"question": "Solve: 7 × 8 - 4 × 6",
     "options": ["A) 28", "B) 30", "C) 32", "D) 34"],
     "correct_answer": "C"},
    
    {"question": "If 12 workers finish a job in 6 days, how many days will 8 workers take?",
     "options": ["A) 8", "B) 9", "C) 10", "D) 12"],
     "correct_answer": "D"},
    
    {"question": "What is 3/4 of 200?",
     "options": ["A) 100", "B) 150", "C) 200", "D) 250"],
     "correct_answer": "B"},
    
    {"question": "What is the remainder when 1234 is divided by 5?",
     "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
     "correct_answer": "D"},
    
    {"question": "How many degrees are in a right angle?",
     "options": ["A) 45°", "B) 60°", "C) 90°", "D) 180°"],
     "correct_answer": "C"},
    
    {"question": "If a box has 3 red, 4 blue, and 5 green balls, what is the probability of picking a blue ball?",
     "options": ["A) 1/3", "B) 2/5", "C) 1/4", "D) 4/12"],
     "correct_answer": "B"},
    
    {"question": "Solve: 8! ÷ (6! × 2!)",
     "options": ["A) 24", "B) 28", "C) 32", "D) 36"],
     "correct_answer": "A"},
    
    {"question": "A father is twice as old as his son. If the son is 20 years old, how old is the father?",
     "options": ["A) 30", "B) 35", "C) 40", "D) 45"],
     "correct_answer": "C"},
    
    {"question": "What is the LCM of 12 and 18?",
     "options": ["A) 24", "B) 30", "C) 36", "D) 48"],
     "correct_answer": "C"},
    
    {"question": "A train 200m long crosses a pole in 20 seconds. What is its speed?",
     "options": ["A) 20 m/s", "B) 25 m/s", "C) 30 m/s", "D) 35 m/s"],
     "correct_answer": "A"},
    
    {"question": "If the sum of angles in a triangle is 180°, what is the sum of angles in a pentagon?",
     "options": ["A) 360°", "B) 540°", "C) 720°", "D) 900°"],
     "correct_answer": "B"},
    
    {"question": "A boat moves upstream at 10 km/h and downstream at 20 km/h. What is its still-water speed?",
     "options": ["A) 12 km/h", "B) 13 km/h", "C) 14 km/h", "D) 15 km/h"],
     "correct_answer": "D"},
    
    {"question": "If a rectangle has a length of 15 cm and width of 10 cm, what is its area?",
     "options": ["A) 100 cm²", "B) 120 cm²", "C) 150 cm²", "D) 180 cm²"],
     "correct_answer": "C"},
    
    {"question": "Find the missing term: 2, 6, 12, 20, ?",
     "options": ["A) 28", "B) 30", "C) 32", "D) 36"],
     "correct_answer": "A"},
    
    {"question": "What is the average of 20, 30, 40, and 50?",
     "options": ["A) 30", "B) 35", "C) 40", "D) 45"],
     "correct_answer": "B"},
    
    {"question": "Solve: 3^3 + 4^2 - 2^4",
     "options": ["A) 15", "B) 17", "C) 19", "D) 21"],
     "correct_answer": "B"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_quiz")
def get_quiz():
    """Serve 5 random questions from the predefined list."""
    quiz_questions = random.sample(QUESTIONS, 5)  # Select 5 random questions
    return jsonify(quiz_questions)

if __name__ == "__main__":
    app.run(debug=True)
