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
        source={{ uri: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80' }}
        style={styles.detailImage}
      />

      <Text style={styles.bodyText}>
        I also enjoy learning mobile frameworks because they let me build apps people can use every day.
      </Text>
      <Image
        source={{ uri: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80' }}
        style={styles.detailImage}
      />

      <Text style={styles.bodyText}>
        This class has helped me connect concepts from web development to app development.
      </Text>
      <Image
        source={{ uri: 'https://images.unsplash.com/photo-1517430816045-df4b7de11d1d?auto=format&fit=crop&w=1200&q=80' }}
        style={styles.detailImage}
      />
    </ScrollView>
  );
}
