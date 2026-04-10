import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#f6f7fb',
  },
  contentWrap: {
    padding: 16,
    gap: 12,
  },
  titleText: {
    fontSize: 24,
    fontWeight: '700',
    color: '#1f2a44',
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#243b6b',
    marginBottom: 6,
  },
  bodyText: {
    fontSize: 15,
    lineHeight: 22,
    color: '#263247',
  },
  metaText: {
    fontSize: 13,
    color: '#5d6b85',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#dde3ef',
    padding: 12,
    gap: 6,
  },
  mainImage: {
    width: '100%',
    height: 220,
    borderRadius: 8,
    marginTop: 6,
  },
  input: {
    backgroundColor: '#ffffff',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#d5ddec',
    padding: 12,
    color: '#1f2a44',
    fontSize: 15,
    minHeight: 48,
  },
  button: {
    backgroundColor: '#3158c9',
    borderRadius: 8,
    alignItems: 'center',
    paddingVertical: 12,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 15,
    fontWeight: '700',
  },
});
