import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import HomeView from "./views/HomeView.vue";
import SignupView from "./views/SignupView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: HomeView,
  },
  {
    path: "/signup",
    component: SignupView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
