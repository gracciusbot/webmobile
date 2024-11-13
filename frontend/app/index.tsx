// /app/index.tsx
import { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';
import PostList  from '../components/PostList';

const Index = () => {
  const router = useRouter();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true; // Flag para verificar se o componente ainda está montado

    const checkAuth = async () => {
      const token = await AsyncStorage.getItem('auth_token');
      if (!token) {
        router.replace('/login');
        return;
      } else {
        fetchData(token);  // Passe o token para a função
      }
    };

    checkAuth();

    return () => {
      isMounted = false;
    };
  }, []);

  const fetchData = async (token: string) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/posts/', {
        method: 'GET',
        headers: {
          Authorization: `Token ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.status === 401) {
        setError('Unauthorized access. Please log in again.');
        router.replace('/login');
        return;
      } else if (!response.ok) {
        throw new Error('Failed to load posts');
      }

      const data = await response.json();
      setData(data);
    } catch (error: any) {
      setError(error.message || 'Error fetching posts');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#f4511e" />
        <Text>Loading posts...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container}>
        <Text style={styles.error}>{error}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView>
        <Text>Posts:</Text>
        <PostList data={data} />
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  error: {
    color: 'red',
    textAlign: 'center',
  },
});

export default Index;
