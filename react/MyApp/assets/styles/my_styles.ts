import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f4f6f8',
    padding: 20,
    alignItems: 'center',
  },
  scrollContainer: {
    backgroundColor: '#f4f6f8',
    padding: 20,
    gap: 12,
  },
  titleText: {
    fontSize: 28,
    fontWeight: '700',
    color: '#102a43',
    textAlign: 'center',
    marginBottom: 12,
  },
  bodyText: {
    fontSize: 16,
    lineHeight: 24,
    color: '#334e68',
    marginBottom: 10,
  },
  mainImage: {
    width: '100%',
    maxWidth: 360,
    height: 220,
    borderRadius: 12,
    marginTop: 10,
  },
  detailImage: {
    width: '100%',
    height: 220,
    borderRadius: 12,
    marginBottom: 12,
  },
});
