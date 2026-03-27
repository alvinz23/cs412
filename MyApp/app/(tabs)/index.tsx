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
        source={require('../../assets/images/index_photo.png')}
        style={styles.mainImage}
        resizeMode="cover"
      />
    </View>
  );
}
