<template>
  <Menubar>
    <template #start>
  <div class="hidden md:block">
    <div class="flex flex-row flex-wrap">
      <div class="w-15rem flex items-center flex-wrap">
        <!-- Logo como imagen -->
        <img 
          src="@\images\logo.jpg" 
          alt="CBTis72 Logo" 
          class="h-1 w-2"
        />
        <span class="font-semibold text-2xl"style="color: #800020;">CBTis72</span>
      </div>

      <div>
        <Button icon="pi pi-bars" severity="secondary" aria-label="Bookmark" text @click="menuMain = !menuMain" />
      </div>
    </div>
  </div>

  <div class="block md:hidden">
    <div class="grid">
      <div class="col-fixed" style="width: 35px">
        <Button icon="pi pi-bars" severity="secondary" aria-label="Bookmark" text @click="menuMainMobile = !menuMainMobile" />
      </div>

      <div class="col flex items-center justify-center">
        <!-- Logo como imagen en móvil -->
        <img 
          src="@\images\logo.jpg" 
          alt="CBTis72 Logo" 
          class="h-1 w-1 rounded-full"
        />
        <span class="font-semibold text-2xl ml-2" style="color: #800020;" >CBTis72</span>
      </div>
    </div>
  </div>
</template>

    <template #end>
      <div class="flex align-items-center gap-2">
        <Avatar image="https://yt3.googleusercontent.com/ytc/AIdro_kirzyGSVrAE6vZryYjtjRWtkR7aosjWPSU_6JbxeS6Kg=s900-c-k-c0x00ffffff-no-rj" shape="circle" @click="toggleMenuProfile" aria-haspopup="true" aria-controls="overlay_menu" />
        <Menu ref="menuProfile" id="overlay_menu" :model="menuProfileItems" :popup="true">
          <template #item="{ item, props }">
            <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
              <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                <span :class="item.icon" />
                <span class="h-1 w-1">{{ item.label }}</span>
              </a>
            </router-link>
          </template>
        </Menu>
      </div>
    </template>
  </Menubar>

  <Sidebar v-model:visible="menuMain" :modal="false" :dismissable="false" :baseZIndex="100">
    <template #container="{ closeCallback }">
      <div class="flex flex-column h-full">
        <mainMenu />
      </div>
    </template>
  </Sidebar>

  <Sidebar v-model:visible="menuMainMobile" :baseZIndex="1001">
    <template>
  <Sidebar v-model:visible="menuMainMobile" :baseZIndex="1001">
    <template #container="{ closeCallback }">
      <div class="flex flex-column h-full">
        <div class="flex align-items-center justify-content-between px-4 pt-3 flex-shrink-0">
          <span class="inline-flex align-items-center gap-2">
            <!-- Nuevo Logo (cambiar la URL de la imagen según sea necesario) -->
            <img 
              src="@\images\logo.jpg" 
              alt="Nuevo Logo" 
              class="h-1 w-1 rounded-full object-cover"
            />
            <!-- Nuevo nombre de la empresa -->
            <span class="font-semibold text-2xl" style="color: #800020;">CBTis72</span>
          </span>
          <span>
            <Button type="button" @click="closeCallback" icon="pi pi-times" rounded outlined class="h-2rem w-2rem mt-1"></Button>
          </span>
        </div>
        <mainMenu />
      </div>
    </template>
  </Sidebar>
</template>

  </Sidebar>

  <div class="py-6 pr-3 md:pr-6" :class="menuMain ? 'container-main' : 'pl-3 md:pl-6'">
    <nuxtPage />
  </div>
</template>

<script setup>
import { ref } from "vue";

const menuProfile = ref();
const menuMain = ref(false);
const menuMainMobile = ref(false);

const menuProfileItems = ref([
  {
    label: "Perfil",
    items: [
      {
        label: "Configuraciones",
        icon: "pi pi-cog",
        route: "/settings",
      },
      {
        label: "Salir",
        icon: "pi pi-sign-out",
        route: "/logout",
      },
    ],
  },
]);

onMounted(() => {
  if (window.innerWidth < 768) {
    menuMain.value = false;
  } else {
    menuMain.value = true;
  }

  window.addEventListener("resize", () => {
    if (window.innerWidth < 768) {
      menuMain.value = false;
    } else {
      menuMain.value = true;
    }
  });
});

const toggleMenuProfile = (event) => {
  menuProfile.value.toggle(event);
};
</script>

<style>
html {
  font-size: 14px;
}

body {
  font-family: var(--font-family);
  font-weight: normal;
  background: var(--surface-ground);
  color: var(--text-color);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: auto;
}

.p-menubar {
  padding: 0.5rem 2rem;
  position: sticky;
  z-index: 1000;
}

.container-main {
  padding-left: 22.5rem;
}

@media screen and (max-width: 768px) {
  .p-menubar {
    padding: 0.5rem 1rem;
  }
  .p-menubar-start {
    width: 90%;
  }
}
</style>
