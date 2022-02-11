import React, { createContext, useState } from "react";
import { Alert } from "react-native";

import { auth, firestore } from "../firebase/config";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        signIn: async (email, password) => {
          auth
            .signInWithEmailAndPassword(email, password)
            .then((success) => null)
            .catch((e) => {
              if (e.code === "auth/wrong-password") {
                Alert.alert("Error", "Password is wrong.");
              }
              if (e.code === "auth/user-not-found") {
                Alert.alert("Error", "User did not registered.");
              }
              if (e.code === "auth/invalid-email") {
                Alert.alert("Error", "That email address is invalid!");
              }
            });
        },
        register: async (email, password, passwordconfirm) => {
          password !== passwordconfirm
            ? Alert.alert("Password Mismatch", "Passwords do not match!")
            : auth
                .createUserWithEmailAndPassword(email, password)
                .then(({ user }) => {
                  const document = firestore.collection("users").doc(user.uid);
                  document.set({
                    email: user.email,
                    displayName: "Unknown",
                    imageURL: "https://picsum.photos/200",
                  });
                })
                .catch((e) => {
                  if (e.code === "auth/email-already-in-use") {
                    Alert.alert(
                      "Error",
                      "That email address is already in use!"
                    );
                  }
                  if (e.code === "auth/weak-password") {
                    Alert.alert("Error", "Try stronger password");
                  }
                  if (e.code === "auth/invalid-email") {
                    Alert.alert("Error", "That email address is invalid!");
                  }
                });
        },
        signOut: async () =>
          auth
            .signOut()
            .then((s) => null)
            .catch((e) => null),
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
