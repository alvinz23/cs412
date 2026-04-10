import { useCallback, useState } from 'react';
import { ScrollView, SafeAreaView, Text, View, Pressable, Image } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { styles } from '../../assets/styles/my_styles';
import { clearAuthData, getAuthData } from '../auth_store';

type Photo = {
  id: number;
  image: string;
};

type Post = {
  id: number;
  profile_display_name: string;
  caption: string;
  timestamp: string;
  photos: Photo[];
};

import { API_BASE } from '../api_config';

export default function FeedScreen() {
  const [feed, setFeed] = useState<Post[]>([]);
  const [message, setMessage] = useState('Log in from the Login tab first.');

  const loadFeed = useCallback(async () => {
    // Feed endpoint for current logged-in profile.
    const auth = getAuthData();
    if (!auth.token || !auth.profileId) {
      setMessage('Missing token/profile. Please log in.');
      setFeed([]);
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/profile/${auth.profileId}/feed`, {
        headers: { Authorization: `Token ${auth.token}` },
      });

      if (response.status === 401) {
        clearAuthData();
        setMessage('Token expired/invalid. Log in again.');
        return;
      }

      const json = await response.json();
      setFeed(json);
      setMessage(`Feed loaded: ${json.length} posts`);
    } catch (error) {
      console.log('Feed error:', error);
      setMessage('Network error loading feed.');
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      loadFeed();
    }, [loadFeed])
  );

  return (
    <SafeAreaView style={styles.screen}>
      <ScrollView contentContainerStyle={styles.contentWrap}>
        <Text style={styles.titleText}>Feed</Text>
        <Text style={styles.metaText}>{message}</Text>

        {feed.map((post) => (
          <View style={styles.card} key={post.id}>
            <Text style={styles.cardTitle}>{post.profile_display_name}</Text>
            <Text style={styles.bodyText}>{post.caption || '(No caption)'}</Text>
            {post.photos?.[0]?.image ? (
              <Image source={{ uri: post.photos[0].image }} style={styles.mainImage} resizeMode="cover" />
            ) : null}
            <Text style={styles.metaText}>{post.timestamp}</Text>
          </View>
        ))}

        <Pressable style={styles.button} onPress={loadFeed}>
          <Text style={styles.buttonText}>Refresh Feed</Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}
