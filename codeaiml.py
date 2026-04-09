import json
import pandas as pd
from sklearn.linear_model import LinearRegression

FILE_NAME = "students.json"

# Load data
def load_data():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return []

# Save data
def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

# Add student
def add_student(data):
    name = input("Enter name: ")
    roll = input("Enter roll number: ")

    for s in data:
        if s["roll"] == roll:
            print("❌ Roll already exists!\n")
            return

    room = input("Enter room number: ")
    fee_paid = float(input("Enter fee paid: "))

    student = {
        "name": name,
        "roll": roll,
        "room": room,
        "fee_paid": fee_paid
    }

    data.append(student)
    save_data(data)
    print("✅ Student added!\n")

# View students
def view_students(data):
    if not data:
        print("No records found.\n")
        return

    print("\n--- Student List ---")
    for s in data:
        print(s)
    print()

# 🔮 ML: Fee Prediction
def predict_fee(data):
    if len(data) < 2:
        print("❌ Not enough data for prediction.\n")
        return

    df = pd.DataFrame(data)

    # Convert roll to numeric for ML
    df["roll"] = pd.to_numeric(df["roll"], errors='coerce')

    X = df[["roll"]]
    y = df["fee_paid"]

    model = LinearRegression()
    model.fit(X, y)

    new_roll = int(input("Enter roll number to predict fee: "))
    predicted_fee = model.predict([[new_roll]])

    print(f"🔮 Predicted Fee for Roll {new_roll}: {predicted_fee[0]:.2f}\n")

# 🚨 ML: Risk Classification
def classify_students(data):
    if not data:
        print("No data available.\n")
        return

    total_fee = 50000

    print("\n--- Student Risk Classification ---")
    for s in data:
        paid = s["fee_paid"]
        ratio = paid / total_fee

        if ratio < 0.5:
            risk = "High Risk"
        elif ratio < 0.8:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        print(f"{s['name']} (Roll {s['roll']}): {risk}")
    print()

# Main menu
def main():
    data = load_data()

    while True:
        print("====== SMART HOSTEL MANAGEMENT SYSTEM ======")
        print("1. Add Student")
        print("2. View Students")
        print("3. Predict Fee (ML)")
        print("4. Classify Students (ML)")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student(data)
        elif choice == "2":
            view_students(data)
        elif choice == "3":
            predict_fee(data)
        elif choice == "4":
            classify_students(data)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")

if __name__ == "__main__":
    main()
