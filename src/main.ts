import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";

// router
import router from "./router";

// axios
import axios from "axios";
axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

createApp(App).use(router).mount("#app");
