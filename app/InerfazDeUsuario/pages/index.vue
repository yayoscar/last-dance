<template>
  <div class="grid">
    <!-- Tarjeta 1: Evaluaciones -->
    <div class="lg:col-3">
      <div class="surface-card shadow-2 p-3 border-round">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-500 font-medium mb-3">Evaluaciones</span>
            <div class="text-900 font-medium text-xl">152</div>
          </div>
          <div class="flex align-items-center justify-content-center bg-blue-100 border-round" style="width: 2.5rem; height: 2.5rem">
            <i class="pi pi-pencil text-blue-500 text-xl"></i>
          </div>
        </div>
        <span class="text-green-500 font-medium">24 nuevas</span>
        <span class="text-500">desde la última revisión</span>
      </div>
    </div>
    <!-- Tarjeta 2: Promedio -->
    <div class="lg:col-3">
      <div class="surface-card shadow-2 p-3 border-round">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-500 font-medium mb-3">Promedio</span>
            <div class="text-900 font-medium text-xl">8.5</div>
          </div>
          <div class="flex align-items-center justify-content-center bg-orange-100 border-round" style="width: 2.5rem; height: 2.5rem">
            <i class="pi pi-star text-orange-500 text-xl"></i>
          </div>
        </div>
        <span class="text-green-500 font-medium">+5%</span>
        <span class="text-500">desde la última evaluación</span>
      </div>
    </div>
    <!-- Tarjeta 3: Estudiantes Inscritos -->
    <div class="lg:col-3">
      <div class="surface-card shadow-2 p-3 border-round">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-500 font-medium mb-3">Estudiantes Inscritos</span>
            <div class="text-900 font-medium text-xl">300</div>
          </div>
          <div class="flex align-items-center justify-content-center bg-cyan-100 border-round" style="width: 2.5rem; height: 2.5rem">
            <i class="pi pi-users text-cyan-500 text-xl"></i>
          </div>
        </div>
        <span class="text-green-500 font-medium">+20</span>
        <span class="text-500">nuevos registrados</span>
      </div>
    </div>
    <!-- Tarjeta 4: Comentarios -->
    <div class="lg:col-3">
      <div class="surface-card shadow-2 p-3 border-round">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-500 font-medium mb-3">Comentarios</span>
            <div class="text-900 font-medium text-xl">152 sin leer</div>
          </div>
          <div class="flex align-items-center justify-content-center bg-purple-100 border-round" style="width: 2.5rem; height: 2.5rem">
            <i class="pi pi-comment text-purple-500 text-xl"></i>
          </div>
        </div>
        <span class="text-green-500 font-medium">85</span>
        <span class="text-500">respondidos</span>
      </div>
    </div>
  </div>
</template>
