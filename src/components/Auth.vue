<template>
  <div v-if="show" dark:invert br fixed  sh p-4 rounded m-4 mr-96>
    <p>{{ user.name }}</p>
    <p>{{ user.email }}</p>
    <button
      row
      icon
      @click="logout()"
      v-if="isAuthenticated"
      text="red"
      hover:text-red-700
    >
      <v-icon>mdi-logout</v-icon>Logout
    </button>
  </div>
  <v-btn
    icon
    @click="loginWithRedirect()"
    v-if="!isAuthenticated"
    x4
    m-4
    fixed
    br
  >
    <v-icon>mdi-account</v-icon>
  </v-btn>
  <div @click="show = !show" cp m-4 mr-72 fixed br z-50>
    <img :src="user.picture" :alt="user.name" v-if="isAuthenticated" rf sh x4 />
  </div>
</template>
<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { user, isAuthenticated, loginWithRedirect, logout } = useAuth0();
const show = ref(false);
</script>
