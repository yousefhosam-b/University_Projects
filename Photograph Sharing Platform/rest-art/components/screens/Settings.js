import React, { useContext } from "react";

import { Button, Keyboard, StyleSheet, Text, View } from "react-native";
import { ScrollView, TouchableHighlight } from "react-native-gesture-handler";
import { createStackNavigator } from "@react-navigation/stack";
import { AuthContext } from "../AuthProvider";

import EditProfileScreen from "./EditProfileScreen";

export default Settings = () => {
  const { user, signOut } = useContext(AuthContext);

  const Stack = createStackNavigator();

  const SettingsScreen = ({ navigation }) => {
    return (
      <View>
        <Text
          style={{
            marginTop: 50,
            marginHorizontal: 50,
            fontSize: 32,
          }}
        >
          Settings
        </Text>
        <ScrollView style={styles.container}>
          <TouchableHighlight
            style={styles.button}
            activeOpacity={0.9}
            underlayColor={"deepskyblue"}
            onPress={() => navigation.navigate("EditProfileScreen")}
          >
            <Text style={styles.buttonText}>Edit Profile</Text>
          </TouchableHighlight>
          <TouchableHighlight
            style={styles.button}
            activeOpacity={0.9}
            underlayColor={"deepskyblue"}
            onPress={() => null}
          >
            <Text style={styles.buttonText}>Give us a Feedback</Text>
          </TouchableHighlight>
          <TouchableHighlight
            style={styles.button}
            activeOpacity={0.9}
            underlayColor={"deepskyblue"}
            onPress={signOut}
          >
            <Text style={styles.buttonText}>Sign Out</Text>
          </TouchableHighlight>
        </ScrollView>
      </View>
    );
  };

  return (
    <Stack.Navigator initialRouteName={"SettingsScreen"}>
      <Stack.Screen
        name="SettingsScreen"
        component={SettingsScreen}
        options={{ header: () => null }}
      />
      <Stack.Screen
        name="EditProfileScreen"
        component={EditProfileScreen}
        options={{ header: () => null }}
      />
    </Stack.Navigator>
  );
};

const styles = StyleSheet.create({
  container: {
    marginVertical: 30,
    borderRadius: 20,
  },
  button: {
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "skyblue",
    height: 60,
    marginBottom: 1,
  },
  buttonText: {
    fontSize: 18,
    color: "white",
  },
});
