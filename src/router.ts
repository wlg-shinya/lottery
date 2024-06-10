import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import HomeView from "./views/HomeView.vue";
import SignupView from "./views/SignupView.vue";
import PublicView from "./views/PublicView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: HomeView,
  },
  {
    path: "/signup",
    component: SignupView,
  },
  {
    path: "/public",
    component: PublicView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
