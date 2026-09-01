import { defineBoot } from "#q-app";
import axios, { type AxiosInstance } from "axios";

declare module "vue" {
    interface ComponentCustomProperties {
        $axios: AxiosInstance;
        $api: AxiosInstance;
    }
}

const apiUrl = import.meta.env.API_URL;
const api = axios.create(apiUrl ? { baseURL: apiUrl } : {});

export default defineBoot(({ app }) => {
    app.config.globalProperties.$axios = axios;
    app.config.globalProperties.$api = api;
});

export { api };
