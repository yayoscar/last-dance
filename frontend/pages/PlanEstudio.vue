<template>
  <div>
    <div class="card">
      <Toolbar class="mb-6">
        <template #start>
          <Button label="Nuevo Plan" icon="pi pi-plus" class="mr-2" @click="clickMostrarDialogoCrearPlan" />
          <Button 
            label="Eliminar" 
            icon="pi pi-trash" 
            severity="danger" 
            outlined 
            @click="confirmDeletePlan()" 
            :disabled="!selectedPlanes || !selectedPlanes.length" 
          />
        </template>
      </Toolbar>

      <DataTable
        ref="dt"
        v-model:selection="selectedPlanes"
        :value="planesEstudio"
        dataKey="id_plan_estudio"
        :paginator="true"
        :rows="10"
        :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
      >
        <template #header>
          <div class="flex justify-between items-center">
            <h3 class="text-xl font-semibold">Planes de Estudio</h3>
            <div class="flex gap-2">
              <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText v-model="filters['global'].value" placeholder="Buscar..." />
              </span>
            </div>
          </div>
        </template>

        <Column selectionMode="multiple" style="width: 3rem" :exportable="false" />
        <Column field="nombre" header="Nombre" sortable style="min-width: 16rem" />
        <Column field="carrera.nombre" header="Carrera" sortable style="min-width: 16rem" />
        <Column header="Acciones" style="min-width: 12rem">
          <template #body="slotProps">
            <div class="flex gap-2">
              <Button 
                icon="pi pi-book" 
                severity="help" 
                rounded 
                @click="clickGestionarSemestres(slotProps.data)"
                v-tooltip="'Gestionar semestres'"
              />
              <Button 
                icon="pi pi-pencil" 
                severity="info" 
                rounded 
                @click="clickEditarPlan(slotProps.data)"
                v-tooltip="'Editar plan'"
              />
              <Button 
                icon="pi pi-trash" 
                severity="danger" 
                rounded 
                @click="confirmDeletePlan(slotProps.data)"
                v-tooltip="'Eliminar plan'"
              />
              <Button 
              icon="pi pi-file-excel" 
              severity="success" 
              rounded 
              @click="exportarCalificaciones(slotProps.data)"
              v-tooltip="'Exportar calificaciones'"
            />
            </div>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Diálogo de nuevo/editar plan -->
    <Dialog 
      v-model:visible="showDialogCrearPlan" 
      :style="{ width: '450px' }" 
      :header="modoEdicion ? 'Editar Plan' : 'Nuevo Plan'" 
      :modal="true" 
      class="p-fluid"
    >
      <div class="p-4 space-y-4">
        <div>
          <label for="nombre" class="block font-semibold mb-1">Nombre*</label>
          <InputText 
            id="nombre" 
            v-model.trim="modelPlan.nombre" 
            required 
            autofocus 
            class="w-full" 
            :class="{ 'p-invalid': submitted && !modelPlan.nombre }"
          />
          <small class="p-error" v-if="submitted && !modelPlan.nombre">
            El nombre es obligatorio
          </small>
        </div>
        
        <div>
          <label for="carrera" class="block font-semibold mb-1">Carrera*</label>
          <Dropdown 
            id="carrera"
            v-model="modelPlan.id_carrera" 
            :options="carreras"
            optionLabel="nombre"
            optionValue="id_carrera"
            placeholder="Selecciona una carrera"
            class="w-full"
            :class="{ 'p-invalid': submitted && !modelPlan.id_carrera }"
          />
          <small class="p-error" v-if="submitted && !modelPlan.id_carrera">
            Debe seleccionar una carrera
          </small>
        </div>
      </div>
      
      <template #footer>
        <Button label="Cancelar" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Guardar" icon="pi pi-check" @click="submitPlan" />
      </template>
    </Dialog>

    <!-- Diálogo de confirmación para eliminar -->
    <Dialog v-model:visible="deletePlanDialog" :style="{ width: '450px' }" header="Confirmar" :modal="true">
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle !text-3xl" />
        <span v-if="planAEliminar">
          ¿Estás seguro de que deseas eliminar el plan <strong>{{ planAEliminar.nombre }}</strong>?
        </span>
        <span v-else>
          ¿Estás seguro de que deseas eliminar los planes seleccionados?
        </span>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" text @click="deletePlanDialog = false" />
        <Button label="Sí" icon="pi pi-check" @click="deletePlan" />
      </template>
    </Dialog>
    
    <!-- Diálogo Gestión de Semestres -->
    <Dialog 
      v-model:visible="showDialogSemestres" 
      modal 
      :header="`Gestión de Semestres - ${planSeleccionado?.nombre || ''}`" 
      :style="{ width: '70rem' }"
    >
      <TabView>
        <TabPanel v-for="semestre in 10" :key="semestre" :header="`Semestre ${semestre}`">
          <div class="flex flex-col gap-4">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-semibold">Materias del Semestre {{ semestre }}</h3>
              <Button 
                label="Agregar Materias" 
                icon="pi pi-plus"
                severity="secondary"
                size="small"
                @click="abrirSelectorMaterias(semestre)"
              />
            </div>
            
            <DataTable :value="materiasPorSemestre[semestre] || []" stripedRows>
              <Column field="nombre" header="Materia"></Column>
              <Column field="creditos" header="Créditos"></Column>
              <Column field="tipo" header="Tipo"></Column>
              <Column header="Acciones">
                <template #body="{ data }">
                  <Button 
                    icon="pi pi-trash" 
                    severity="danger" 
                    size="small" 
                    @click="desasignarMateria(data, semestre)"
                  />
                </template>
              </Column>
            </DataTable>
          </div>
        </TabPanel>
      </TabView>

      <!-- Diálogo para seleccionar materias -->
      <Dialog 
        v-model:visible="showDialogAgregarMaterias" 
        modal 
        header="Agregar Materias" 
        :style="{ width: '50rem' }"
      >
        <div class="mb-4">
          <MultiSelect 
            v-model="materiasSeleccionadas" 
            :options="materiasDisponiblesFiltradas" 
            optionLabel="nombre" 
            placeholder="Selecciona materias"
            class="w-full"
            :filter="true"
            display="chip"
          />
        </div>
        
        <div class="flex justify-end gap-2">
          <Button label="Cancelar" severity="secondary" @click="showDialogAgregarMaterias = false" />
          <Button 
            label="Asignar" 
            severity="primary"
            @click="asignarMaterias"
            :disabled="materiasSeleccionadas.length === 0"
          />
        </div>
      </Dialog>
    </Dialog>

    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import axiosInstance from "~/utils/axiosConfig";
