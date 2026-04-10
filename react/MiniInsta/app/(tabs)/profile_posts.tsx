import { useCallback, useState } from 'react';
import { ScrollView, SafeAreaView, Text, View, Pressable, Image } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { styles } from '../../assets/styles/my_styles';
import { clearAuthData, getAuthData } from '../auth_store';

type Profile = {
  id: number;
  username: string;
  display_name: string;
  bio_text: string;
};

type Post = {
  id: number;
  caption: string;
  timestamp: string;
  photos?: { id: number; image: string; timestamp: string }[];
};

import { API_BASE } from '../api_config';

export default function ProfilePostsScreen() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [message, setMessage] = useState('Log in from the Login tab first.');

  const loadData = useCallback(async () => {
    // Pull profile + own posts using saved token/profile id.
    const auth = getAuthData();
    if (!auth.token || !auth.profileId) {
      setMessage('Missing token/profile. Please log in.');
      setProfile(null);
      setPosts([]);
      return;
    }

    try {
      const headers = { Authorization: `Token ${auth.token}` };

      const [pRes, postsRes] = await Promise.all([
        fetch(`${API_BASE}/api/profile/${auth.profileId}`, { headers }),
        fetch(`${API_BASE}/api/profile/${auth.profileId}/posts`, { headers }),
      ]);

      // If token fails, clear and ask user to log in again.
      if (pRes.status === 401 || postsRes.status === 401) {
        clearAuthData();
        setMessage('Token expired/invalid. Log in again.');
        return;
      }

      const pJson = await pRes.json();
      const postsJson = await postsRes.json();

      setProfile(pJson);
      setPosts(postsJson);
      setMessage(`Logged in as ${auth.username}`);
    } catch (error) {
      console.log('Profile/posts error:', error);
      setMessage('Network error loading profile/posts.');
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      loadData();
    }, [loadData])
  );

  return (
    <SafeAreaView style={styles.screen}>
      <ScrollView contentContainerStyle={styles.contentWrap}>
        <Text style={styles.titleText}>My Profile + Posts</Text>
        <Text style={styles.metaText}>{message}</Text>

        {profile ? (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>{profile.display_name}</Text>
            <Text style={styles.bodyText}>@{profile.username}</Text>
            <Text style={styles.bodyText}>{profile.bio_text}</Text>
          </View>
        ) : null}

        {posts.map((post) => (
          <View style={styles.card} key={post.id}>
            <Text style={styles.bodyText}>{post.caption || '(No caption)'}</Text>
            {post.photos?.[0]?.image ? (
              <Image source={{ uri: post.photos[0].image }} style={styles.mainImage} resizeMode="cover" />
            ) : null}
            <Text style={styles.metaText}>{post.timestamp}</Text>
          </View>
        ))}

        <Pressable style={styles.button} onPress={loadData}>
          <Text style={styles.buttonText}>Refresh</Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}
