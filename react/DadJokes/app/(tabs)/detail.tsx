import { Image, ScrollView, Text } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

export default function DetailScreen() {
  return (
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <Text style={styles.titleText}>More About My Interest: Software Projects</Text>

      <Text style={styles.bodyText}>
        I like exploring full-stack projects that combine backend APIs, databases, and clean UI design.
      </Text>
      <Image
        source={{
          uri: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Delleboersterheide%2C_natuurgebied_van_het_It_Fryske_Gea._25-12-2019._%28actm.%29_10.jpg/3840px-Delleboersterheide%2C_natuurgebied_van_het_It_Fryske_Gea._25-12-2019._%28actm.%29_10.jpg',
        }}
        style={styles.detailImage}
      />

      <Text style={styles.bodyText}>
        I also enjoy learning mobile frameworks because they let me build apps people can use every day.
      </Text>
      <Image
        source={{
          uri: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Space_Shuttle_Columbia_launching.jpg/1280px-Space_Shuttle_Columbia_launching.jpg?_=20191002004108',
        }}
        style={styles.detailImage}
      />

      <Text style={styles.bodyText}>
        This class has helped me connect concepts from web development to app development.
      </Text>
      <Image
        source={{
          uri: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Messier83_-_Heic1403a.jpg/640px-Messier83_-_Heic1403a.jpg',
        }}
        style={styles.detailImage}
      />
    </ScrollView>
  );
}
