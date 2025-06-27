<template>
  <div>
    <Card>
      <template #title>Alumnos</template>

      <template #content>
        <DataTable :value="alumnos" stripedRows>
          <template #header>
            <div class="flex justify-end">
              <Button 
                @click="clickMostrarDialogoAgregarAGrupo"
                label="Agregar a Grupo" 
                icon="pi pi-users"
              />
            </div>
          </template>

          <Column field="nombre" header="Nombre"></Column>
          <Column field="ape_paterno" header="Apellido Paterno"></Column>
          <Column field="ape_materno" header="Apellido Materno"></Column>
          <Column field="num_control" header="Núm. Control"></Column>
          <Column field="turno" header="Turno"></Column>
          <Column field="generacion" header="Generación"></Column>
        </DataTable>
      </template>
    </Card>

    <!-- Dialog Asignar Grupo -->
    <Dialog 
      v-model:visible="showDialogAsignarGrupo" 
      modal 
      header="Agregar Alumnos a Grupo" 
      :style="{ width: '40rem' }"
    >
      <div class="field">
        <label class="font-semibold">Selecciona los alumnos</label>
        <MultiSelect 
          v-model="alumnosSeleccionados"
          :options="alumnos"
          optionLabel="nombre"
          placeholder="Selecciona alumnos"
          filter
          class="w-full"
        />
      </div>

      <div class="field mt-4">
        <label class="font-semibold">Selecciona el grupo</label>
        <Dropdown 
          v-model="grupoSeleccionado"
          :options="grupos"
          optionLabel="nombre"
          optionValue="id_grupo"
          placeholder="Selecciona un grupo"
          class="w-full"
        />
      </div>

      <div class="flex justify-end gap-2 mt-4">
        <Button label="Cancelar" severity="secondary" @click="cancelarDialogoGrupo" />
        <Button label="Agregar" severity="primary" :loading="loading" @click="agregarAlumnosAGrupo" />
      </div>
    </Dialog>

    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import type { Alumno } from '~/features/alumnos/models/alumno-mode'
import type { Grupo } from '~/features/grupos/models/grupo-mode'
import axiosInstance from '~/utils/axiosConfig'

const toast = useToast()
const alumnos = ref<Alumno[]>([])
const grupos = ref<Grupo[]>([])
const alumnosSeleccionados = ref<Alumno[]>([])
const grupoSeleccionado = ref<number | null>(null)
const showDialogAsignarGrupo = ref(false)
const loading = ref(false)

const cargarAlumnos = async () => {
  try {
    const response = await axiosInstance.get<Alumno[]>("alumnos")
    alumnos.value = response.data
  } catch (error) {
    console.error("Error al cargar alumnos:", error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudieron cargar los alumnos',
      life: 3000
    })
  }
}

const cargarGrupos = async () => {
  try {
    const response = await axiosInstance.get<Grupo[]>("grupos")
    grupos.value = response.data
  } catch (error) {
    console.error("Error al cargar grupos:", error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudieron cargar los grupos',
      life: 3000
    })
  }
}

const clickMostrarDialogoAgregarAGrupo = async () => {
  alumnosSeleccionados.value = []
  grupoSeleccionado.value = null
  await Promise.all([cargarAlumnos(), cargarGrupos()])
  showDialogAsignarGrupo.value = true
}

const agregarAlumnosAGrupo = async () => {
  if (!grupoSeleccionado.value) return

  try {
    loading.value = true
    const ids = alumnosSeleccionados.value.map(a => a.id_alumno)
    await axiosInstance.post(`grupos/${grupoSeleccionado.value}/alumnos`, { alumnos: ids })
    toast.add({
      severity: 'success',
      summary: 'Éxito',
      detail: 'Alumnos agregados correctamente',
      life: 3000
    })
    showDialogAsignarGrupo.value = false
  } catch (error: any) {
    console.error("Error al agregar alumnos al grupo:", error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.response?.data?.detail || 'Error al agregar alumnos al grupo',
      life: 3000
    })
  } finally {
    loading.value = false
  }
}

const cancelarDialogoGrupo = () => {
  showDialogAsignarGrupo.value = false
  alumnosSeleccionados.value = []
  grupoSeleccionado.value = null
}

onMounted(() => {
  cargarAlumnos()
})
</script>

<style scoped>
.field {
  margin-bottom: 1rem;
}
</style>