import { useToast } from 'primevue/usetoast';

const toast = useToast();

interface PlanEstudio {
  id_plan_estudio?: number;
  nombre: string;
  id_carrera: number;
  carrera?: {
    id_carrera: number;
    nombre: string;
  };
}

interface Carrera {
  id_carrera: number;
  nombre: string;
}

interface Materia {
  id_materia: number;
  nombre: string;
  creditos: number;
  tipo: string;
  id_modulo?: number | null;
}

// Definir las variables reactivas
const planesEstudio = ref<PlanEstudio[]>([]);
const selectedPlanes = ref<PlanEstudio[]>([]);
const filters = ref({
  global: { value: null, matchMode: 'contains' }
});
const showDialogCrearPlan = ref(false);
const deletePlanDialog = ref(false);
const modoEdicion = ref(false);
const submitted = ref(false);
const carreras = ref<Carrera[]>([]);
const planAEliminar = ref<PlanEstudio | null>(null);

const modelPlan = ref<PlanEstudio>({ 
  nombre: "", 
  id_carrera: null as unknown as number
});

// Variables para gestión de semestres
const showDialogSemestres = ref(false);
const showDialogAgregarMaterias = ref(false);
const planSeleccionado = ref<PlanEstudio | null>(null);
const materiasDisponibles = ref<Materia[]>([]);
const materiasSeleccionadas = ref<Materia[]>([]);
const materiasPorSemestre = ref<Record<number, Materia[]>>({});
const semestreActual = ref(1);

