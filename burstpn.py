from flask import Flask, request, session, jsonify, Response
from flask_cors import CORS
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth, storage
from pyfcm import FCMNotification
from flask_pymongo import PyMongo
import pymongo
import random
import string
from bson import json_util, ObjectId
import json
import uuid
import time


app = Flask(__name__)
CORS(app)

''' Implement mongodb '''
app.config['MONGO_DBNAME'] = 'BurstUsers'
app.config['MONGO_URI'] = "mongodb+srv://fish:fish@burst-0-mfedp.mongodb.net/Brust_user?retryWrites=true"
mongo = PyMongo(app)

#Firebase configureation
#config = {
#    "apiKey": "AIzaSyDX2V0h0iLLrLADlAUmoBLk4zHG_xzAEKU",
#    "authDomain": "pushnotification-cbd2e.firebaseapp.com",
#    "databaseURL": "https://pushnotification-cbd2e.firebaseio.com",
#    "projectId": "pushnotification-cbd2e",
#    "storageBucket": "pushnotification-cbd2e.appspot.com",
#    "messagingSenderId": "117879701626",
#};
#firebase = pyrebase.initialize_app(config)
cred = credentials.Certificate("serviceAccountKey.json")
firebase = firebase_admin.initialize_app(cred, {
    'storageBucket': 'pushnotification-cbd2e.appspot.com'
})
@app.route("/")
def index():
    serverStatus = "Server running\n"
    return serverStatus

@app.route("/send_push_notification", methods=['GET'])
def send_push_notif():
    """sends push notification to the registration_id
        Args:
            registration_id : registration_id (obtained through getting the authorization from the user)
    """
    push_service = FCMNotification(api_key="AAAAG3ItgHo:APA91bEogfOFp_Ww61-X1AtqVZyXxG9FQnPjc8AWqTeOabeaxuaE3LWVI_3nTEGdJ5DYuhqu48kLC5Ou8Lm0c1x2-O8pK11vdpRY-uVeVAQyVS1c4QNpz5nfE4hJ8JxTxnvOgW9-6s5x")
    #Registration_id used to test: eZ6zsMlG2aI:APA91bG87qMf_ACHHx2cSBiu9IWbR9W78XQnzYO1Xz6qG116rLmacRZYwoFJM8mECQ19JVkbowolpxdFOpHbrwQGYiSnNeGJFuwSIeqN5MSJ6K3ZNe8wPhANd56V3F5ffHl5dyi7XpFH
    registration_id = request.args.get('registration_id')
    message_title = "Notification"
    message_body = "Please update"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    return jsonify({"success": True, "message": "sent"})
    
if __name__ == '__main__':
    app.secret_key = 'skey'
    app.run(debug=False)
