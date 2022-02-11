import * as firebase from "firebase";

export const firebaseConfig = {
  apiKey: "AIzaSyD7lhScB8_LMv3V-6-lMDFB6YuRf0YTr6I",
  authDomain: "rest-art-40e11.firebaseapp.com",
  projectId: "rest-art-40e11",
  storageBucket: "rest-art-40e11.appspot.com",
  messagingSenderId: "503289104117",
  appId: "1:503289104117:web:84c9f1ee8e6f2545eaa7bc",
  measurementId: "G-2M9W8P90S3",
};

export const firebaseApp = firebase.initializeApp(firebaseConfig);
export const auth = firebase.auth();
export const firestore = firebase.firestore();
export const storage = firebase.storage();
