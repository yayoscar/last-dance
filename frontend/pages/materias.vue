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
        :value="Materias"
        dataKey="id"
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
        <Column field="codigo" header="Código" sortable style="min-width: 12rem" />
        <Column field="nombre" header="Nombre" sortable style="min-width: 16rem" />
        <Column field="creditos" header="Créditos" sortable style="min-width: 8rem" />
        <Column field="tipo.name" header="Tipo" sortable style="min-width: 12rem" />
        <Column header="Acciones" style="min-width: 8rem">
          <template #body="slotProps">
            <Button icon="pi pi-pencil" rounded text @click="editProduct(slotProps.data)" />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Diálogo de nuevo/editar producto -->
    <Dialog v-model:visible="showDialogCrearMateria" :style="{ width: '450px' }" header="Nuevo Producto" :modal="true" class="p-fluid">
      <div class="p-4 space-y-4">
        <div>
          <label for="nombre" class="block font-semibold mb-1">Nombre</label>
          <InputText id="nombre" v-model.trim="modelMateria.nombre" required autofocus class="w-full" />
        </div>
        <div>
          <label for="creditos" class="block font-semibold mb-1">Créditos</label>
          <InputNumber id="creditos" v-model="modelMateria.creditos" inputId="integeronly" class="w-full" />
        </div>
        <div>
          <label for="tipo" class="block font-semibold mb-1">Tipo</label>
          <Dropdown v-model="modelMateria.tipo" :options="tipos" optionLabel="name" placeholder="Selecciona un tipo" class="w-full" />
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axiosInstance from "~/utils/axiosConfig";

// Definir las variables reactivas
const Materias = ref<any[]>([]); // Lista de materias
const selectedProducts = ref<any[]>([]); // Productos seleccionados
const filters = ref({ global: { value: null } }); // Filtro global para búsqueda
const showDialogCrearMateria = ref(false); // Controla el diálogo de creación
const deleteProductsDialog = ref(false); // Controla el diálogo de eliminación
const modelMateria = ref({ nombre: "", creditos: null, tipo: null }); // Objeto para crear/editar materia
const tipos = ref([{ name: "Teórico" }, { name: "Práctico" }]); // Tipos de materias de ejemplo

// Cargar las materias cuando se monta el componente
onMounted(async () => {
    try {
        const response = await axiosInstance.get("materias");
        if (response.data && Array.isArray(response.data)) {
            Materias.value = response.data; // Actualizar las materias si la respuesta es válida
        }
    } catch (error) {
        console.error("Error fetching materias:", error);
    }
});

// Mostrar diálogo para agregar nueva materia
const clickMostrarDialogoCrearMateria = () => {
    modelMateria.value = { nombre: "", creditos: null, tipo: null }; // Limpiar el modelo
    showDialogCrearMateria.value = true;
};

// Función para agregar una nueva materia
const clickAgregarMateria = async () => {
    if (!modelMateria.value.nombre || !modelMateria.value.creditos || !modelMateria.value.tipo) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    try {
        const response = await axiosInstance.post("materias", modelMateria.value);
        if (response.data) {
            Materias.value.push(response.data); // Agregar la nueva materia a la lista
            showDialogCrearMateria.value = false; // Cerrar el diálogo
            modelMateria.value = { nombre: "", creditos: null, tipo: null }; // Limpiar el formulario
        }
    } catch (error) {
        console.error("Error adding materia:", error);
    }
};

// Función para eliminar las materias seleccionadas
const confirmDeleteSelected = () => {
    if (selectedProducts.value.length > 0) {
        deleteProductsDialog.value = true; // Mostrar el diálogo de confirmación
    }
};

// Eliminar materias seleccionadas
const deleteSelectedProducts = async () => {
    try {
        const ids = selectedProducts.value.map((p: any) => p.id); // Obtener los ids de las materias seleccionadas
        const response = await axiosInstance.delete("materias", { data: { ids } });
        if (response.data) {
            // Eliminar las materias de la lista local
            Materias.value = Materias.value.filter((materia: any) => !ids.includes(materia.id));
            selectedProducts.value = []; // Limpiar selección
            deleteProductsDialog.value = false; // Cerrar el diálogo de confirmación
        }
    } catch (error) {
        console.error("Error deleting materias:", error);
    }
};
</script>

<style scoped lang="css">
</style>
