import { defineStore, acceptHMRUpdate } from "pinia";
import { api } from "@/boot/api";

type Item = {
    id: number;
    name: string | null;
};

interface ItemState {
    items: Item[];
    loading: boolean;
    error: string | null;
}

export const useItemStore = defineStore("item", {
    state: (): ItemState => ({
        items: [],
        loading: false,
        error: null
    }),

    getters: {},

    actions: {
        async fetchItems() {
            this.loading = true;
            this.error = null;

            try {
                const { data } = await api.get<Item[]>("/api/v1/items");
                this.items = data;
            } catch (error) {
                this.error =
                    error instanceof Error
                        ? error.message
                        : "Failed to load items";
            } finally {
                this.loading = false;
            }
        }
    }
});

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useItemStore, import.meta.hot));
}
