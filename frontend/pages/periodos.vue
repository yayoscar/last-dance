<template>
  <div>
    <!-- Título -->
    <div class="flex justify-center items-center gap-3 mb-4">
      <i class="pi pi-calendar animate-bounce text-3xl text-blue-600" />
      <h2 class="text-3xl font-semibold animate-fade-in">Periodos</h2>
    </div>

    <div class="card">
      <Toolbar class="mb-6">
        <template #start>
          <Button label="Nuevo" icon="pi pi-plus" class="mr-2" @click="showDialogCrearPeriodo" />
          <Button
            label="Eliminar"
            icon="pi pi-trash"
            severity="danger"
            outlined
            @click="confirmDeleteSelected"
            :disabled="!selectedPeriods.length"
          />
        </template>
      </Toolbar>

      <DataTable
        ref="dt"
        v-model:selection="selectedPeriods"
        :value="periods"
        dataKey="id_periodo"
        :paginator="true"
        :rows="5"
        :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
      >
        <template #header>
          <div class="flex justify-end">
            <IconField>
              <InputIcon><i class="pi pi-search" /></InputIcon>
            </IconField>
          </div>
        </template>

        <Column selectionMode="multiple" style="width: 3rem" :exportable="false" />
        <Column field="periodo" header="Periodo" sortable style="min-width: 12rem" />
        <Column field="fecha_inicio" header="Fecha Inicio" sortable style="min-width: 10rem" />
        <Column field="fecha_fin" header="Fecha Fin" sortable style="min-width: 10rem" />
      </DataTable>
    </div>

    <!-- Diálogo crear periodo -->
    <Dialog v-model:visible="showDialog" header="Agregar Periodo" :modal="true" :style="{ width: '40rem' }">
      <div class="field mb-4">
        <label class="font-semibold block mb-1">Periodo</label>
        <InputText v-model="newPeriodo.periodo" autocomplete="off" />
      </div>
      <div class="field mb-4">
        <label class="font-semibold block mb-1">Fecha Inicio</label>
        <InputText v-model="newPeriodo.fecha_inicio" type="date" />
      </div>
      <div class="field mb-4">
        <label class="font-semibold block mb-1">Fecha Fin</label>
        <InputText v-model="newPeriodo.fecha_fin" type="date" />
      </div>

      <div class="flex justify-end gap-2">
        <Button label="Cancelar" severity="secondary" @click="showDialog = false" />
        <Button label="Agregar" severity="primary" @click="agregarPeriodo" />
      </div>
    </Dialog>

    <!-- Diálogo eliminar -->
    <Dialog v-model:visible="deletePeriodsDialog" :style="{ width: '450px' }" header="Confirmar" :modal="true">
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle !text-3xl" />
        <span>¿Estás seguro de que deseas eliminar el/los periodo(s) seleccionado(s)?</span>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" text @click="deletePeriodsDialog = false" />
        <Button label="Sí" icon="pi pi-check" @click="deleteSelectedPeriods" />
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { FilterMatchMode } from '@primevue/core/api'
import axiosInstance from '~/utils/axiosConfig'

const periods = ref([])
const selectedPeriods = ref([])
const filters = ref({})
const deletePeriodsDialog = ref(false)
const showDialog = ref(false)
const newPeriodo = ref({
  periodo: '',
  fecha_inicio: '',
  fecha_fin: ''
})

const initFilters = () => {
  filters.value = {
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
  }
}

const loadPeriods = async () => {
  try {
    const response = await axiosInstance.get('periodos')
    periods.value = response.data
  } catch (error) {
    console.error('Error al cargar periodos:', error)
  }
}

const agregarPeriodo = async () => {
  if(!newPeriodo.value.periodo || !newPeriodo.value.fecha_inicio || !newPeriodo.value.fecha_fin){
    alert("Por favor llena todos los campos");
    return;
  }
  try {
    const response = await axiosInstance.post('periodos', newPeriodo.value)
    periods.value.push(response.data)
    showDialog.value = false
    newPeriodo.value = { periodo: '', fecha_inicio: '', fecha_fin: '' }
  } catch (error) {
    console.error('Error al agregar periodo:', error)
  }
}

const deleteSelectedPeriods = async () => {
  try {
    const promises = selectedPeriods.value.map(periodo =>
      axiosInstance.delete(`periodos/${periodo.id_periodo}`)
    )
    await Promise.all(promises)

    periods.value = periods.value.filter(
      p => !selectedPeriods.value.some(sel => sel.id_periodo === p.id_periodo)
    )

    selectedPeriods.value = []
    deletePeriodsDialog.value = false
  } catch (error) {
    console.error('Error eliminando periodos:', error)
  }
}

const confirmDeleteSelected = () => {
  deletePeriodsDialog.value = true
}

const showDialogCrearPeriodo = () => {
  showDialog.value = true
}

onMounted(() => {
  //initFilters()
  loadPeriods();
})
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fade-in 0.6s ease-out;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}
.animate-bounce {
  animation: bounce 1.2s infinite ease-in-out;
}
</style>
