<template>
    <div>
        <Card>
            <template #title>Planes de Estudio</template>
            
            <template #content>
                <DataTable :value="planesEstudio" stripedRows>
                    <template #header>
                        <div class="flex justify-end">
                            <Button 
                                @click="clickMostrarDialogoCrearPlan"
                                label="Agregar Plan de Estudio" 
                                icon="pi pi-plus"
                            />
                        </div>
                    </template>
                    <Column field="nombre" header="Nombre del Plan"></Column>
                    <Column field="carrera.nombre" header="Carrera"></Column>
                    <Column field="acciones" header="Acciones">
                        <template #body="slotProps">
                            <div class="flex gap-2">
                                <Button 
                                    icon="pi pi-book" 
                                    severity="help" 
                                    size="small"
                                    @click="clickGestionarSemestres(slotProps.data)"
                                    v-tooltip="'Gestionar semestres'"
                                />
                                <Button 
                                    icon="pi pi-pencil" 
                                    severity="info" 
                                    size="small" 
                                    @click="clickEditarPlan(slotProps.data)"
                                    v-tooltip="'Editar plan'"
                                />
                                <Button 
                                    icon="pi pi-trash" 
                                    severity="danger" 
                                    size="small" 
                                    @click="clickEliminarPlan(slotProps.data)"
                                    v-tooltip="'Eliminar plan'"
                                />
                            </div>
                        </template>
                    </Column>                
                </DataTable>
            </template>
        </Card>

        <!-- Dialog Crear/Editar Plan de Estudio -->
        <Dialog 
            v-model:visible="showDialogCrearPlan" 
            modal 
            :header="modoEdicion ? 'Editar Plan de Estudio' : 'Agregar Plan de Estudio'" 
            :style="{ width: '60rem' }"
        >
            <span class="text-surface-500 dark:text-surface-400 block mb-4">
                {{ modoEdicion ? 'Edita la información del plan de estudio.' : 'Agrega información del plan de estudio.' }}
            </span>
            
            <form @submit.prevent="submitPlan">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Nombre del Plan -->
                    <div class="field">
                        <label class="font-semibold" for="nombre">Nombre del Plan *</label>
                        <div class="flex flex-col gap-2 mt-1">
                            <InputText 
                                id="nombre"
                                v-model="modelPlan.nombre"
                                class="w-full" 
                                autocomplete="off"
                                :class="{ 'p-invalid': $v.nombre.$error }"
                                @blur="$v.nombre.$touch"
                            />
                            <small 
                                v-if="$v.nombre.$error" 
                                class="p-error"
                            >
                                {{ $v.nombre.$errors[0].$message }}
                            </small>
                        </div>
                    </div>

                    <!-- Carrera -->
                    <div class="field">
                        <label class="font-semibold" for="carrera">Carrera *</label>
                        <div class="flex flex-col gap-2 mt-1">
                            <Dropdown
                                id="carrera"
                                v-model="modelPlan.id_carrera"
                                :options="carreras"
                                optionLabel="nombre"
                                optionValue="id_carrera"
                                placeholder="Selecciona una carrera"
                                class="w-full"
                                :class="{ 'p-invalid': $v.id_carrera.$error }"
                                @blur="$v.id_carrera.$touch"
                            />
                            <small 
                                v-if="$v.id_carrera.$error" 
                                class="p-error"
                            >
                                {{ $v.id_carrera.$errors[0].$message }}
                            </small>
                        </div>
                    </div>
                </div>
                
                <div class="flex justify-end gap-2 mt-6">
                    <Button 
                        type="button" 
                        label="Cancelar" 
                        severity="secondary" 
                        @click="cancelarDialog"
                    />
                    <Button 
                        type="submit" 
                        :label="modoEdicion ? 'Actualizar' : 'Agregar'" 
                        severity="primary"
                        :loading="loading"
                    />
                </div>
            </form>
        </Dialog>

        <!-- Dialog Confirmar Eliminación -->
        <Dialog 
            v-model:visible="showDialogEliminar" 
            modal 
            header="Confirmar Eliminación" 
            :style="{ width: '30rem' }"
        >
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle text-orange-500" style="font-size: 2rem"></i>
                <span>
                    ¿Estás seguro de que quieres eliminar el plan de estudio 
                    <strong>{{ planAEliminar?.nombre }}</strong> 
                    de la carrera <strong>{{ planAEliminar?.carrera?.nombre }}</strong>?
                </span>
            </div>
            
            <div class="flex justify-end gap-2 mt-4">
                <Button 
                    type="button" 
                    label="Cancelar" 
                    severity="secondary" 
                    @click="showDialogEliminar = false"
                />
                <Button 
                    type="button" 
                    label="Eliminar" 
                    severity="danger"
                    :loading="loading"
                    @click="confirmarEliminarPlan"
                />
            </div>
        </Dialog>

        <!-- Dialog Gestión de Semestres -->
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

            <!-- Dialog para seleccionar materias -->
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
                    <Button 
                        label="Cancelar" 
                        severity="secondary" 
                        @click="showDialogAgregarMaterias = false"
                    />
                    <Button 
                        label="Asignar" 
                        severity="primary"
                        @click="asignarMaterias"
                        :disabled="materiasSeleccionadas.length === 0"
                    />
                </div>
            </Dialog>
        </Dialog>

        <!-- Toast para notificaciones -->
        <Toast />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'
