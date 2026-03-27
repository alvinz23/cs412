import { Image, Text, View } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

export default function AboutScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>About This App</Text>
      <Text style={styles.bodyText}>
        This is a simple React Native app created with Expo tabs. It demonstrates navigation and reusable styles across multiple screens.
      </Text>
      <Image
        source={{ uri: 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=1200&q=80' }}
        style={styles.mainImage}
      />
    </View>
  );
}
