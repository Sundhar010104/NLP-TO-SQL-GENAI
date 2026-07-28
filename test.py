from auth.firebase import db

try:
    db.collection("test").document("demo").set({
        "name": "Firestore Test",
        "status": "Success"
    })

    print("✅ Firestore connection successful!")

except Exception as e:
    print("❌ Firestore Error:")
    print(e)