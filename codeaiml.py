import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

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

    for s in data:
        print(s)
    print()

# 🔮 ML: Fee Prediction (Regression)
def predict_fee(data):
    if len(data) < 2:
        print("❌ Not enough data.\n")
        return

    df = pd.DataFrame(data)
    df["roll"] = pd.to_numeric(df["roll"], errors='coerce')

    X = df[["roll"]]
    y = df["fee_paid"]

    model = LinearRegression()
    model.fit(X, y)

    new_roll = int(input("Enter roll number: "))
    prediction = model.predict([[new_roll]])

    print(f"🔮 Predicted Fee: {prediction[0]:.2f}\n")

# 🤖 REAL ML: Risk Classification
def train_and_classify(data):
    if len(data) < 3:
        print("❌ Not enough data to train ML model.\n")
        return

    df = pd.DataFrame(data)
    total_fee = 50000

    # Create labels (target)
    def label(row):
        ratio = row["fee_paid"] / total_fee
        if ratio < 0.5:
            return 0   # High Risk
        elif ratio < 0.8:
            return 1   # Medium Risk
        else:
            return 2   # Low Risk

    df["risk"] = df.apply(label, axis=1)

    # Features (input)
    df["roll"] = pd.to_numeric(df["roll"], errors='coerce')
    X = df[["roll", "fee_paid"]]
    y = df["risk"]

    # Train ML model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    print("\n--- ML Risk Prediction ---")
    for i, row in df.iterrows():
        pred = model.predict([[row["roll"], row["fee_paid"]]])[0]

        if pred == 0:
            risk = "High Risk"
        elif pred == 1:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        print(f"{row['name']} (Roll {row['roll']}): {risk}")
    print()

# Main menu
def main():
    data = load_data()

    while True:
        print("====== AI HOSTEL MANAGEMENT SYSTEM ======")
        print("1. Add Student")
        print("2. View Students")
        print("3. Predict Fee (ML)")
        print("4. ML Risk Classification")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student(data)
        elif choice == "2":
            view_students(data)
        elif choice == "3":
            predict_fee(data)
        elif choice == "4":
            train_and_classify(data)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")

if __name__ == "__main__":
    main()
