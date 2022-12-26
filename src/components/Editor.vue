<script setup lang="ts">
import MonacoEditor from "monaco-editor-vue3";
import { isDark } from "../../hooks/dark";
import { options } from "../../hooks/monaco";
const { state, dispatch } = useStore();
const test = ref("");
const title = ref("");
const funcs = ref([]);
const building = ref(false);
const language = computed(() => {
  switch (title.value.split(".")[1]) {
    case "py":
      return "python";
    case "html":
      return "html";
    case "js":
      return "javascript";
    case "ts":
      return "typescript";
    case "css":
      return "css";
    case "json":
      return "json";
    case "md":
      return "markdown";
    default:
      return "plaintext";
  }
});

const fetchWorkspace = async () => {
  const { data } = await useFetch(`/api/upload/${state.user.sub}`).json();
  dispatch({ workspace: unref(data as any) });
};

const postLambda = async () => {
  await fetch(
    `/api/upload/${state.user.sub}/?name=${encodeURIComponent(title.value)}`,
    {
      method: "POST",
      body: JSON.stringify({
        code: test.value,
      }),
    }
  );
  await fetchWorkspace();
};

const fetchZip = async () => {
  building.value = true;
  const { data } = await useFetch(
    `/api/download/${state.user.sub}`
  ).blob();
  building.value = false;
  dispatch({
    zip: unref(data as any),
    zip_url: URL.createObjectURL(unref(data as any)),
  });
  
};

const deployLambda = async () => {
  const formdata = new FormData();
  formdata.append("file", state.zip);
  const { data } = await useFetch(`/api/deploy/${state.user.sub}`, {
    method: "POST",
    body: formdata,
  }).text();
  dispatch({ deploy: unref(data as any) });
};

const fetchLambdas = async () => {
  const { data } = await useFetch(`/api/deploy/${state.user.sub}`).json();
  console.log(data);
  const res = unref(data as any);
  funcs.value = res;
};

const deleteLambda = async (name: string) => {
  await fetch(`/api/deploy/${state.user.sub}/?name=${name}`, {
    method: "DELETE",
  });
  await fetchLambdas();
};


watchEffect(() => {
  state.code
    ? (test.value = state.code)
    : (test.value =
      "");
});

watchEffect(() => {
  state.currentname
    ? (title.value = state.currentname)
    : (title.value = "app.py");
});

onMounted(async () => {
  await fetchLambdas();

  await fetchWorkspace();
});

const len = computed(() => funcs.value.length);

watchEffect(() => {
  if (len.value > 0) {
    funcs.value = funcs.value.sort((a, b) => {
      return a.name > b.name ? 1 : -1;
    });
  }
});

</script>

<template>
  <div pa-4 app row center gap-4>
    <input v-model="title" bg-gray-500 p-1 px-4 w-full rounded text-white sh />
    <div col center>
      <v-btn :color="isDark ? 'secondary' : 'primary'" icon @click="postLambda()" z-50>
        <v-icon>mdi-content-save</v-icon>
      </v-btn>
      <small text-xs scale-75>Save</small>
    </div>
    <div col center v-if="!state.zip_url">
      <v-btn :color="isDark ? 'secondary' : 'primary'" icon @click="fetchZip()" z-50 v-if="!state.zip_url" :class="building? 'animate-spin' : ''">
        <v-icon>mdi-cog</v-icon>
      </v-btn>
      <small text-xs scale-75>Build</small>
    </div>
    <div col center v-else>
      <a :href="state.zip_url" underlined text-orange-600 download="app.zip" col center>
        <Icon icon="mdi-zip-box" color="primary" x3 />
        <small text-xs scale-75>Package</small>
      </a>
    </div>
    <div col center v-if="!state.deploy">
      <v-btn :color="isDark ? 'secondary' : 'primary'" icon @click="deployLambda()" z-50>
        <v-icon>mdi-cloud-upload</v-icon>
      </v-btn>
      <small text-xs scale-75>Deploy</small>
    </div>
    <div col center v-else cp>
      <a :href="JSON.parse(state.deploy).url" underlined text-orange-600 col center>
        <Icon icon="logos:aws-lambda" rf p-1 :color="isDark ? 'secondary' : 'primary'" x3 />
        <small text-xs scale-75>Deployed</small>
      </a>
    </div>
    <v-navigation-drawer v-if="len > 0"
      location="right"
  z-20    >
      <h1 text-lg text-teal drop-shadow-lg drop-shadow-black p-4>Deployed</h1>
      <div v-for="func in funcs" color="warning" col start gap-1 text-xs scale-80 p-1>

        <p col><strong>ID</strong>
        <p>{{ func.name }}
          <Icon icon="mdi-delete" text-red hover:text-red-700 cp scale @click="deleteLambda(func.name)" />
        </p>
        </p>
        <p col><strong>URL</strong> <a :href="func.url">{{ func.url }}</a></p>
        <p col><strong>ARN</strong> {{ func.arn }}</p>
      </div>
    </v-navigation-drawer>
  </div>
  <div h-screen w-auto py-4 rounded-lg sh :bg="isDark ? '#1E1E1E' : '#FFFFFE'">
    <MonacoEditor :theme="isDark ? 'vs-dark' : 'vs'" :options="options" :language="language" v-model:value="test">
    </MonacoEditor>
  </div>
</template>
