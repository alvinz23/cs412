import { Tabs } from 'expo-router';
import React from 'react';

export default function TabLayout() {
  // Main tabs for this assignment flow.
  return (
    <Tabs>
      <Tabs.Screen name="login" options={{ title: 'Login' }} />
      <Tabs.Screen name="profile_posts" options={{ title: 'My Profile' }} />
      <Tabs.Screen name="feed" options={{ title: 'Feed' }} />
      <Tabs.Screen name="create_post" options={{ title: 'Create Post' }} />
    </Tabs>
  );
}
