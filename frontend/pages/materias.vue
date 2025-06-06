<template>
  <div>
    <div class="card">
      <Toolbar class="mb-6">
        <template #start>
          <Button label="Nuevo" icon="pi pi-plus" class="mr-2" @click="clickMostrarDialogoCrearMateria" />
          <Button label="Eliminar" icon="pi pi-trash" severity="danger" outlined @click="confirmDeleteSelected" :disabled="!selectedProducts || !selectedProducts.length" />
        </template>
      </Toolbar>

      <DataTable
        ref="dt"
        v-model:selection="selectedProducts"
        :value="materias"
        dataKey="id_materia"
        :paginator="true"
        :rows="5"
        :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
      >
        <template #header>
          <div class="flex justify-end">
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText v-model="filters['global'].value" placeholder="Buscar..." />
            </span>
          </div>
        </template>

        <Column selectionMode="multiple" style="width: 3rem" :exportable="false" />
        <Column field="id_materia" header="ID" sortable style="min-width: 8rem" />
        <Column field="nombre" header="Nombre" sortable style="min-width: 16rem" />
        <Column field="creditos" header="Créditos" sortable style="min-width: 8rem" />
        <Column field="tipo" header="Tipo" sortable style="min-width: 12rem" />
        <Column field="modulo.nombre" header="Módulo" sortable style="min-width: 12rem" />
        <Column header="Acciones" style="min-width: 8rem">
          <template #body="slotProps">
            <Button icon="pi pi-pencil" rounded text @click="editProduct(slotProps.data)" />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Diálogo de nuevo/editar materia -->
    <Dialog v-model:visible="showDialogCrearMateria" :style="{ width: '450px' }" :header="modoEdicion ? 'Editar Materia' : 'Nueva Materia'" :modal="true" class="p-fluid">
      <div class="p-4 space-y-4">
        <div>
          <label for="nombre" class="block font-semibold mb-1">Nombre*</label>
          <InputText 
            id="nombre" 
            v-model.trim="modelMateria.nombre" 
            required 
            autofocus 
            class="w-full" 
            :class="{ 'p-invalid': submitted && !modelMateria.nombre }"
          />
          <small class="p-error" v-if="submitted && !modelMateria.nombre">
            El nombre es obligatorio
          </small>
        </div>
        
        <div>
          <label for="creditos" class="block font-semibold mb-1">Créditos*</label>
          <InputNumber 
            id="creditos" 
            v-model="modelMateria.creditos" 
            inputId="integeronly" 
            class="w-full" 
            :min="1" 
            :class="{ 'p-invalid': submitted && (!modelMateria.creditos || modelMateria.creditos <= 0) }"
          />
          <small class="p-error" v-if="submitted && (!modelMateria.creditos || modelMateria.creditos <= 0)">
            Los créditos deben ser un número positivo
          </small>
        </div>
        
        <div>
          <label for="tipo" class="block font-semibold mb-1">Tipo*</label>
          <Dropdown 
            id="tipo"
            v-model="modelMateria.tipo" 
            :options="tipos"
            optionLabel="label"
            optionValue="value"
            placeholder="Selecciona un tipo"
            class="w-full"
            :class="{ 'p-invalid': submitted && !modelMateria.tipo }"
            @change="handleTipoChange"
          />
          <small class="p-error" v-if="submitted && !modelMateria.tipo">
            Debe seleccionar un tipo
          </small>
        </div>
        
        <!-- Campo Módulo (solo visible si tipo es 'Materia') -->
        <div v-if="modelMateria.tipo === 'Módulo'">
          <label for="modulo" class="block font-semibold mb-1">Módulo*</label>
          <Dropdown
            id="modulo"
            v-model="modelMateria.id_modulo"
            :options="modulos"
            optionLabel="nombre"
            optionValue="id_modulo"
            placeholder="Selecciona un módulo"
            class="w-full"
            :class="{ 'p-invalid': submitted && modelMateria.tipo === 'Módulo' && !modelMateria.id_modulo }"
          />
          <small class="p-error" v-if="submitted && modelMateria.tipo === 'Módulo' && !modelMateria.id_modulo">
            El módulo es obligatorio para materias
          </small>
        </div>
      </div>
      
      <template #footer>
        <Button label="Cancelar" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Guardar" icon="pi pi-check" @click="clickAgregarMateria" />
      </template>
    </Dialog>

    <!-- Diálogo de confirmación para eliminar -->
    <Dialog v-model:visible="deleteProductsDialog" :style="{ width: '450px' }" header="Confirmar" :modal="true">
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle !text-3xl" />
        <span>¿Estás seguro de que deseas eliminar las materias seleccionadas?</span>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" text @click="deleteProductsDialog = false" />
        <Button label="Sí" icon="pi pi-check" @click="deleteSelectedProducts" />
      </template>
    </Dialog>
    
    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axiosInstance from "~/utils/axiosConfig";