// Computed para filtrar materias disponibles
const materiasDisponiblesFiltradas = computed(() => {
  return materiasDisponibles.value.filter(materia => 
    !materiasPorSemestre.value[semestreActual.value]?.some(m => m.id_materia === materia.id_materia)
)});

// Cargar datos iniciales
onMounted(async () => {
  await Promise.all([cargarPlanesEstudio(), cargarCarreras()]);
});

const cargarPlanesEstudio = async () => {
  try {
    const response = await axiosInstance.get("planes_estudio/");
    planesEstudio.value = response.data;
  } catch (error) {
    mostrarError('Error al cargar los planes de estudio');
  }
};

const cargarCarreras = async () => {
  try {
    const response = await axiosInstance.get("carreras/");
    carreras.value = response.data;
  } catch (error) {
    mostrarError('Error al cargar las carreras');
  }
};

const cargarMateriasDisponibles = async () => {
  try {
    const response = await axiosInstance.get("materias/");
    materiasDisponibles.value = response.data;
  } catch (error) {
    mostrarError('Error al cargar materias disponibles');
  }
};

const cargarMateriasPorSemestre = async () => {
  if (!planSeleccionado.value) return;

  try {
    const response = await axiosInstance.get(
      `planes_estudio/${planSeleccionado.value.id_plan_estudio}/semestres/materias`
    );
    materiasPorSemestre.value = response.data;
  } catch (error) {
    mostrarError('Error al cargar materias por semestre');
  }
};

// Métodos para CRUD de planes
const clickMostrarDialogoCrearPlan = () => {
  modoEdicion.value = false;
  modelPlan.value = { nombre: "", id_carrera: null as unknown as number };
  submitted.value = false;
  showDialogCrearPlan.value = true;
};

const clickEditarPlan = (plan: PlanEstudio) => {
  modoEdicion.value = true;
  modelPlan.value = { ...plan };
  submitted.value = false;
  showDialogCrearPlan.value = true;
};

const confirmDeletePlan = (plan?: PlanEstudio) => {
  if (plan) {
    planAEliminar.value = plan;
  } else {
    planAEliminar.value = null;
  }
  deletePlanDialog.value = true;
};

const hideDialog = () => {
  showDialogCrearPlan.value = false;
  submitted.value = false;
};

const validarFormulario = (): boolean => {
  submitted.value = true;
  
  if (!modelPlan.value.nombre.trim()) {
    return false;
  }
  
  if (!modelPlan.value.id_carrera) {
    return false;
  }
  
  return true;
};

const submitPlan = async () => {
  if (!validarFormulario()) return;

  try {
    if (modoEdicion.value && modelPlan.value.id_plan_estudio) {
      // Cambiado a PUT y URL corregida
      const response = await axiosInstance.put(
        `planes_estudio/${modelPlan.value.id_plan_estudio}`,
        {
          nombre: modelPlan.value.nombre,
          id_carrera: modelPlan.value.id_carrera
        }
      );
      const index = planesEstudio.value.findIndex(p => p.id_plan_estudio === modelPlan.value.id_plan_estudio);
      if (index !== -1) {
        planesEstudio.value[index] = response.data;
      }
      mostrarExito('Plan actualizado correctamente');
    } else {
      // POST con URL corregida
      const response = await axiosInstance.post(
        "planes_estudio",
        {
          nombre: modelPlan.value.nombre,
          id_carrera: modelPlan.value.id_carrera
        }
      );
      planesEstudio.value.push(response.data);
      mostrarExito('Plan creado correctamente');
    }
    showDialogCrearPlan.value = false;
  } catch (error: any) {
    mostrarError(error.response?.data?.detail || 'Error al guardar el plan');
  }
};

