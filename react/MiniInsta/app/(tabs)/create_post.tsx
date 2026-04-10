import { useState } from 'react';
import { Pressable, SafeAreaView, Text, TextInput, View } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { clearAuthData, getAuthData } from '../auth_store';

import { API_BASE } from '../api_config';

export default function CreatePostScreen() {
  const [caption, setCaption] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [message, setMessage] = useState('');

  async function submitPost() {
    // Create a post using caption + optional image URL.
    const auth = getAuthData();
    if (!auth.token) {
      setMessage('Please log in first.');
      return;
    }

    try {
      console.log('POST /api/posts payload:', { caption, image_url: imageUrl });

      const response = await fetch(`${API_BASE}/api/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${auth.token}`,
        },
        body: JSON.stringify({ caption, image_url: imageUrl }),
      });

      const json = await response.json();
      console.log('POST /api/posts response:', response.status, json);

      if (response.status === 401) {
        clearAuthData();
        setMessage('Token expired/invalid. Log in again.');
        return;
      }

      if (!response.ok) {
        setMessage(json.detail ?? 'Could not create post.');
        return;
      }

      setCaption('');
      setImageUrl('');
      setMessage('Post created successfully.');
    } catch (error) {
      console.log('Create post error:', error);
      setMessage('Network error creating post.');
    }
  }

  return (
    <SafeAreaView style={styles.screen}>
      <View style={styles.contentWrap}>
        <Text style={styles.titleText}>Create Post</Text>

        <TextInput
          placeholder="Caption"
          value={caption}
          onChangeText={setCaption}
          style={styles.input}
          multiline
        />

        <TextInput
          placeholder="Image URL (optional)"
          value={imageUrl}
          onChangeText={setImageUrl}
          style={styles.input}
          autoCapitalize="none"
        />

        <Pressable style={styles.button} onPress={submitPost}>
          <Text style={styles.buttonText}>Submit</Text>
        </Pressable>

        {message ? <Text style={styles.metaText}>{message}</Text> : null}
      </View>
    </SafeAreaView>
  );
}