import { useToast } from 'primevue/usetoast';

const toast = useToast();

interface Materia {
  id_materia?: number;
  nombre: string;
  creditos: number | null;
  tipo: string;
  id_modulo?: number | null;
  modulo?: {
    id_modulo: number;
    nombre: string;
  };
}

interface TipoOption {
  label: string;
  value: string;
}

// Definir las variables reactivas
const materias = ref<Materia[]>([]);
const selectedProducts = ref<Materia[]>([]);
const filters = ref({
  global: { value: null, matchMode: 'contains' }
});
const showDialogCrearMateria = ref(false);
const deleteProductsDialog = ref(false);
const modoEdicion = ref(false);
const submitted = ref(false);

const modelMateria = ref<Materia>({ 
  nombre: "", 
  creditos: null, 
  tipo: "",
  id_modulo: null
});

const tipos = ref<TipoOption[]>([
  { label: 'Materia', value: 'Materia' },
  { label: 'Módulo', value: 'Módulo' }
]);

const modulos = ref<Array<{id_modulo: number, nombre: string}>>([]);

// Cargar las materias y módulos al montar el componente
onMounted(async () => {
  await Promise.all([cargarMaterias(), cargarModulos()]);
});

const cargarMaterias = async () => {
  try {
    const response = await axiosInstance.get("materias");
    materias.value = response.data;
  } catch (error) {
    console.error("Error completo:", error); // Agrega esto
    mostrarError('Error al cargar las materias');
  }
};

const cargarModulos = async () => {
  try {
    const response = await axiosInstance.get("modulos");
    modulos.value = response.data;
  } catch (error) {
    mostrarError('Error al cargar los módulos');
    console.error("Error fetching modulos:", error);
  }
};

const clickMostrarDialogoCrearMateria = () => {
  modoEdicion.value = false;
  modelMateria.value = { nombre: "", creditos: null, tipo: "", id_modulo: null };
  submitted.value = false;
  showDialogCrearMateria.value = true;
};

const hideDialog = () => {
  showDialogCrearMateria.value = false;
  submitted.value = false;
};

const handleTipoChange = () => {
  if (modelMateria.value.tipo === 'Materia') {
    modelMateria.value.id_modulo = null;
  }
};

const clickAgregarMateria = async () => {
  if (!validarFormulario()) return;

  const payload = {
    nombre: modelMateria.value.nombre,
    creditos: modelMateria.value.creditos,
    tipo: modelMateria.value.tipo,
    id_modulo: modelMateria.value.tipo === "Módulo" ? modelMateria.value.id_modulo || null : null
  };

  try {
    const response = await axiosInstance.post("materias", payload);
    materias.value.push(response.data);
    showDialogCrearMateria.value = false;
    await cargarMaterias();
  } catch (error: any) {
    console.error("Error:", error);
    alert(error.response?.data?.detail || "Error al crear la materia");
  }
};

const validarFormulario = (): boolean => {
  submitted.value = true;
  
  // Validación del nombre
  if (!modelMateria.value.nombre.trim()) {
    return false;
  }
  
  // Validación de créditos
  if (modelMateria.value.creditos === null || modelMateria.value.creditos <= 0) {
    return false;
  }
  
  // Validación del tipo
  if (!modelMateria.value.tipo) {
    return false;
  }
  
  // Validación del módulo (solo si es tipo "Módulo")
  if (modelMateria.value.tipo === 'Módulo' && !modelMateria.value.id_modulo) {
    return false;
  }
  
  return true;
};
const confirmDeleteSelected = () => {
  if (selectedProducts.value.length > 0) {
    deleteProductsDialog.value = true;
  }
};

const deleteSelectedProducts = async () => {
  try {
    const ids = selectedProducts.value.map((materia) => materia.id_materia);
    await axiosInstance.delete("materias", { data: { ids } });
    materias.value = materias.value.filter((materia) => !ids.includes(materia.id_materia));
    selectedProducts.value = [];
    deleteProductsDialog.value = false;
    mostrarExito('Materias eliminadas correctamente');
  } catch (error) {
    mostrarError('Error al eliminar materias');
    console.error("Error deleting materias:", error);
  }
};

const editProduct = (materia: Materia) => {
  modoEdicion.value = true;
  modelMateria.value = { ...materia };
  submitted.value = false;
  showDialogCrearMateria.value = true;
};

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