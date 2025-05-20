import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  TextInput,
  View,
  Button,
  Image,
  ActivityIndicator,
  ScrollView,
  Platform,
} from 'react-native';
import { Video } from 'expo-av';

export default function App() {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  // NOTE: Change URL below to local IP when testing on phone. Leave as is when testing on PC.
  const SERVER_URL = 'http://localhost:5000';

  const handleGenerate = async () => {
    if (!prompt.trim()) return;


    setLoading(true);
    setImageUrl(null);
    setVideoUrl(null);
    setErrorMsg(null);

    try {
      const response = await fetch(`${SERVER_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();

      if (data.image_url) {
        setImageUrl(data.image_url);
      } else if (data.video_url) {
        setVideoUrl(data.video_url);
      } else {
        setErrorMsg('No Media Returned ');
      }
    } catch (err) {
      setErrorMsg('Error Connecting to Server ');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Text to Media Generator</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter a prompt..."
        value={prompt}
        onChangeText={setPrompt}
      />
      <Button title="Generate" onPress={handleGenerate} />

      {loading && <ActivityIndicator size="large" color="#007AFF" style={{ marginTop: 20}} />}
      {errorMsg && <Text style={styles.error}>{errorMsg}</Text>}

      {imageUrl && (
        <Image
          source={{ uri: imageUrl }}
          style={styles.media}
          resizeMode="contain"
        />
      )}

      {videoUrl && (
        <Video
          source={{ uri: videoUrl }}
          style={styles.media}
          useNativeControls
          resizeMode="contain"
          isLooping
        />
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === 'android' ? 50 : 80,
    paddingBottom: 50,
    paddingHorizontal: 16,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    width: '100%',
    padding: 12,
    borderRadius: 8,
    marginBottom: 12,
  },
  media: {
    width: '100%',
    height: 300,
    marginTop:20,
    borderRadius: 10,
  },
  error: {
    color: 'red',
    marginTop: 10,
  },
});