import { useToast } from 'primevue/usetoast'
import type { Carrera } from '~/features/carreras/models/carrera-model'
import type { PlanEstudio, PlanEstudioCreate, PlanEstudioUpdate } from '~/features/plan_estudios/models/plan-estudio-mode'
import type { Materia } from '~/features/materias/models/materia-model'
import axiosInstance from "~/utils/axiosConfig"

// Definición de tipos adicionales
interface MateriaPorSemestre {
  [semestre: number]: Materia[]
}

// Composables
const toast = useToast()

// Estados reactivos
const planesEstudio = ref<PlanEstudio[]>([])
const carreras = ref<Carrera[]>([])
const loading = ref(false)

// Estados para diálogos
const showDialogCrearPlan = ref(false)
const showDialogEliminar = ref(false)
const showDialogSemestres = ref(false)
const showDialogAgregarMaterias = ref(false)

// Estados para gestión de semestres
const planSeleccionado = ref<PlanEstudio | null>(null)
const materiasDisponibles = ref<Materia[]>([])
const materiasSeleccionadas = ref<Materia[]>([])
const materiasPorSemestre = ref<MateriaPorSemestre>({})
const semestreActual = ref(1)

// Estados para formulario de plan
const modoEdicion = ref(false)
const planAEliminar = ref<PlanEstudio | null>(null)
const modelPlan = ref<PlanEstudioCreate | (PlanEstudioUpdate & { id_plan_estudio?: number })>({
  nombre: "",
  id_carrera: null as unknown as number // Corrección de tipado
})

// Validaciones
const rules = {
  nombre: { required, minLength: minLength(3) },
  id_carrera: { required }
}
const $v = useVuelidate(rules, modelPlan)

// Computed
const materiasDisponiblesFiltradas = computed(() => {
  return materiasDisponibles.value.filter(materia => 
    !materiasPorSemestre.value[semestreActual.value]?.some(m => m.id_materia === materia.id_materia)
)})

// Métodos para planes de estudio
const clickMostrarDialogoCrearPlan = () => {
  modoEdicion.value = false
  modelPlan.value = { 
    nombre: "", 
    id_carrera: null as unknown as number
  }
  $v.value.$reset()
  showDialogCrearPlan.value = true
}

const clickEditarPlan = (plan: PlanEstudio) => {
  modoEdicion.value = true
  modelPlan.value = { 
    ...plan,
    id_plan_estudio: plan.id_plan_estudio
  }
  $v.value.$reset()
  showDialogCrearPlan.value = true
}

const clickEliminarPlan = (plan: PlanEstudio) => {
  planAEliminar.value = plan
  showDialogEliminar.value = true
}

const cancelarDialog = () => {
  showDialogCrearPlan.value = false
  $v.value.$reset()
  modelPlan.value = { 
    nombre: "", 
    id_carrera: null as unknown as number
  }
}

const cargarPlanesEstudio = async () => {
  try {
    loading.value = true
    const response = await axiosInstance.get<PlanEstudio[]>("planes_estudio")
    planesEstudio.value = response.data
  } catch (error) {
    mostrarError('Error al cargar los planes de estudio')
  } finally {
    loading.value = false
  }
}

const cargarCarreras = async () => {
  try {
    const response = await axiosInstance.get<Carrera[]>("carreras")
    carreras.value = response.data
  } catch (error) {
    mostrarError('Error al cargar las carreras')
  }
}

