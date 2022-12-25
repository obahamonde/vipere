import { acceptHMRUpdate, defineStore } from "pinia";

export const useStore = defineStore("store", () => {
  const state = reactive({}) as any;
  const dispatch = (newState: any) => {
    Object.assign(state, { ...state, ...newState });
  };
  return {
    state,
    dispatch,
  };
});

if (import.meta.hot) {
  acceptHMRUpdate(useStore, import.meta.hot);
}
