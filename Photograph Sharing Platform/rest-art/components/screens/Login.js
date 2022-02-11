import React, { useContext, useState } from "react";
import {
  Text,
  View,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Keyboard,
} from "react-native";

import { LinearGradient } from "expo-linear-gradient";
import { AuthContext } from "../AuthProvider";

export default Login = ({ navigation }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { signIn } = useContext(AuthContext);

  return (
    <View style={styles.container}>
      <LinearGradient
        style={styles.background}
        colors={["skyblue", "dodgerblue"]}
      />
      <TextInput
        style={styles.inputfield}
        placeholder="E-mail"
        keyboardType={"email-address"}
        value={email}
        onChangeText={setEmail}
      ></TextInput>
      <TextInput
        style={styles.inputfield}
        placeholder="Password"
        textContentType={"password"}
        secureTextEntry={true}
        value={password}
        onChangeText={setPassword}
      ></TextInput>
      <TouchableOpacity
        activeOpacity={0.75}
        style={styles.button}
        onPress={() => signIn(email, password)}
      >
        <Text style={styles.buttonText}>Log in</Text>
      </TouchableOpacity>
      <Text
        style={{ color: "cyan" }}
        onPress={() => navigation.navigate("Register")}
      >
        Create an account?
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: "100%",
    height: "100%",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "dodgerblue",
  },
  background: {
    position: "absolute",
    width: "100%",
    height: "100%",
  },
  buttonText: {
    color: "oldlace",
    fontSize: 18,
  },
  inputfield: {
    width: "80%",
    height: "8%",
    margin: 10,
    borderRadius: 8,
    borderWidth: 0.5,
    backgroundColor: "oldlace",
    textAlign: "center",
  },
  button: {
    width: "36%",
    height: "6%",
    margin: 20,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 20,
    backgroundColor: "skyblue",
  },
});
