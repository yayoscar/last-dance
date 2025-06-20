<template>
  <div>
    <div class="card">
      <Toolbar class="mb-6">
        <template #start>
          <Button 
            label="Nuevo Módulo" 
            icon="pi pi-plus" 
            class="mr-2" 
            @click="showDialogCrearModulo" 
          />
          <Button 
            label="Eliminar" 
            icon="pi pi-trash" 
            severity="danger" 
            outlined 
            @click="confirmDeleteSelected" 
            :disabled="!selectedModulos || !selectedModulos.length" 
          />
        </template>
      </Toolbar>

      <DataTable
        ref="dt"
        v-model:selection="selectedModulos"
        :value="modulos"
        dataKey="id_modulo"
        :paginator="true"
        :rows="10"
        :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} módulos"
        :rowsPerPageOptions="[5,10,25]"
      >
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-bold">Gestión de Módulos</h2>
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText 
                v-model="filters['global'].value" 
                placeholder="Buscar módulos..." 
              />
            </span>
          </div>
        </template>

        <Column selectionMode="multiple" style="width: 3rem" :exportable="false" />
        <Column field="id_modulo" header="ID" sortable style="min-width: 6rem" />
        <Column field="nombre" header="Nombre" sortable style="min-width: 16rem" />
        <Column header="Acciones" style="min-width: 8rem">
          <template #body="slotProps">
            <Button 
              icon="pi pi-pencil" 
              rounded 
              text 
              severity="secondary" 
              @click="editModulo(slotProps.data)" 
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Diálogo para crear/editar módulo -->
    <Dialog 
      v-model:visible="showDialog" 
      :style="{ width: '450px' }" 
      :header="dialogTitle" 
      :modal="true" 
      class="p-fluid"
    >
      <div class="p-4 space-y-4">
        <div>
          <label for="nombre" class="block font-semibold mb-1">Nombre del módulo*</label>
          <InputText 
            id="nombre" 
            v-model.trim="moduloForm.nombre" 
            required 
            autofocus 
            class="w-full" 
            :class="{ 'p-invalid': submitted && !moduloForm.nombre }"
          />
          <small class="p-error" v-if="submitted && !moduloForm.nombre">
            El nombre es obligatorio
          </small>
        </div>
      </div>

      <template #footer>
        <Button 
          label="Cancelar" 
          icon="pi pi-times" 
          text 
          @click="hideDialog" 
        />
        <Button 
          label="Guardar" 
          icon="pi pi-check" 
          @click="saveModulo" 
        />
      </template>
    </Dialog>

    <!-- Diálogo de confirmación para eliminar -->
    <Dialog 
      v-model:visible="deleteDialog" 
      :style="{ width: '450px' }" 
      header="Confirmar eliminación" 
      :modal="true"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle text-red-500 text-3xl" />
        <span v-if="selectedModulos.length > 1">
          ¿Estás seguro de que deseas eliminar los {{ selectedModulos.length }} módulos seleccionados?
        </span>
        <span v-else>
          ¿Estás seguro de que deseas eliminar el módulo seleccionado?
        </span>
      </div>
      <template #footer>
        <Button 
          label="No" 
          icon="pi pi-times" 
          text 
          @click="deleteDialog = false" 
        />
        <Button 
          label="Sí" 
          icon="pi pi-check" 
          severity="danger" 
          @click="deleteModulos" 
        />
      </template>
    </Dialog>

    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axiosInstance from '~/utils/axiosConfig';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

interface Modulo {
  id_modulo?: number;
  nombre: string;
}

// Datos reactivos
const modulos = ref<Modulo[]>([]);
const selectedModulos = ref<Modulo[]>([]);
const filters = ref({
  global: { value: null, matchMode: 'contains' }
});
const showDialog = ref(false);
const deleteDialog = ref(false);
const submitted = ref(false);
const isEditing = ref(false);
const currentModuloId = ref<number | null>(null);

// Formulario
const moduloForm = ref<Modulo>({
  nombre: ''
});

// Título dinámico del diálogo
const dialogTitle = ref('');

// Cargar módulos al montar el componente
onMounted(() => {
  loadModulos();
});

// Cargar lista de módulos
const loadModulos = async () => {
  try {
    const response = await axiosInstance.get('/modulos');
    modulos.value = response.data;
  } catch (error) {
    showError('Error al cargar los módulos');
    console.error('Error loading modulos:', error);
  }
};

// Mostrar diálogo para crear nuevo módulo
const showDialogCrearModulo = () => {
  moduloForm.value = { nombre: '' };
  dialogTitle.value = 'Nuevo Módulo';
  isEditing.value = false;
  submitted.value = false;
  showDialog.value = true;
};
const editModulo = (modulo: Modulo) => {
  moduloForm.value = { ...modulo };
  dialogTitle.value = 'Editar Módulo';
  currentModuloId.value = modulo.id_modulo ?? null; // Usamos el operador de coalescencia nula para convertir undefined en null
  isEditing.value = true;
  submitted.value = false;
  showDialog.value = true;
};
// Ocultar diálogo
const hideDialog = () => {
  showDialog.value = false;
  submitted.value = false;
};

// Guardar módulo (crear o actualizar)
const saveModulo = async () => {
  submitted.value = true;

  if (!moduloForm.value.nombre.trim()) {
    return;
  }

  try {
    if (isEditing.value && currentModuloId.value) {
      // Actualizar módulo existente
      await axiosInstance.put(`/modulos/${currentModuloId.value}`, moduloForm.value);
      showSuccess('Módulo actualizado correctamente');
    } else {
      // Crear nuevo módulo
      await axiosInstance.post('/modulos', moduloForm.value);
      showSuccess('Módulo creado correctamente');
    }

    await loadModulos();
    showDialog.value = false;
  } catch (error) {
    showError('Error al guardar el módulo');
    console.error('Error saving modulo:', error);
  }
};

// Confirmar eliminación
const confirmDeleteSelected = () => {
  if (selectedModulos.value.length > 0) {
    deleteDialog.value = true;
  }
};

// Eliminar módulos seleccionados
const deleteModulos = async () => {
  try {
    const ids = selectedModulos.value.map(m => m.id_modulo);
    await axiosInstance.delete('/modulos', { 
      data: { ids } 
    });
    
    showSuccess(
      selectedModulos.value.length > 1 
        ? 'Módulos eliminados correctamente' 
        : 'Módulo eliminado correctamente'
    );
    
    await loadModulos();
    selectedModulos.value = [];
    deleteDialog.value = false;
  } catch (error) {
    showError('Error al eliminar los módulos');
    console.error('Error deleting modulos:', error);
  }
};

// Mostrar notificación de éxito
const showSuccess = (message: string) => {
  toast.add({
    severity: 'success',
    summary: 'Éxito',
    detail: message,
    life: 3000
  });
};

// Mostrar notificación de error
const showError = (message: string) => {
  toast.add({
    severity: 'error',
    summary: 'Error',
    detail: message,
    life: 3000
  });
};
</script>

<style scoped>
/* Estilos personalizados */
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
</style>