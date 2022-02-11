import { LinearGradient } from "expo-linear-gradient";
import React, { useContext, useState, useEffect } from "react";

import {
  Dimensions,
  ImageBackground,
  Keyboard,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { TouchableHighlight } from "react-native-gesture-handler";
import Icon from "react-native-vector-icons/FontAwesome";

import * as firebase from "firebase";
import { firestore } from "../../firebase/config";

import Animated, { Easing } from "react-native-reanimated";

export default Discover = () => {
  const [post, setPost] = useState(null);
  const [rated, setRated] = useState(false);
  const [waiting, setWaiting] = useState(true);

  const translateValue = useState(new Animated.Value(0))[0];
  const scaleValue = useState(new Animated.Value(0))[0];

  useEffect(() => {
    if (!post) getPost();
  });

  const randomId = () => {
    const CHARS =
      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    let autoId = "";

    for (let i = 0; i < 50; i++) {
      autoId += CHARS.charAt(Math.floor(Math.random() * CHARS.length));
    }
    return autoId;
  };

  const getPost = () => {
    Animated.timing(scaleValue, {
      toValue: 0,
      duration: 0,
      easing: Easing.ease,
      useNativeDriver: true,
    }).start();
    Animated.timing(translateValue, {
      toValue: 0,
      duration: 50,
      easing: Easing.ease,
      useNativeDriver: true,
    }).start(() => {
      setWaiting(false);
    });
    firestore
      .collectionGroup("sharedposts")
      .orderBy("postid")
      .startAt(randomId())
      .limit(1)
      .get()
      .then((data) => {
        data.forEach((doc) => {
          setPost(doc.data());
        });
      });
  };

  const ratePost = (liked) => {
    if (!post || waiting) return;

    if (liked) {
      firestore
        .collection("users")
        .doc(post.publishedBy)
        .collection("sharedposts")
        .where("publishDate", "==", post.publishDate)
        .limit(1)
        .get()
        .then((data) =>
          data.forEach((doc) => {
            doc.ref.update({
              likes: firebase.firestore.FieldValue.increment(1),
            });
          })
        );
    } else {
      firestore
        .collection("users")
        .doc(post.publishedBy)
        .collection("sharedposts")
        .where("publishDate", "==", post.publishDate)
        .limit(1)
        .get()
        .then((data) =>
          data.forEach((doc) => {
            doc.ref.update({
              dislikes: firebase.firestore.FieldValue.increment(1),
            });
          })
        );
    }
    Animated.timing(translateValue, {
      toValue: liked ? 500 : -500,
      duration: 200,
      easing: Easing.ease,
      useNativeDriver: true,
    }).start(() => {
      setWaiting(true);
      getPost();
    });
  };

  return (
    <View style={styles.container}>
      {post && (
        <Animated.View
          style={{
            transform: [
              {
                scale: scaleValue,
              },
              {
                translateX: translateValue,
              },
            ],
          }}
        >
          <ImageBackground
            style={styles.image}
            source={{ uri: post.imageURL }}
            onLoadEnd={() => {
              Animated.timing(scaleValue, {
                toValue: 1,
                duration: 200,
                easing: Easing.ease,
                useNativeDriver: true,
              }).start();
            }}
          >
            <LinearGradient
              colors={["rgba(0,0,0,0.75)", "rgba(0,0,0,0.25)"]}
              style={{ height: "12%", justifyContent: "center" }}
            >
              <Text style={styles.imageHeader}>{post.postName}</Text>
            </LinearGradient>
          </ImageBackground>
        </Animated.View>
      )}
      <View style={{ flexDirection: "row" }}>
        <TouchableHighlight
          style={{
            width: 70,
            height: 70,
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "rgba(0,0,0,0.75)",
            borderRadius: 35,
            marginHorizontal: 20,
            marginBottom: 30,
            transform: [{ scaleX: -1 }],
          }}
          onPress={() => ratePost(false)}
        >
          <Icon
            name="thumbs-down"
            color="rgb(255,0,0)"
            size={40}
            backgroundColor="rgba(0,0,0,0.5)"
            borderRadius={0}
          />
        </TouchableHighlight>
        <TouchableHighlight
          style={{
            width: 50,
            height: 50,
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "rgba(0,0,0,0.75)",
            borderRadius: 25,
            marginTop: 10,
            marginBottom: 30,
          }}
          onPress={() => getPost()}
        >
          <Icon
            name="repeat"
            color="rgb(255,255,255)"
            size={25}
            backgroundColor="rgba(0,0,0,0.5)"
            borderRadius={0}
          />
        </TouchableHighlight>
        <TouchableHighlight
          style={{
            width: 70,
            height: 70,
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "rgba(0,0,0,0.75)",
            borderRadius: 35,
            marginHorizontal: 20,
            marginBottom: 30,
          }}
          onPress={() => ratePost(true)}
        >
          <Icon
            name="thumbs-up"
            color="rgb(0,255,0)"
            size={40}
            backgroundColor="rgba(0,0,0,0.5)"
            borderRadius={0}
          />
        </TouchableHighlight>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "flex-end",
    alignItems: "center",
  },
  image: {
    resizeMode: "cover",
    width: 300,
    height: 400,
    overflow: "hidden",
    borderRadius: 20,
    marginVertical: 30,
  },
  imageHeader: {
    marginLeft: 20,
    fontSize: 24,
    fontWeight: "bold",
    color: "white",
  },
});
