import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyC0yQTUf86Gf9gilT5faIQWpuN7nDnXWts",
  "authDomain": "intelligentyahtzee.firebaseapp.com",
  "projectId": "intelligentyahtzee",
  "storageBucket": "intelligentyahtzee.firebasestorage.app",
  "messagingSenderId": "346054723591",
  "appId": "1:346054723591:web:d6e733c26ae92c0f0cc2a2",
  "measurementId": "G-J86SRE8G37",
  "databaseURL": "https://intelligentyahtzee-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("User logged in!")
        return user
    except Exception as e:
        raise ValueError("Invalid login") from e

def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print("User signed up!")
        return user
    except Exception as e:
        raise ValueError("Signup failed") from e

def saveMaxScore(user, score):
    try:
        uid = user["localId"]
        token = user["idToken"]
        db.child(uid).update({"maxScore": score}, token)
        print("Score saved!")
    except:
        print("Error saving score:")

def getMaxScore(user):
    try:
        uid = user["localId"]
        token = user["idToken"]
        maxScore = db.child(uid).child("maxScore").get(token)
        print("Score retrieved!")
        return maxScore.val()
    except:
        print("Error saving score:")