import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import HomeView from "./views/HomeView.vue";
import SignupView from "./views/SignupView.vue";
import SignupStep2View from "./views/SignupStep2View.vue";
import PublicView from "./views/PublicView.vue";
import ProfileView from "./views/ProfileView.vue";

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
    path: "/signup_step2",
    component: SignupStep2View,
  },
  {
    path: "/public",
    component: PublicView,
  },
  {
    path: "/profile",
    component: ProfileView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
