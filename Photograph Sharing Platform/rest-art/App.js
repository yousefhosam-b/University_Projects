import "react-native-gesture-handler";
import React from "react";
import { StyleSheet } from "react-native";

import { AuthProvider } from "./components/AuthProvider";
import Navigation from "./components/Navigation";

export default function App() {
  return (
    <AuthProvider>
      <Navigation />
    </AuthProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
});