const submitPlan = async () => {
  const isValid = await $v.value.$validate()
  if (!isValid) return

  try {
    loading.value = true
    
    if (modoEdicion.value) {
      const planUpdate = modelPlan.value as PlanEstudioUpdate & { id_plan_estudio: number }
      // Asegúrate que la URL termine con /
      const response = await axiosInstance.patch<PlanEstudio>(
        `planes_estudio/${planUpdate.id_plan_estudio}/`, 
        { nombre: planUpdate.nombre, id_carrera: planUpdate.id_carrera }
      )
      // ... resto del código
    } else {
      const planCreate = modelPlan.value as PlanEstudioCreate
      // Asegúrate que la URL termine con /
      const response = await axiosInstance.post<PlanEstudio>("planes_estudio/", planCreate)
      planesEstudio.value.push(response.data)
      mostrarExito('Plan de estudio agregado exitosamente')
    }
    
    showDialogCrearPlan.value = false
  } catch (error: any) {
    mostrarError(error.response?.data?.detail || 'Error al guardar el plan de estudio')
  } finally {
    loading.value = false
  }
}
const confirmarEliminarPlan = async () => {
  if (!planAEliminar.value) return

  try {
    loading.value = true
    await axiosInstance.delete(`planes_estudio/${planAEliminar.value.id_plan_estudio}`)
    planesEstudio.value = planesEstudio.value.filter(p => p.id_plan_estudio !== planAEliminar.value?.id_plan_estudio)
    mostrarExito('Plan de estudio eliminado exitosamente')
    showDialogEliminar.value = false
    planAEliminar.value = null
  } catch (error: any) {
    mostrarError(error.response?.data?.detail || 'Error al eliminar el plan de estudio')
  } finally {
    loading.value = false
  }
}

// Métodos para gestión de semestres
const clickGestionarSemestres = async (plan: PlanEstudio) => {
  planSeleccionado.value = plan
  materiasPorSemestre.value = {}
  showDialogSemestres.value = true
  
  try {
    loading.value = true
    await cargarMateriasDisponibles()
    await cargarMateriasPorSemestre()
  } catch (error) {
    mostrarError('Error al cargar información de semestres')
  } finally {
    loading.value = false
  }
}

const cargarMateriasDisponibles = async () => {
  try {
    const response = await axiosInstance.get<Materia[]>("materias")
    materiasDisponibles.value = response.data
  } catch (error) {
    mostrarError('Error al cargar materias disponibles')
  }
}

const cargarMateriasPorSemestre = async () => {
  if (!planSeleccionado.value) return

  try {
    const response = await axiosInstance.get<MateriaPorSemestre>(
      `planes_estudio/${planSeleccionado.value.id_plan_estudio}/semestres/materias`
    )
    materiasPorSemestre.value = response.data
  } catch (error) {
    mostrarError('Error al cargar materias por semestre')
  }
}

const abrirSelectorMaterias = (semestre: number) => {
  semestreActual.value = semestre
  materiasSeleccionadas.value = []
  showDialogAgregarMaterias.value = true
}

const asignarMaterias = async () => {
  if (!planSeleccionado.value || materiasSeleccionadas.value.length === 0) return;

  try {
    loading.value = true;
    for (const materia of materiasSeleccionadas.value) {
      await axiosInstance.post(
        `/planes_estudio/${planSeleccionado.value.id_plan_estudio}/materias`,
        {
          id_materia: materia.id_materia,
          semestre: semestreActual.value
        }
      );
    }
    mostrarExito('Materias asignadas correctamente');
    showDialogAgregarMaterias.value = false;
    await cargarMateriasPorSemestre();
  } catch (error: any) {
    mostrarError(error.response?.data?.detail || 'Error al asignar materias');
  } finally {
    loading.value = false;
    materiasSeleccionadas.value = [];
  }
};

const desasignarMateria = async (materia: Materia, semestre: number) => {
  if (!planSeleccionado.value) return

  try {
    loading.value = true
    await axiosInstance.delete(
      `planes_estudio/${planSeleccionado.value.id_plan_estudio}/materias/${materia.id_materia}`,
      { params: { semestre } }
    )
    mostrarExito('Materia desasignada')
    await cargarMateriasPorSemestre()
  } catch (error) {
    mostrarError('Error al desasignar materia')
  } finally {
    loading.value = false
  }
}

// Helpers
const mostrarExito = (mensaje: string) => {
  toast.add({ severity: 'success', summary: 'Éxito', detail: mensaje, life: 3000 })
}

const mostrarError = (mensaje: string) => {
  toast.add({ severity: 'error', summary: 'Error', detail: mensaje, life: 3000 })
  console.error(mensaje)
}

// Lifecycle
onMounted(async () => {
  await Promise.all([cargarPlanesEstudio(), cargarCarreras()])
})
</script>

<style scoped>
.field {
    margin-bottom: 1rem;
}

.p-invalid {
    border-color: #e24c4c;
}

.p-error {
    color: #e24c4c;
    font-size: 0.875rem;
}
</style>