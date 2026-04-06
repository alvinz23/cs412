import { useCallback, useEffect, useState } from 'react';
import { Image, Pressable, SafeAreaView, ScrollView, Text, View } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

type Joke = {
  id: number;
  text: string;
  contributor: string;
  created_at: string;
};

type Picture = {
  id: number;
  image_url: string;
  contributor: string;
  created_at: string;
};

const API_BASE = 'http://10.239.67.127:8000/cs412/dadjokes';

export default function IndexScreen() {
  const [joke, setJoke] = useState<Joke | null>(null);
  const [picture, setPicture] = useState<Picture | null>(null);
  const [error, setError] = useState('');

  const loadRandom = useCallback(async () => {
    try {
      setError('');
      const [jokeRes, pictureRes] = await Promise.all([
        fetch(`${API_BASE}/api/random`),
        fetch(`${API_BASE}/api/random_picture`),
      ]);

      if (!jokeRes.ok || !pictureRes.ok) {
        throw new Error('Could not load random content.');
      }

      const jokeJson: Joke = await jokeRes.json();
      const pictureJson: Picture = await pictureRes.json();
      setJoke(jokeJson);
      setPicture(pictureJson);
    } catch (err) {
      setError('Failed to load from API. Confirm Django server is running.');
      console.log('Index API error:', err);
    }
  }, []);

  useEffect(() => {
    loadRandom();
  }, [loadRandom]);

  return (
    <SafeAreaView style={styles.screen}>
      <ScrollView contentContainerStyle={styles.contentWrap}>
        <Text style={styles.titleText}>DadJokes OS</Text>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Random Joke</Text>
          <Text style={styles.bodyText}>{joke?.text ?? 'Loading joke...'}</Text>
          <Text style={styles.metaText}>{joke ? `By ${joke.contributor}` : ''}</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Random Picture</Text>
          {picture?.image_url ? (
            <Image source={{ uri: picture.image_url }} style={styles.mainImage} resizeMode="cover" />
          ) : (
            <Text style={styles.bodyText}>Loading picture...</Text>
          )}
          <Text style={styles.metaText}>{picture ? `By ${picture.contributor}` : ''}</Text>
        </View>

        {error ? <Text style={styles.errorText}>{error}</Text> : null}

        <Pressable style={styles.button} onPress={loadRandom}>
          <Text style={styles.buttonText}>Refresh Random</Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}