const deletePlan = async () => {
  try {
    if (planAEliminar.value) {
      // DELETE con URL corregida
      await axiosInstance.delete(
        `planes_estudio/${planAEliminar.value.id_plan_estudio}`
      );
      planesEstudio.value = planesEstudio.value.filter(
        p => p.id_plan_estudio !== planAEliminar.value?.id_plan_estudio
      );
      mostrarExito('Plan eliminado correctamente');
    } else if (selectedPlanes.value.length > 0) {
      // DELETE múltiple con estructura de datos corregida
      const ids = selectedPlanes.value.map(plan => plan.id_plan_estudio);
      await axiosInstance.delete(
        "planes_estudio/delete-multiple",
        { data: { ids } }
      );
      planesEstudio.value = planesEstudio.value.filter(
        plan => !ids.includes(plan.id_plan_estudio)
      );
      selectedPlanes.value = [];
      mostrarExito('Planes eliminados correctamente');
    }
    deletePlanDialog.value = false;
  } catch (error) {
    mostrarError('Error al eliminar el plan');
  }
};

// Métodos para gestión de semestres
const clickGestionarSemestres = async (plan: PlanEstudio) => {
  planSeleccionado.value = plan;
  showDialogSemestres.value = true;
  
  try {
    await Promise.all([cargarMateriasDisponibles(), cargarMateriasPorSemestre()]);
  } catch (error) {
    mostrarError('Error al cargar información de semestres');
  }
};

const abrirSelectorMaterias = (semestre: number) => {
  semestreActual.value = semestre;
  materiasSeleccionadas.value = [];
  showDialogAgregarMaterias.value = true;
};
const exportarCalificaciones = async (plan?: PlanEstudio) => {
  const planId = plan?.id_plan_estudio || selectedPlanes.value?.[0]?.id_plan_estudio;
  
  if (!planId) {
    mostrarError('Debe seleccionar un plan');
    return;
  }
  
  try {
    toast.add({
      severity: 'info',
      summary: 'Generando reporte',
      detail: 'Por favor espere...',
      life: 3000
    });

    const response = await axiosInstance.get(
      `planes_estudio/${planId}/reporte-calificaciones`,
      { 
        responseType: 'blob',
        headers: {
          'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
      }
    );
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `calificaciones_plan_${planId}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.parentNode?.removeChild(link);

    mostrarExito('Reporte descargado correctamente');
  } catch (error) {
    console.error('Error al exportar:', error);
    mostrarError('Error al generar el reporte. Verifique la consola para más detalles.');
  }
};

const asignarMaterias = async () => {
  if (!planSeleccionado.value || materiasSeleccionadas.value.length === 0) return;

  try {
    const promises = materiasSeleccionadas.value.map(materia =>
      axiosInstance.post(
        `planes_estudio/${planSeleccionado.value?.id_plan_estudio}/materias`,
        {
          id_materia: materia.id_materia,
          semestre: semestreActual.value
        }
      )
    );

    await Promise.all(promises);
    mostrarExito('Materias asignadas correctamente');
    showDialogAgregarMaterias.value = false;
    await cargarMateriasPorSemestre();
  } catch (error: any) {
    mostrarError(error.response?.data?.detail || 'Error al asignar materias');
  }
};

const desasignarMateria = async (materia: Materia, semestre: number) => {
  if (!planSeleccionado.value) return;

  try {
    await axiosInstance.delete(
      `planes_estudio/${planSeleccionado.value.id_plan_estudio}/materias/${materia.id_materia}`,
      { params: { semestre } }
    );
    mostrarExito('Materia desasignada correctamente');
    await cargarMateriasPorSemestre();
  } catch (error) {
    mostrarError('Error al desasignar materia');
  }
};

// Helpers
const mostrarExito = (mensaje: string) => {
  toast.add({ severity: 'success', summary: 'Éxito', detail: mensaje, life: 3000 });
};

const mostrarError = (mensaje: string) => {
  toast.add({ severity: 'error', summary: 'Error', detail: mensaje, life: 3000 });
};
</script>

<style scoped lang="css">
.card {
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  background-color: white;
}

.p-toolbar {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}

.p-invalid {
  border-color: #e24c4c;
}

.p-error {
  color: #e24c4c;
  font-size: 0.875rem;
}
</style>