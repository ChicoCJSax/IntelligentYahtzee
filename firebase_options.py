import pyrebase
from firebaseConfigInfo import firebaseConfig

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