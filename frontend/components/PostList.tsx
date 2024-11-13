import { RefreshControl, FlatList, View } from "react-native";
import PostItem from "./PostItem";

const PostList = ({ data }) => {
  const renderItem = ({ item }) => (
    <PostItem id={item.id} title={item.title} subscription={item.subscription} author={item.author} photo_post={item.photo_post} comments={item.comments} likes_count={item.likes_count} author_id={item.author_id} author_photo={item.author_photo}/>
  );

  return (
    <View>
      <FlatList
        data={data}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderItem}
        refreshControl={
          <RefreshControl
            refreshing={false}
            onRefresh={() => console.log("refreshing...")}
          />
        }
      />
    </View>
  );
};

export default PostList;
