from flask import Flask, request, jsonify 
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from bson import ObjectId
from database import collection  # MongoDB collection from database.py

app = Flask(__name__)
CORS(app)
app.app_context().push()

# -------------------------------
# Route to Send Marketing Email
# -------------------------------
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json
    recipient = data.get("recipient")
    subject = data.get("subject")
    body = data.get("body")

    if not recipient or not subject or not body:
        return jsonify({"error": "Missing recipient, subject, or body"}), 400

    message = Mail(
        from_email="sinhalipika2000@gmail.com",
        to_emails=recipient,
        subject=subject,
        html_content=body
    )

    try:
        # Using hardcoded API key for now
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        return jsonify({"message": "Email sent", "status_code": response.status_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# Route to Submit Appointment
# -------------------------------
@app.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.json

    required_fields = ["date", "carDetails", "contactDetails", "paymentStatus"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing one or more required fields"}), 400

    result = collection.insert_one(data)

    # Send acknowledgment email
    try:
        recipient = data["contactDetails"]["email"]
        subject = "Appointment Confirmation"
        body = f"<p>Hi {data['contactDetails'].get('name', '')},</p><p>Your car service appointment is booked for {data['date']}.</p>"

        message = Mail(
            from_email="sinhalipika2000@gmail.com",
            to_emails=recipient,
            subject=subject,
            html_content=body
        )
        sg = SendGridAPIClient("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")
        sg.send(message)
    except Exception as e:
        print("Acknowledgment email failed:", str(e))

    return jsonify({"message": "Appointment created", "id": str(result.inserted_id)}), 201

# -------------------------------
# Route to Get All Appointments
# -------------------------------
@app.route("/appointments", methods=["GET"])
def get_appointments():
    appointments = []
    for appointment in collection.find():
        appointment["_id"] = str(appointment["_id"])
        appointments.append(appointment)
    return jsonify(appointments)

# -------------------------------
# Route to Update Appointment
# -------------------------------
@app.route("/appointments/<appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    data = request.json
    collection.update_one({"_id": ObjectId(appointment_id)}, {"$set": data})
    return jsonify({"message": "Appointment updated"}), 200

# -------------------------------
# Route to Delete Appointment
# -------------------------------
@app.route("/appointments/<appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    collection.delete_one({"_id": ObjectId(appointment_id)})
    return jsonify({"message": "Appointment deleted"}), 200

# -------------------------------
# Default route
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Car Workshop Appointment API is running"})

# -------------------------------
# Run locally
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
