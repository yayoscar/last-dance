<template>
  <div class="overflow-y-auto">
    <ul class="list-none p-3 m-0">
      <li>
        <div v-ripple v-styleclass="{
            selector: '@next',
            enterClass: 'hidden',
            enterActiveClass: 'slidedown',
            leaveToClass: 'hidden',
            leaveActiveClass: 'slideup'
          }" class="p-3 flex align-items-center justify-content-between text-600 cursor-pointer p-ripple">
          <span class="font-medium">MENÚ PRINCIPAL</span>
          <i class="pi pi-chevron-down"></i>
        </div>
        <ul class="list-none p-0 m-0 overflow-hidden">
          <!-- Inicio -->
          <li>
            <a @click="Inicio" v-ripple
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
              <i class="pi pi-home mr-2"></i>
              <span class="font-medium">Inicio</span>
            </a>
          </li>
          <!-- Cursos -->
          <li>
            <NuxtLink to="/carreras"
              v-ripple 
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
              <i class="pi pi-tag mr-2"></i>
              <span class="font-medium">Carreras</span>
            </NuxtLink>
          </li>
          <!-- Cursos -->
          <li>
            <a v-ripple
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
              <i class="pi pi-bookmark mr-2"></i>
              <span class="font-medium">Cursos</span>
            </a>
          </li>
          <!-- Calificaciones -->
          <li>
            <a v-ripple @click="toggleCalificacionesMenu"
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
              <i class="pi pi-chart-line mr-2"></i>
              <span class="font-medium">Calificaciones</span>
              <i class="pi pi-chevron-down ml-auto"></i>
            </a>
            <ul v-show="calificacionesMenuVisible" class="list-none py-0 pl-3 pr-0 m-0 overflow-hidden">
              <!-- Ingresar Notas -->
              <li>
                <a v-ripple
                  class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
                  <i class="pi pi-pencil mr-2"></i>
                  <span class="font-medium">Ingresar Notas</span>
                </a>
              </li>
              <!-- Estadísticas -->
              <li>
                <a v-ripple
                  class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
                  <i class="pi pi-chart-bar mr-2"></i>
                  <span class="font-medium">Estadísticas</span>
                </a>
              </li>
            </ul>
          </li>
          <!-- Materias -->
          <li>
            <a v-ripple @click="Materia"
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
              <i class="pi pi-book mr-2"></i>
              <span class="font-medium">Materias</span>
            </a>
          </li>
          <li>
            <a v-ripple @click="leccion()"
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
              <i class="pi pi-book mr-2"></i>
              <span class="font-medium">Lecciones</span>
            </a>
          </li>
          <!-- Planes de Estudio -->
          <li>
            <a v-ripple
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
              <i class="pi pi-file mr-2"></i>
              <span class="font-medium">Planes de Estudio</span>
            </a>
          </li>
        </ul>
      </li>
    </ul>
  </div>

  <div class="mt-auto">
    <hr class="mb-3 mx-3 border-top-1 border-none surface-border" />
    <a v-ripple
      class="m-3 flex align-items-center cursor-pointer p-3 gap-2 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
      <Avatar
        image="https://yt3.googleusercontent.com/ytc/AIdro_kirzyGSVrAE6vZryYjtjRWtkR7aosjWPSU_6JbxeS6Kg=s900-c-k-c0x00ffffff-no-rj"
        shape="circle" />
      <span class="font-bold" style="color: #800020;">CBTis 72</span>
    </a>
  </div>
</template>

<script>
import Leccion from '~/pages/leccion.vue';


export default {
  data() {
    return {
      calificacionesMenuVisible: false,
    };
  },
  methods: {
      toggleCalificacionesMenu() {
        this.calificacionesMenuVisible = !this.calificacionesMenuVisible;
      },
      Materia() {
        this.$router.push('/Materias');
      },
      Inicio() {
        this.$router.push('/');
      },
      leccion() {
        this.$router.push('/leccion');
      }
  },
  components: {
    Leccion
    }
  }

</script>

<style scoped>
.grafica-container {
  margin-top: 20px;
}
</style>