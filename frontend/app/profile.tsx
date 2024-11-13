import React, { useState, useEffect } from 'react';
import { View, Text, Image, StyleSheet, Button, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter, useSearchParams } from 'expo-router'; // Importando useSearchParams

const ProfileScreen = () => {
 // Pega o id do autor da URL
  const router = useRouter();
  const [userProfile, setUserProfile] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const token = await AsyncStorage.getItem('auth_token');
        if (!token) {
          router.replace('/login'); // Redireciona se o token não estiver presente
          return;
        }

        // Usando o author_id passado na URL para buscar o perfil do usuário
        const response = await fetch(`http://127.0.0.1:8000/api/profile/1/`, {
          method: 'GET',
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUserProfile(data);
        } else {
          setError('Failed to load profile');
        }
      } catch (error) {
        setError('Error fetching profile');
      } finally {
        setLoading(false);
      }
    }; fetchUserProfile(); // Chama a função de busca de perfil quando o author_id é encontrado
 
    
  },); // Executa o efeito sempre que o author_id mudar

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#f4511e" />
        <Text>Loading profile...</Text>
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
      {userProfile && (
        <>
          <Image
            source={{ uri: userProfile.photo }}
            style={styles.profileImage}
          />
          <Text style={styles.user}>{userProfile.user}</Text>
          <Text style={styles.bio}>{userProfile.bio}</Text>
        </>
      )}
      <Button title="Edit Profile" onPress={() => router.push('/edit-profile')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  profileImage: {
    width: 120,
    height: 120,
    borderRadius: 60,
    marginBottom: 20,
  },
  username: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  bio: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
    color: 'gray',
  },
  error: {
    color: 'red',
  },
});

export default ProfileScreen;
