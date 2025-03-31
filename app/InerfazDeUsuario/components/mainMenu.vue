<template>
  <div class="overflow-y-auto">
    <ul class="list-none p-3 m-0">
      <li>
        <div
          v-ripple
          v-styleclass="{
            selector: '@next',
            enterClass: 'hidden',
            enterActiveClass: 'slidedown',
            leaveToClass: 'hidden',
            leaveActiveClass: 'slideup'
          }"
          class="p-3 flex align-items-center justify-content-between text-600 cursor-pointer p-ripple"
        >
          <span class="font-medium">MENÚ PRINCIPAL</span>
          <i class="pi pi-chevron-down"></i>
        </div>
        <ul class="list-none p-0 m-0 overflow-hidden">
          <!-- Inicio -->
          <li>
            <a
              v-ripple
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
            >
              <i class="pi pi-home mr-2"></i>
              <span class="font-medium">Inicio</span>
            </a>
          </li>
          <!-- Cursos -->
          <li>
            <a
              v-ripple
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
            >
              <i class="pi pi-bookmark mr-2"></i>
              <span class="font-medium">Cursos</span>
            </a>
          </li>
          <!-- Calificaciones -->
          <li>
            <a
              v-ripple
              v-styleclass="{
                selector: '@next',
                enterClass: 'hidden',
                enterActiveClass: 'slidedown',
                leaveToClass: 'hidden',
                leaveActiveClass: 'slideup'
              }"
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
            >
              <i class="pi pi-chart-line mr-2"></i>
              <span class="font-medium">Calificaciones</span>
              <i class="pi pi-chevron-down ml-auto"></i>
            </a>
            <ul v-show="calificacionesMenuVisible" class="list-none py-0 pl-3 pr-0 m-0 hidden overflow-y-hidden transition-all transition-duration-400 transition-ease-in-out">
              <!-- Ingresar Notas -->
              <li>
                <a
                  v-ripple
                  v-styleclass="{
                    selector: '@next',
                    enterClass: 'hidden',
                    enterActiveClass: 'slidedown',
                    leaveToClass: 'hidden',
                    leaveActiveClass: 'slideup'
                  }"
                  class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                >
                  <i class="pi pi-pencil mr-2"></i>
                  <span class="font-medium">Ingresar Notas</span>
                  <i class="pi pi-chevron-down ml-auto"></i>
                </a>
                <ul class="list-none py-0 pl-3 pr-0 m-0 hidden overflow-y-hidden transition-all transition-duration-400 transition-ease-in-out">
                  <li>
                    <a
                      v-ripple
                      class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                    >
                      <i class="pi pi-table mr-2"></i>
                      <span class="font-medium">Ver Reporte</span>
                    </a>
                  </li>
                  <li>
                    <a
                      v-ripple
                      class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                    >
                      <i class="pi pi-search mr-2"></i>
                      <span class="font-medium">Buscar Alumno</span>
                    </a>
                  </li>
                </ul>
              </li>
              <!-- Estadísticas -->
              <li>
                <a
                  v-ripple
                  class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                >
                  <i class="pi pi-chart-bar mr-2"></i>
                  <span class="font-medium">Estadísticas</span>
                </a>
              </li>
            </ul>
          </li>
          <!-- Estudiantes con submenú -->
          <li>
            <a
              v-ripple
              v-styleclass="{
                selector: '@next',
                enterClass: 'hidden',
                enterActiveClass: 'slidedown',
                leaveToClass: 'hidden',
                leaveActiveClass: 'slideup'
              }"
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
            >
              <i class="pi pi-users mr-2"></i>
              <span class="font-medium">Estudiantes</span>
              <i class="pi pi-chevron-down ml-auto"></i>
            </a>
            <ul class="list-none p-0 m-0 overflow-hidden">
              <li>
                <a
                  v-ripple
                  class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                >
                  <i class="pi pi-check-circle mr-2"></i>
                  <span class="font-medium">Aprobados</span>
                </a>
              </li>
              <li>
                <a
                  v-ripple
                  class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                >
                  <i class="pi pi-times-circle mr-2"></i>
                  <span class="font-medium">Reprobados</span>
                </a>
              </li>
            </ul>
          </li>
          <!-- Notificaciones -->
          <li>
            <a
              v-ripple
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
            >
              <i class="pi pi-bell mr-2"></i>
              <span class="font-medium">Notificaciones</span>
              <span class="inline-flex align-items-center justify-content-center ml-auto bg-primary border-circle" style="min-width: 1.5rem; height: 1.5rem">3</span>
            </a>
          </li>
          <!-- Calendario -->
          <li>
            <a
              v-ripple
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
            >
              <i class="pi pi-calendar mr-2"></i>
              <span class="font-medium">Calendario</span>
            </a>
          </li>
          <!-- Configuración -->
          <li>
            <a
              v-ripple
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
            >
              <i class="pi pi-cog mr-2"></i>
              <span class="font-medium">Configuración</span>
            </a>
          </li>
          <!--Graficas-->
          <li>
            <a
              v-ripple
              v-styleclass="{
                selector: '@next',
                enterClass: 'hidden',
                enterActiveClass: 'slidedown',
                leaveToClass: 'hidden',
                leaveActiveClass: 'slideup'
              }"
              class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
            >
              <i class="pi pi-users mr-2"></i>
              <span class="font-medium">Graficas</span>
              <i class="pi pi-chevron-down ml-auto"></i>
            </a>
            <ul class="list-none p-0 m-0 overflow-hidden">
              <li>
                <a
                  v-ripple
                  class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                >
                  <span class="font-medium">Alumno_Maestro</span>
                </a>
              </li>
              <li>
                <a
                  v-ripple
                  class="flex align-items-center cursor-pointer p-3 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple"
                >
                  <span class="font-medium">NumeroDeAlumnos</span>
                </a>
              </li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </div>

  <div class="mt-auto">
    <hr class="mb-3 mx-3 border-top-1 border-none surface-border" />
    <a v-ripple class="m-3 flex align-items-center cursor-pointer p-3 gap-2 border-round text-700 hover:surface-100 transition-duration-150 transition-colors p-ripple">
      <Avatar image="https://yt3.googleusercontent.com/ytc/AIdro_kirzyGSVrAE6vZryYjtjRWtkR7aosjWPSU_6JbxeS6Kg=s900-c-k-c0x00ffffff-no-rj" shape="circle" />
      <span class="font-bold" style="color: #800020;">CBTis 72</span>
    </a>
  </div>
</template>

<script>
export default {
  data() {
    return {
      graficaMenuVisible: false, // Controla la visibilidad del submenú
      graficaVisible: false, // Controla la visibilidad de las gráficas
      graficaSeleccionada: null, // Guarda la gráfica seleccionada
      calificacionesMenuVisible: false // Controla la visibilidad del submenú de Calificaciones
    };
  },
  methods: {
    // Mostrar/Ocultar el submenú de Gráficas
    toggleGraficaMenu() {
      this.graficaMenuVisible = !this.graficaMenuVisible;
    },
    // Cargar la gráfica seleccionada
    loadGrafica(grafica) {
      this.graficaSeleccionada = grafica;
      this.graficaVisible = true; // Hacer visible el iframe
    },
    // Mostrar/Ocultar el submenú de Calificaciones
    toggleCalificacionesMenu() {
      this.calificacionesMenuVisible = !this.calificacionesMenuVisible;
    }
  }
};
</script>

<style scoped>
.grafica-container {
  margin-top: 20px;
}
</style>
