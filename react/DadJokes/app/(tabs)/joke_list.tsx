import { useEffect, useState } from 'react';
import { FlatList, SafeAreaView, Text, View } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

type Joke = {
  id: number;
  text: string;
  contributor: string;
  created_at: string;
};

const API_BASE = 'http://10.239.67.127:8000/cs412/dadjokes';

export default function JokeListScreen() {
  const [jokes, setJokes] = useState<Joke[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadJokes() {
      try {
        setError('');
        const response = await fetch(`${API_BASE}/api/jokes`);
        if (!response.ok) {
          throw new Error('Could not load jokes.');
        }
        const json: Joke[] = await response.json();
        setJokes(json);
      } catch (err) {
        setError('Failed to load jokes from API.');
        console.log('Joke list API error:', err);
      }
    }

    loadJokes();
  }, []);

  return (
    <SafeAreaView style={styles.screen}>
      <View style={styles.contentWrap}>
        <Text style={styles.titleText}>All Jokes</Text>
        {error ? <Text style={styles.errorText}>{error}</Text> : null}

        <FlatList
          data={jokes}
          keyExtractor={(item) => String(item.id)}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text style={styles.bodyText}>{item.text}</Text>
              <Text style={styles.metaText}>By {item.contributor}</Text>
            </View>
          )}
          contentContainerStyle={styles.listWrap}
        />
      </View>
    </SafeAreaView>
  );
}
