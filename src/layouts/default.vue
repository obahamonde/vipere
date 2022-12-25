<template>
  <v-app-bar app color="primary" dark fixed>
    <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

    <v-toolbar-title font-script hover:text-amber cp>Nexus</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn icon>
      <v-icon>mdi-magnify</v-icon>
    </v-btn>

    <v-btn icon>
      <v-icon>mdi-heart</v-icon>
    </v-btn>

    <v-btn icon>
      <v-icon>mdi-dots-vertical</v-icon>
    </v-btn>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" app clipped fixed temporary>
    <v-list dense>
      <v-list-item v-for="item in items" :key="item.title" link>
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
  <v-main>
    <RouterView />
  </v-main>
</template>
<script setup lang="ts">
const drawer = ref(false);
const items = [
  { title: "Dashboard", icon: "mdi-view-dashboard" },
  { title: "Friends", icon: "mdi-account-group" },
  { title: "Messages", icon: "mdi-message" },
];
</script>
