# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore

db = None

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized globally")
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")
else:
    db = firestore.client()
