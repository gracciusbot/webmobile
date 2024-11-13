import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useState, useRef } from 'react';
import { TouchableOpacity, Text, StyleSheet, Image, View, TextInput, Alert, Dimensions, SafeAreaView, ScrollView } from 'react-native';
import { useRouter } from 'expo-router'; // Importando o hook de navegação

const { width } = Dimensions.get('window');

const PostItem = ({ id, title, subscription, author, author_photo, photo_post, likes_count, token, comments, author_id, isFollowing }) => {
  const [likes, setLikes] = useState(likes_count);
  const [isLiked, setIsLiked] = useState(false);
  const [following, setFollowing] = useState(isFollowing);
  const [newComment, setNewComment] = useState('');
  const [currentComments, setCurrentComments] = useState(comments || []);
  const commentInputRef = useRef(null); // Ref para o campo de input de comentário
  const router = useRouter(); // Inicializando o hook de navegação
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const token = await AsyncStorage.getItem('auth_token');
        if (!token) {
          router.replace('/login'); // Redireciona se o token não estiver presente
          return;
        }

        // Usando o author_id passado na URL para buscar o perfil do usuário
        const response = await fetch(`http://127.0.0.1:8000/api/profile/`, {
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
    };

    if (author_id) {
      fetchUserProfile(); // Chama a função de busca de perfil quando o author_id é encontrado
    } else {
      setError('User ID not found');
      setLoading(false);
    }
  }, [author_id]); // Executa o efeito sempre que o author_id mudar

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

  // Função para enviar o comentário
  const handleAddComment = async () => {
    if (!newComment.trim()) {
      Alert.alert("Erro", "Por favor, insira um comentário válido.");
      return;
    }
    try {
      const token = await AsyncStorage.getItem('auth_token');
      const response = await fetch(`http://127.0.0.1:8000/api/posts/${id}/comments/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: newComment }),
      });

      if (response.ok) {
        const responseData = await response.json();
        setCurrentComments([...currentComments, responseData]);
        setNewComment('');
      } else {
        Alert.alert("Erro", "Não foi possível adicionar o comentário.");
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      Alert.alert("Erro", "Ocorreu um erro ao enviar o comentário.");
    }
  };

  // Função para ativar o campo de comentário ao clicar no botão de comentário
  const handleCommentButtonPress = () => {
    commentInputRef.current.focus();
  };

  const toggleLike = async () => {
    try {
      const token = await AsyncStorage.getItem('auth_token');
      const response = await fetch(`http://127.0.0.1:8000/api/posts/${id}/like/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const responseData = await response.json();
        setLikes(responseData.likes_count);
        setIsLiked(!isLiked);
      } else {
        console.error("Erro ao tentar curtir o post.");
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
    }
  };

  const toggleFollow = async () => {
    try {
      const token = await AsyncStorage.getItem('auth_token');
      const response = await fetch(`http://127.0.0.1:8000/api/follow/${author_id}/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const responseData = await response.json();
        setFollowing(responseData.is_following);
      } else {
        console.error("Erro ao tentar seguir/deseguir o autor.");
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
    }
  };

  // Função para navegar até o perfil do autor
  const goToAuthorProfile = () => {
    router.push(`/profile/${author_id}`); // Navegar para o perfil do autor usando o author_id
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <TouchableOpacity style={styles.card} onPress={() => {}}>
          <View style={styles.authorContainer}>
            {author_photo && (
              <>
                <Image source={{ uri: author_photo }} style={styles.authorPhoto} />
                <TouchableOpacity onPress={goToAuthorProfile}>
                  <Text style={styles.authorName}>{author}</Text> {/* Nome do autor que leva ao perfil */}
                </TouchableOpacity>
              </>
            )}
            <TouchableOpacity onPress={toggleFollow} style={styles.followButton}>
              <Text style={styles.followButtonText}>{following ? 'Unfollow' : 'Follow'}</Text>
            </TouchableOpacity>
          </View>

          {photo_post && (
            <Image source={{ uri: photo_post }} style={styles.image} />
          )}

          <Text style={styles.title}>{title}</Text>
          <Text style={styles.subscription}>{subscription}</Text>
          <Text style={styles.likes}>Likes: {likes}</Text>

          <View style={styles.buttonContainer}>
            <TouchableOpacity onPress={toggleLike} style={styles.likeButton}>
              <Text style={styles.likeButtonText}>{isLiked ? 'Unlike' : 'Like'}</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => commentInputRef.current.focus()} style={styles.commentButton}>
              <Text style={styles.commentButtonText}>Comentar</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.commentsSection}>
            <Text style={styles.commentsTitle}>Comentários:</Text>
            {currentComments.length > 0 ? (
              currentComments.map((comment, index) => (
                <View key={index} style={styles.comment}>
                  <Text style={styles.commentAuthor}>{comment.author}:</Text>
                  <Text>{comment.content}</Text>
                </View>
              ))
            ) : (
              <Text style={styles.noComments}>Sem comentários ainda</Text>
            )}
          </View>

          <View style={styles.commentInputContainer}>
            <TextInput
              ref={commentInputRef}
              style={styles.commentInput}
              placeholder="Escreva um comentário..."
              value={newComment}
              onChangeText={setNewComment}
            />
            <TouchableOpacity onPress={handleAddComment} style={styles.sendCommentButton}>
              <Text style={styles.sendCommentButtonText}>Enviar</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContainer: {
    paddingVertical: 10,
    alignItems: 'center',
  },
  card: {
    borderWidth: 1,
    borderRadius: 10,
    padding: 20,
    backgroundColor: '#fff',
    width: width * 0.9,  // Ajuste dinâmico com base na largura da tela
  },
  image: {
    width: '100%',          // Ocupa toda a largura do container
    height: 300,            // Altura fixa
    resizeMode: 'contain',  // Ajusta a imagem para caber sem distorção
    borderRadius: 10,       // Deixa os cantos arredondados
    marginBottom: 10,
    backgroundColor: '#f0f0f0', // Background para preencher caso a imagem não ocupe todo o espaço
  },
  authorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  authorPhoto: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 10,
    borderWidth: 1,
  },
  authorName: {
    fontSize: 16,
    color: '#007BFF',
    textDecorationLine: 'underline', // Para indicar que é um link
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  subscription: {
    fontSize: 16,
    marginVertical: 10,
  },
  likes: {
    fontSize: 16,
    color: 'gray',
    marginBottom: 10,
  },
  buttonContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  likeButton: {
    backgroundColor: '#007BFF',
    paddingVertical: 5,
    paddingHorizontal: 10,
    borderRadius: 5,
    marginRight: 10,
  },
  likeButtonText: {
    color: '#fff',
    fontSize: 16,
  },
  commentButton: {
    backgroundColor: '#007BFF',
    paddingVertical: 5,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
  commentButtonText: {
    color: '#fff',
    fontSize: 16,
  },
  followButton: {
    backgroundColor: '#28a745',
    paddingVertical: 5,
    paddingHorizontal: 15,
    borderRadius: 5,
    position: 'absolute',
    top: 10,
    right: 10,
  },
  followButtonText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
  },
  commentsSection: {
    marginTop: 15,
  },
  commentsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  comment: {
    flexDirection: 'row',
    marginBottom: 5,
  },
  commentAuthor: {
    fontWeight: 'bold',
    marginRight: 5,
  },
  noComments: {
    color: 'gray',
    fontStyle: 'italic',
  },
  commentInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  commentInput: {
    flex: 1,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    padding: 8,
    marginRight: 10,
  },
  sendCommentButton: {
    backgroundColor: '#007BFF',
    paddingVertical: 5,
    paddingHorizontal: 15,
    borderRadius: 5,
  },
  sendCommentButtonText: {
    color: '#fff',
    fontSize: 16,
  },
});

export default PostItem;
