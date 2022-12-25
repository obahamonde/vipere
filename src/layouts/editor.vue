<template>
  <v-app-bar app :color="isDark ? 'secondary' : 'primary'" dark fixed>
    <v-btn icon @click.stop="refresh()"><img src="/favicon.gif" rf x3 /></v-btn>
    <v-toolbar-title font-script hover:text-amber cp>Vipére</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon @click="toggleDark()">
      <v-icon>{{ isDark ? "mdi-lightbulb-on" : "mdi-lightbulb" }}</v-icon>
    </v-btn>
  </v-app-bar>

  <v-navigation-drawer app clipped fixed width="150" permanent col center>
    <v-list dense>
      <v-list-item v-for="item in state.workspace" :key="item.title" link>
        <div v-if="item.name.includes('.py')" cp scale row center>
          <Icon icon="logos:python" m-1 @click="getCode(item.url)" />
          <v-title text-xs @click="getCode(item.url)">{{ item.name }}</v-title>
          <Icon
            icon="mdi-delete"
            @click="deleteFile(item.url)"
            text-red
            hover:text-red-700
          />
        </div>
        <div v-else-if="item.name.includes('.html')" cp scale row center>
          <Icon icon="logos:html-5" m-1 @click="getCode(item.url)" />
          <v-title text-xs
            ><a :href="item.url" decoration-none>{{ item.name }}</a></v-title
          >
          <Icon
            icon="mdi-delete"
            @click="deleteFile(item.url)"
            text-red
            hover:text-red-700
          />
        </div>
        <div
          v-else-if="item.name.includes('requirements.txt')"
          cp
          scale
          row
          center
        >
          <Icon icon="mdi-cog" @click="getCode(item.url)" />
          <v-title text-xs @click="getCode(item.url)">{{ item.name }}</v-title>
          <Icon
            icon="mdi-delete"
            @click="deleteFile(item.url)"
            text-red
            hover:text-red-700
          />
        </div>
        <div v-else-if="item.type === 'directory'" cp scale row>
          <Icon icon="mdi-folder" @click="fetchFolder(item.url, item.name)" />
          <v-title @click="fetchFolder(item.url, item.name)">{{
            item.name
          }}</v-title>
          <Icon
            icon="mdi-delete"
            @click="deleteFile(item.url)"
            text-red
            hover:text-red-700
          />
        </div>
        <div v-else cp scale row>
          <Icon icon="mdi-file" @click="fetchFolder(item.url, item.name)" />
          <v-title @click="fetchFolder(item.url, item.name)">{{
            item.name
          }}</v-title>
          <Icon
            icon="mdi-delete"
            @click="deleteFile(item.url)"
            text-red
            hover:text-red-700
          />
        </div>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
  <v-main>
    <RouterView />
    <Auth z-50 />
  </v-main>
</template>
<script setup lang="ts">
import { isDark, toggleDark } from "../../hooks/dark";
import { useAuth0 } from "@auth0/auth0-vue";
const { getAccessTokenSilently } = useAuth0();
const { state, dispatch } = useStore();

const refresh = () => {
  window.location.reload();
};

const fetchWorkspace = async () => {
  const token = await getAccessTokenSilently();
  const { data } = await useFetch(
    "https://dev-tvhqmk7a.us.auth0.com/userinfo",
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  ).json();
  state.user = unref(data);
  const { data: workspace } = await useFetch(
    "/api/upload/" + state.user.sub
  ).json();
  state.workspace = unref(workspace);
};

const fetchFolder = async (url: string, name: string) => {
  const { data } = await useFetch(
    "/api/upload/?key=" + url.split("cdn.hatarini.com/")[1]
  ).json();
  state.currentFolder = {
    [name]: JSON.stringify(unref(data)),
  };
};

const getCode = async (url: string) => {
  state.codeUrl = url;
  const { data } = await useFetch(state.codeUrl).text();
  state.code = unref(data);
  state.currentname = state.codeUrl.split("lambda/")[1];
  await downloadCode();
};

const downloadCode = async () => {
  const { data } = await useFetch(
    "/api/download/?key=" + state.codeUrl.split("cdn.hatarini.com/")[1]
  ).json();
  state.code = unref(data);
};

const deleteFile = async (url: string) => {
  await useFetch("/api/upload/?key=" + url.split("cdn.hatarini.com/")[1], {
    method: "DELETE",
  });
  await fetchWorkspace();
  state.code = "";
};
const items = ref([]);

onMounted(async () => {
  await fetchWorkspace();
  items.value = state.workspace;
});

watchEffect(async () => {
  state.workspace ? (items.value = state.workspace) : await fetchWorkspace();
});
</script>
