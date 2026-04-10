import { useState } from 'react';
import { Pressable, SafeAreaView, Text, TextInput, View } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { setAuthData } from '../auth_store';

import { API_BASE } from '../api_config';

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  async function handleLogin() {
    // Login call to Django API. Returns token if creds are good.
    setMessage('');

    try {
      const response = await fetch(`${API_BASE}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail ?? 'Login failed.');
        return;
      }

      setAuthData({
        token: data.token,
        profileId: data.profile_id,
        username: data.username,
      });

      // We keep it simple: just show success text and use other tabs.
      setMessage('Login successful.');
    } catch (error) {
      console.log('Login error:', error);
      setMessage('Network error during login.');
    }
  }

  return (
    <SafeAreaView style={styles.screen}>
      <View style={styles.contentWrap}>
        <Text style={styles.titleText}>MiniInsta Login</Text>

        <TextInput
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
          style={styles.input}
          autoCapitalize="none"
        />

        <TextInput
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          style={styles.input}
          secureTextEntry
        />

        <Pressable style={styles.button} onPress={handleLogin}>
          <Text style={styles.buttonText}>Login</Text>
        </Pressable>

        {message ? <Text style={styles.metaText}>{message}</Text> : null}
      </View>
    </SafeAreaView>
  );
}
