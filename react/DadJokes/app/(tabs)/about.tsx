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
        source={{
          uri: 'https://upload.wikimedia.org/wikipedia/commons/9/99/039_Northern_lights_over_M%C3%BDvatn_%28Iceland%29_Photo_by_Giles_Laurent.jpg',
        }}
        style={styles.mainImage}
      />
    </View>
  );
}
