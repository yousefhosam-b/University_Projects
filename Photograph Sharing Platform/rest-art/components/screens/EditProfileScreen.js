import React, { useEffect, useContext, useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  StyleSheet,
  Alert,
  Button,
  ImageBackground,
  Keyboard,
} from "react-native";

import MaterialCommunityIcons from "react-native-vector-icons/MaterialCommunityIcons";
import FontAwesome from "react-native-vector-icons/FontAwesome";

import Animated from "react-native-reanimated";
import BottomSheet from "reanimated-bottom-sheet";
import * as ImagePicker from "expo-image-picker";

import { AuthContext } from "../AuthProvider";
import { firestore, storage } from "../../firebase/config";

const EditProfileScreen = ({ navigation }) => {
  const { user } = useContext(AuthContext);
  const [image, setImage] = useState(null);
  const [userData, setUserData] = useState(null);
  const [updated, setUpdated] = useState(false);

  const getUserData = () => {
    firestore
      .collection("users")
      .doc(user.uid)
      .get()
      .then((data) => setUserData(data.data()))
      .catch((e) => null);
  };

  const handleUpdate = async () => {
    uploadImage();
  };

  const uploadImage = () => {
    if (image == null) {
      setUpdated(true);
      return;
    }

    const uploadUri = image;
    let filename = uploadUri.substring(uploadUri.lastIndexOf("/") + 1);

    // Add timestamp to File Name
    const extension = filename.split(".").pop();
    const name = filename.split(".").slice(0, -1).join(".");
    filename = name + Date.now() + "." + extension;

    fetch(uploadUri)
      .then((r) => r.blob())
      .then((f) =>
        storage
          .ref(`userposts/${user.uid}/profilepicture/${filename}`)
          .put(f, { contentType: "image/jpeg" })
          .then((snapshot) =>
            snapshot.ref.getDownloadURL().then(function (url) {
              console.log(url);
              setUserData({ ...userData, imageURL: url });
              setUpdated(true);
            })
          )
          .catch((e) => null)
      )
      .catch((e) => null);
  };

  useEffect(() => {
    getUserData();
  }, []);

  useEffect(() => {
    if (!updated) return;

    console.log(userData);
    firestore
      .collection("users")
      .doc(user.uid)
      .update({
        displayName: userData.displayName,
        email: userData.email,
        imageURL: userData.imageURL,
      })
      .then((s) => {
        Alert.alert(
          "Profile Updated!",
          "Your profile has been updated successfully."
        );
      })
      .catch((e) => null);

    setUpdated(false);

    navigation.goBack();
  }, [updated]);

  const takePhotoFromCamera = () => {
    ImagePicker.requestCameraPermissionsAsync()
      .then(() =>
        ImagePicker.getCameraPermissionsAsync().then((s) => {
          if (s.granted == true) {
            {
              ImagePicker.launchCameraAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: true,
                aspect: [1, 1],
                quality: 1,
              })
                .then((im) => {
                  if (im.cancelled == false) {
                    setImage(im.uri);
                    bs.current.snapTo(1);
                  }
                })
                .catch((e) => null);
            }
          } else
            Alert.alert(
              "Permission required!",
              "Please give permission to camera in order to access it."
            );
        })
      )
      .catch((e) => null);
  };

  const choosePhotoFromLibrary = () => {
    ImagePicker.requestMediaLibraryPermissionsAsync()
      .then(() =>
        ImagePicker.getMediaLibraryPermissionsAsync().then((s) => {
          if (s.granted == true) {
            {
              ImagePicker.launchImageLibraryAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: true,
                aspect: [1, 1],
                quality: 1,
              })
                .then((im) => {
                  if (im.cancelled == false) {
                    setImage(im.uri);
                    bs.current.snapTo(1);
                  }
                })
                .catch((e) => null);
            }
          } else
            Alert.alert(
              "Permission required!",
              "Please give permission to media library in order to access it."
            );
        })
      )
      .catch((e) => null);
  };

  const renderInner = () => (
    <View style={styles.panel}>
      <View style={{ alignItems: "center" }}>
        <Text style={styles.panelTitle}>Upload Photo</Text>
        <Text style={styles.panelSubtitle}>Choose Your Profile Picture</Text>
      </View>
      <TouchableOpacity
        style={styles.panelButton}
        onPress={takePhotoFromCamera}
      >
        <Text style={styles.panelButtonTitle}>Take Photo</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.panelButton}
        onPress={choosePhotoFromLibrary}
      >
        <Text style={styles.panelButtonTitle}>Choose From Library</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.panelButton}
        onPress={() => bs.current.snapTo(1)}
      >
        <Text style={styles.panelButtonTitle}>Cancel</Text>
      </TouchableOpacity>
    </View>
  );

  const renderHeader = () => (
    <View style={styles.header}>
      <View style={styles.panelHeader}>
        <View style={styles.panelHandle} />
      </View>
    </View>
  );

  const bs = React.useRef(null);
  const fall = new Animated.Value(1);

  return (
    <View style={styles.container}>
      <BottomSheet
        ref={bs}
        snapPoints={[330, -5]}
        renderContent={renderInner}
        renderHeader={renderHeader}
        initialSnap={1}
        callbackNode={fall}
        enabledGestureInteraction={true}
      />
      <View
        style={{
          margin: 20,
        }}
      >
        <View style={{ alignItems: "center" }}>
          <TouchableOpacity
            onPress={() => {
              bs.current.snapTo(0);
              Keyboard.dismiss();
            }}
          >
            <View
              style={{
                height: 100,
                width: 100,
                borderRadius: 15,
                marginTop: 20,
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <ImageBackground
                source={image ? { uri: image } : null}
                style={{
                  height: 100,
                  width: 100,
                  borderRadius: 50,
                  overflow: "hidden",
                  backgroundColor: "dodgerblue",
                }}
              >
                <View
                  style={{
                    flex: 1,
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                >
                  <MaterialCommunityIcons
                    name="camera"
                    size={35}
                    color="#fff"
                    style={{
                      opacity: 0.7,
                      alignItems: "center",
                      justifyContent: "center",
                      borderWidth: 1,
                      borderColor: "#fff",
                      borderRadius: 10,
                    }}
                  />
                </View>
              </ImageBackground>
            </View>
          </TouchableOpacity>
        </View>

        <View style={styles.action}>
          <FontAwesome name="user-o" color="#333333" size={20} />
          <TextInput
            placeholder="Full Name"
            placeholderTextColor="#666666"
            autoCorrect={false}
            value={userData ? userData.displayName : ""}
            onChangeText={(txt) =>
              setUserData({ ...userData, displayName: txt })
            }
            style={styles.textInput}
          />
        </View>
        <View style={styles.action}>
          <FontAwesome name="envelope" color="#333333" size={20} />
          <TextInput
            placeholder="Email Address"
            placeholderTextColor="#666666"
            value={userData ? userData.email : ""}
            onChangeText={(txt) => setUserData({ ...userData, email: txt })}
            autoCorrect={false}
            keyboardType="email-address"
            style={styles.textInput}
          />
        </View>
        <Button title={"Update"} onPress={handleUpdate}>
          Update
        </Button>
      </View>
    </View>
  );
};

export default EditProfileScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  panel: {
    padding: 20,
    backgroundColor: "#FFFFFF",
    paddingTop: 20,
    width: "100%",
  },
  header: {
    backgroundColor: "#FFFFFF",
    shadowColor: "#333333",
    shadowOffset: { width: -1, height: -3 },
    shadowRadius: 2,
    shadowOpacity: 0.4,
    paddingTop: 20,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  panelHeader: {
    alignItems: "center",
  },
  panelHandle: {
    width: 40,
    height: 8,
    borderRadius: 4,
    backgroundColor: "#00000040",
    marginBottom: 10,
  },
  panelTitle: {
    fontSize: 27,
    height: 35,
  },
  panelSubtitle: {
    fontSize: 14,
    color: "gray",
    height: 30,
    marginBottom: 10,
  },
  panelButton: {
    padding: 13,
    borderRadius: 10,
    backgroundColor: "#2e64e5",
    alignItems: "center",
    marginVertical: 7,
  },
  panelButtonTitle: {
    fontSize: 17,
    fontWeight: "bold",
    color: "white",
  },
  action: {
    flexDirection: "row",
    marginTop: 10,
    marginBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#f2f2f2",
    paddingBottom: 5,
  },
  textInput: {
    flex: 1,
    marginTop: Platform.OS === "ios" ? 0 : -12,
    height: 30,
    paddingLeft: 10,
    color: "#333333",
  },
});
