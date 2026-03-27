import { Image, Text, View } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

export default function IndexScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Hi, I am Alvin</Text>
      <Text style={styles.bodyText}>
        I enjoy building web apps and learning mobile development with React Native.
      </Text>
      <Image
        source={{
          uri: 'https://upload.wikimedia.org/wikipedia/commons/9/99/039_Northern_lights_over_M%C3%BDvatn_%28Iceland%29_Photo_by_Giles_Laurent.jpg',
        }}
        style={styles.mainImage}
        resizeMode="cover"
      />
    </View>
  );
}
