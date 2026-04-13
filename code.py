import json
import numpy as np
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
        print(f"Name: {s['name']}, Roll: {s['roll']}, Room: {s['room']}, Fee: {s['fee_paid']}")
    print()

# Search
def search_student(data):
    roll = input("Enter roll number: ")
    
    for s in data:
        if s["roll"] == roll:
            print("\nStudent Found:", s, "\n")
            return
    
    print("❌ Not found.\n")

# Update fee
def update_fee(data):
    roll = input("Enter roll number: ")
    
    for s in data:
        if s["roll"] == roll:
            extra = float(input("Enter additional fee: "))
            s["fee_paid"] += extra
            save_data(data)
            print("✅ Fee updated.\n")
            return
    
    print("❌ Student not found.\n")

# Delete student
def delete_student(data):
    roll = input("Enter roll number: ")
    
    for s in data:
        if s["roll"] == roll:
            data.remove(s)
            save_data(data)
            print("✅ Student deleted.\n")
            return
    
    print("❌ Student not found.\n")

# Fee report
def fee_report(data):
    total_fee = 50000
    total_paid = 0
    total_due = 0
    
    print("\n--- Fee Report ---")
    
    for s in data:
        paid = s["fee_paid"]
        due = total_fee - paid
        
        total_paid += paid
        total_due += due
        
        print(f"{s['name']} (Roll {s['roll']}): Paid = {paid}, Due = {due}")
    
    print("\nTotal Paid:", total_paid)
    print("Total Due:", total_due)
    print()

# Room report
def room_report(data):
    rooms = {}
    
    for s in data:
        room = s["room"]
        if room not in rooms:
            rooms[room] = []
        rooms[room].append(s["name"])
    
    print("\n--- Room Allocation ---")
    for room in rooms:
        print(f"Room {room}: {', '.join(rooms[room])}")
    print()

# ================= AI / ML PART =================

def train_models(data):
    if len(data) < 2:
        print("⚠️ Not enough data for AI training.\n")
        return None, None

    X = []
    y_reg = []
    y_cls = []

    total_fee = 50000

    for s in data:
        paid = s["fee_paid"]

        X.append([paid])
        y_reg.append(paid)

        if paid < total_fee * 0.5:
            y_cls.append(0)  # Defaulter
        else:
            y_cls.append(1)  # Regular

    X = np.array(X)
    y_reg = np.array(y_reg)
    y_cls = np.array(y_cls)

    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X, y_reg)

    # Decision Tree
    dt_model = DecisionTreeClassifier()
    dt_model.fit(X, y_cls)

    return lr_model, dt_model

def predict_student(data):
    lr_model, dt_model = train_models(data)

    if lr_model is None:
        return

    roll = input("Enter roll number: ")

    for s in data:
        if s["roll"] == roll:
            paid = s["fee_paid"]

            pred_fee = lr_model.predict([[paid]])[0]
            status = dt_model.predict([[paid]])[0]

            print("\n--- AI Prediction ---")
            print(f"Current Paid: {paid}")
            print(f"Predicted Fee Trend: {pred_fee:.2f}")

            if status == 0:
                print("Status: ❌ Defaulter")
            else:
                print("Status: ✅ Regular")
            print()
            return

    print("❌ Student not found.\n")

# ================= MAIN MENU =================

def main():
    data = load_data()
    
    while True:
        print("====== HOSTEL MANAGEMENT SYSTEM ======")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Fee")
        print("5. Delete Student")
        print("6. Fee Report")
        print("7. Room Report")
        print("8. AI Prediction")
        print("9. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_student(data)
        elif choice == "2":
            view_students(data)
        elif choice == "3":
            search_student(data)
        elif choice == "4":
            update_fee(data)
        elif choice == "5":
            delete_student(data)
        elif choice == "6":
            fee_report(data)
        elif choice == "7":
            room_report(data)
        elif choice == "8":
            predict_student(data)
        elif choice == "9":
            print("Exiting program...")
            break
        else:
            print("Invalid choice!\n")

# Run program
main()
