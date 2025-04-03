
import { createRouter, createWebHistory } from "vue-router";
import Menu from "..components/mainMenu.vue";
import Materias from '..pages/materias.vue';

const routes = [
  {
    path: "/",
    name: "Menu",
  },
  {
    path: "/materias",
    name: "Materias",
    component: Materias,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

export default router;