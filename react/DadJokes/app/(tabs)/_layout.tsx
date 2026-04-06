import { Tabs } from 'expo-router';
import React from 'react';

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
        }}
      />
      <Tabs.Screen
        name="joke_list"
        options={{
          title: 'Jokes',
        }}
      />
      <Tabs.Screen
        name="add_joke"
        options={{
          title: 'Add Joke',
        }}
      />
    </Tabs>
  );
}
