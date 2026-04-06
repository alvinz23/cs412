import { useState } from 'react';
import { Alert, Pressable, SafeAreaView, Text, TextInput, View } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

const API_BASE = 'http://10.239.67.127:8000/cs412/dadjokes';

export default function AddJokeScreen() {
  const [text, setText] = useState('');
  const [contributor, setContributor] = useState('');
  const [message, setMessage] = useState('');

  async function submitJoke() {
    if (!text.trim() || !contributor.trim()) {
      setMessage('Please enter both joke text and contributor.');
      return;
    }

    try {
      console.log('POST /api/jokes payload:', { text, contributor });
      const response = await fetch(`${API_BASE}/api/jokes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, contributor }),
      });

      const json = await response.json();
      console.log('POST /api/jokes response:', response.status, json);

      if (!response.ok) {
        throw new Error('Could not submit joke.');
      }

      setText('');
      setContributor('');
      setMessage('Joke submitted successfully.');
      Alert.alert('Success', 'Your joke was posted.');
    } catch (err) {
      setMessage('Submission failed. Check API/server and try again.');
      console.log('Add joke API error:', err);
    }
  }

  return (
    <SafeAreaView style={styles.screen}>
      <View style={styles.contentWrap}>
        <Text style={styles.titleText}>Add Joke</Text>

        <TextInput
          placeholder="Enter your joke"
          value={text}
          onChangeText={setText}
          style={styles.input}
          multiline
        />

        <TextInput
          placeholder="Contributor name"
          value={contributor}
          onChangeText={setContributor}
          style={styles.input}
        />

        <Pressable style={styles.button} onPress={submitJoke}>
          <Text style={styles.buttonText}>Submit Joke</Text>
        </Pressable>

        {message ? <Text style={styles.metaText}>{message}</Text> : null}
      </View>
    </SafeAreaView>
  );
}
