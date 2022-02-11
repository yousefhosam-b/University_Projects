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

import Animated from "react-native-reanimated";
import BottomSheet from "reanimated-bottom-sheet";
import * as ImagePicker from "expo-image-picker";

import * as firebase from "firebase";

import { AuthContext } from "../AuthProvider";
import { firestore, storage } from "../../firebase/config";
import { LinearGradient } from "expo-linear-gradient";

const SharePostScreen = ({ navigation }) => {
  const { user } = useContext(AuthContext);
  const [image, setImage] = useState(null);
  const [post, setPost] = useState(null);
  const [updated, setUpdated] = useState(false);

  const handleUpload = async () => {
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
          .ref(`userposts/${user.uid}/sharedposts/${filename}`)
          .put(f, { contentType: "image/jpeg" })
          .then((snapshot) =>
            snapshot.ref.getDownloadURL().then(function (url) {
              setPost({ ...post, imageURL: url });
              setUpdated(true);
            })
          )
          .catch((e) => null)
      )
      .catch((e) => null);
  };

  useEffect(() => {
    if (!updated) return;

    firestore
      .collection("users")
      .doc(user.uid)
      .collection("sharedposts")
      .add({
        postName: post.postName,
        imageURL: post.imageURL,
        publishDate: firebase.firestore.FieldValue.serverTimestamp(),
        likes: 0,
        dislikes: 0,
      })
      .then((doc) => {
        doc.update({
          postid: `${doc.id}${user.uid}`,
        });
        Alert.alert("Post Shared!", "Your post has been shared successfully.");
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
                aspect: [3, 4],
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
                aspect: [3, 4],
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
        <View style={{ alignItems: "center", marginVertical: 50 }}>
          <TouchableOpacity
            activeOpacity={0.9}
            onPress={() => {
              bs.current.snapTo(0);
              Keyboard.dismiss();
            }}
          >
            <ImageBackground
              style={[
                styles.image,
                image
                  ? null
                  : {
                      borderColor: "black",
                      borderWidth: 2,
                      backgroundColor: "hsl(200,80%,80%)",
                    },
              ]}
              source={{ uri: image }}
            >
              <LinearGradient
                colors={["rgba(0,0,0,0.75)", "rgba(0,0,0,0.25)"]}
                style={{ height: "14%", justifyContent: "center" }}
              >
                <TextInput
                  placeholder="Title..."
                  placeholderTextColor="#bbb"
                  autoCapitalize="words"
                  autoCorrect={false}
                  value={post ? post.postName : ""}
                  onChangeText={(txt) => setPost({ ...post, postName: txt })}
                  style={[styles.imageHeader, { flex: 1 }]}
                />
              </LinearGradient>
              <MaterialCommunityIcons
                name="camera"
                size={80}
                color={image ? "transparent" : "black"}
                style={{
                  paddingVertical: 120,
                  alignSelf: "center",
                  opacity: 0.7,
                  alignItems: "center",
                  justifyContent: "center",
                }}
              />
            </ImageBackground>
          </TouchableOpacity>
        </View>
        <Button title={"Share"} onPress={handleUpload}></Button>
      </View>
    </View>
  );
};

export default SharePostScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  image: {
    resizeMode: "cover",
    width: 300,
    height: 400,
    overflow: "hidden",
    borderRadius: 20,
  },
  imageHeader: {
    marginLeft: 20,
    fontSize: 24,
    fontWeight: "bold",
    color: "white",
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
});
