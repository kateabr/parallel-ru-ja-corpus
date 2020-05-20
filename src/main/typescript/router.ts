import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

Vue.use(VueRouter);

const routes: RouteConfig[] = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/Home.vue")
  },
  {
    path: "/search",
    name: "search",
    component: () => import("@/views/Search.vue")
  },
  {
    path: "/about",
    name: "about",
    component: () => import("@/views/About.vue")
  },
  {
    path: "/entry/:id",
    name: "entry",
    component: () => import("@/views/Entry.vue")
  },
  {
    path: "*",
    name: "404",
    component: () => import("@/views/404.vue")
  }
];

export const router = new VueRouter({
  base: "/",
  mode: "history",
  routes: routes
});
