import { createStackNavigator } from "@react-navigation/stack";
import React, { useContext, useEffect, useState } from "react";

import {
  Dimensions,
  Image,
  ImageBackground,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { ScrollView, TouchableHighlight } from "react-native-gesture-handler";
import Icon from "react-native-vector-icons/FontAwesome";

import { firestore } from "../../firebase/config";

import { AuthContext } from "../AuthProvider";
import SharePostScreen from "./SharePostScreen";

export default Profile = ({ navigation }) => {
  const { user } = useContext(AuthContext);
  const [postCount, setPostCount] = useState("");
  const [rating, setRating] = useState(0);
  const [userData, setUserData] = useState(null);

  const [posts, setPosts] = useState([]);

  const Stack = createStackNavigator();

  const getUserData = () => {
    firestore
      .collection("users")
      .doc(user.uid)
      .get()
      .then((data) => setUserData(data.data()));
  };

  const fetchPosts = () => {
    firestore
      .collection("users")
      .doc(user.uid)
      .collection("sharedposts")
      .orderBy("publishDate", "desc")
      .get()
      .then((data) => {
        setPostCount(data.size);
        setPosts([]);
        let liked = 0;
        let rated = 0;
        data.forEach((doc) => {
          rated += doc.data().dislikes + doc.data().likes;
          liked += doc.data().likes;
          setPosts((posts) => [
            ...posts,
            <ImageBackground
              key={doc.id}
              style={styles.postPreview}
              source={{ uri: doc.data().imageURL }}
            ></ImageBackground>,
          ]);
        });
        setRating(rated == 0 ? 0 : ((5 * liked) / rated).toFixed(1));
      });
  };

  useEffect(() => {
    navigation.addListener("focus", () => {
      getUserData();
      fetchPosts();
    });
  }, [navigation]);

  const ProfileScreen = () => (
    <View style={{ minHeight: Dimensions.get("screen").height }}>
      <ScrollView>
        <View style={styles.container}>
          <Image source={{ uri: userData?.imageURL }} style={styles.picture} />
          <Text style={{ fontSize: 32, paddingVertical: 10 }}>
            {userData?.displayName}
          </Text>
          <View style={styles.profileDetailsContainer}>
            <View style={{ alignItems: "center" }}>
              <Text style={{ fontSize: 24 }}>{postCount}</Text>
              <Text style={{ fontSize: 16 }}>Posts</Text>
            </View>
            <View style={{ alignItems: "center" }}>
              <Text style={{ fontSize: 24 }}>{rating}</Text>
              <Text style={{ fontSize: 16 }}>Average Rating</Text>
            </View>
          </View>
          <View style={styles.postContainer}>
            <TouchableHighlight
              underlayColor="rgba(0,0,0,0.1)"
              style={[
                styles.postPreview,
                {
                  alignItems: "center",
                  justifyContent: "center",
                  borderColor: "gray",
                  borderWidth: 1,
                },
              ]}
              onPress={() => navigation.navigate("SharePostScreen")}
            >
              <Icon name="camera" color="gray" size={30}></Icon>
            </TouchableHighlight>
            {posts}
          </View>
        </View>
      </ScrollView>
    </View>
  );

  return (
    <Stack.Navigator initialRouteName="ProfileScreen">
      <Stack.Screen
        name="ProfileScreen"
        component={ProfileScreen}
        options={{ header: () => null }}
      />
      <Stack.Screen
        name="SharePostScreen"
        component={SharePostScreen}
        options={{ header: () => null }}
      />
    </Stack.Navigator>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    paddingTop: 50,
  },
  picture: {
    overflow: "hidden",
    width: 120,
    height: 120,
    borderRadius: 60,
  },
  profileDetailsContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    width: 250,
    marginBottom: 10,
  },
  postContainer: {
    flex: 1,
    flexDirection: "row",
    flexWrap: "wrap",
    width: Dimensions.get("screen").width,
  },
  postPreview: {
    width: 120,
    height: 120,
    borderRadius: 15,
    overflow: "hidden",
    resizeMode: "cover",
    margin: 2.5,
  },
});
