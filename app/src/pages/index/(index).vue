<template>
    <q-page class="flex flex-center">
        <div class="column items-center">
            <h1>Hello World</h1>
            <q-btn
                class="q-mt-md"
                color="primary"
                to="/second"
                label="Go to Second Page"
                no-caps
            />
        </div>

        <q-inner-loading :showing="store.loading" />

        <q-banner v-if="store.error" class="bg-negative text-white q-ma-md">
            {{ store.error }}
        </q-banner>

        <pre v-else>{{ store.items }}</pre>
    </q-page>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useItemStore } from "@/stores/item";

const store = useItemStore();

onMounted(() => {
    void store.fetchItems();
});
</script>
