<template>
  <div>
    <div class="card">
      <Toolbar class="mb-6">
        <template #start>
          <Button label="Nuevo" icon="pi pi-plus" class="mr-2" @click="mostrarDialogoCrearGrupo" />
          <Button 
            label="Eliminar" 
            icon="pi pi-trash" 
            severity="danger" 
            outlined 
            @click="confirmarEliminacionSeleccionados" 
            :disabled="!gruposSeleccionados || !gruposSeleccionados.length" 
          />
        </template>
      </Toolbar>

      <DataTable
        ref="dt"
        v-model:selection="gruposSeleccionados"
        :value="grupos"
        dataKey="id_grupo"
        :paginator="true"
        :rows="10"
        :filters="filtros"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
        :rowsPerPageOptions="[5,10,25]"
      >
        <template #header>
          <div class="flex justify-end">
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText v-model="filtros['global'].value" placeholder="Buscar..." />
            </span>
          </div>
        </template>

        <Column selectionMode="multiple" style="width: 3rem" :exportable="false" />
        <Column field="id_grupo" header="ID" sortable style="min-width: 8rem" />
        <Column field="nombre" header="Nombre" sortable style="min-width: 16rem" />
        <Column field="tipo" header="Tipo" sortable style="min-width: 12rem" />
        <Column field="turno" header="Turno" sortable style="min-width: 12rem" />
        <Column header="Acciones" style="min-width: 8rem">
          <template #body="slotProps">
            <Button icon="pi pi-pencil" rounded text @click="editarGrupo(slotProps.data)" />
          <Button 
      icon="pi pi-file-excel" 
      rounded 
      text 
      @click="descargarPlantilla(slotProps.data.id_grupo)"
      severity="info"
      v-tooltip.top="'Descargar plantilla de calificaciones'"
    />
        </template>
        </Column>
      </DataTable>
    </div>

    <!-- Diálogo de nuevo/editar grupo -->
    <Dialog 
      v-model:visible="mostrarDialogoGrupo" 
      :style="{ width: '450px' }" 
      :header="modoEdicion ? 'Editar Grupo' : 'Nuevo Grupo'" 
      :modal="true" 
      class="p-fluid"
    >
      <div class="p-4 space-y-4">
        <div>
          <label for="nombre" class="block font-semibold mb-1">Nombre*</label>
          <InputText 
            id="nombre" 
            v-model.trim="modeloGrupo.nombre" 
            required 
            autofocus 
            class="w-full" 
            :class="{ 'p-invalid': enviado && !modeloGrupo.nombre }"
          />
          <small class="p-error" v-if="enviado && !modeloGrupo.nombre">
            El nombre es obligatorio
          </small>
        </div>
        
        <div>
          <label for="tipo" class="block font-semibold mb-1">Tipo*</label>
          <Dropdown 
            id="tipo"
            v-model="modeloGrupo.tipo" 
            :options="tiposGrupo"
            optionLabel="label"
            optionValue="value"
            placeholder="Selecciona un tipo"
            class="w-full"
            :class="{ 'p-invalid': enviado && !modeloGrupo.tipo }"
          />
          <small class="p-error" v-if="enviado && !modeloGrupo.tipo">
            Debe seleccionar un tipo
          </small>
        </div>
        
        <div>
          <label for="turno" class="block font-semibold mb-1">Turno*</label>
          <Dropdown 
            id="turno"
            v-model="modeloGrupo.turno" 
            :options="turnos"
            optionLabel="label"
            optionValue="value"
            placeholder="Selecciona un turno"
            class="w-full"
            :class="{ 'p-invalid': enviado && !modeloGrupo.turno }"
          />
          <small class="p-error" v-if="enviado && !modeloGrupo.turno">
            Debe seleccionar un turno
          </small>
        </div>
      </div>
      
      <template #footer>
        <Button label="Cancelar" icon="pi pi-times" text @click="ocultarDialogo" />
        <Button 
          label="Guardar" 
          icon="pi pi-check" 
          @click="modoEdicion ? actualizarGrupo() : crearGrupo()" 
        />
      </template>
    </Dialog>

    <!-- Diálogo de confirmación para eliminar -->
    <Dialog 
      v-model:visible="mostrarDialogoConfirmacionEliminar" 
      :style="{ width: '450px' }" 
      header="Confirmar" 
      :modal="true"
    >
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle !text-3xl" />
        <span>¿Estás seguro de que deseas eliminar los grupos seleccionados?</span>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" text @click="mostrarDialogoConfirmacionEliminar = false" />
        <Button label="Sí" icon="pi pi-check" @click="eliminarGruposSeleccionados" />
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

interface Grupo {
  id_grupo?: number;
  nombre: string;
  tipo: string;
  turno: string;
}

interface OpcionDropdown {
  label: string;
  value: string;
}

// Variables reactivas
const grupos = ref<Grupo[]>([]);
const gruposSeleccionados = ref<Grupo[]>([]);
const filtros = ref({
  global: { value: null, matchMode: 'contains' }
});
const mostrarDialogoGrupo = ref(false);
const mostrarDialogoConfirmacionEliminar = ref(false);
const modoEdicion = ref(false);
const enviado = ref(false);

const modeloGrupo = ref<Grupo>({ 
  nombre: "", 
  tipo: "", 
  turno: ""
});

const tiposGrupo = ref<OpcionDropdown[]>([
  { label: 'Regular', value: 'Regular' },
  { label: 'Especial', value: 'Especial' },
  { label: 'Intensivo', value: 'Intensivo' }
]);

const turnos = ref<OpcionDropdown[]>([
  { label: 'Matutino', value: 'Matutino' },
  { label: 'Vespertino', value: 'Vespertino' },
  { label: 'Nocturno', value: 'Nocturno' }
]);

// Cargar datos al montar el componente
onMounted(async () => {
  await cargarGrupos();
});

const cargarGrupos = async () => {
  try {
    const response = await axiosInstance.get("grupos");
    grupos.value = response.data;
  } catch (error) {
    mostrarError('Error al cargar los grupos');
    console.error("Error cargando grupos:", error);
  }
};

const mostrarDialogoCrearGrupo = () => {
  modoEdicion.value = false;
  modeloGrupo.value = { nombre: "", tipo: "", turno: "" };
  enviado.value = false;
  mostrarDialogoGrupo.value = true;
};

const ocultarDialogo = () => {
  mostrarDialogoGrupo.value = false;
  enviado.value = false;
};

const validarFormulario = (): boolean => {
  enviado.value = true;
  
  if (!modeloGrupo.value.nombre.trim()) return false;
  if (!modeloGrupo.value.tipo) return false;
  if (!modeloGrupo.value.turno) return false;
  
  return true;
};

const crearGrupo = async () => {
  if (!validarFormulario()) return;

  try {
    const response = await axiosInstance.post("grupos", modeloGrupo.value);
    grupos.value.push(response.data);
    mostrarDialogoGrupo.value = false;
    mostrarExito('Grupo creado correctamente');
    await cargarGrupos();
  } catch (error: any) {
    console.error("Error:", error);
    mostrarError(error.response?.data?.detail || "Error al crear el grupo");
  }
};

const editarGrupo = (grupo: Grupo) => {
  modoEdicion.value = true;
  modeloGrupo.value = { ...grupo };
  enviado.value = false;
  mostrarDialogoGrupo.value = true;
};

const actualizarGrupo = async () => {
  if (!validarFormulario() || !modeloGrupo.value.id_grupo) return;

  try {
    await axiosInstance.put(`grupos/${modeloGrupo.value.id_grupo}`, modeloGrupo.value);
    mostrarDialogoGrupo.value = false;
    mostrarExito('Grupo actualizado correctamente');
    await cargarGrupos();
  } catch (error: any) {
    console.error("Error:", error);
    mostrarError(error.response?.data?.detail || "Error al actualizar el grupo");
  }
};

const confirmarEliminacionSeleccionados = () => {
  if (gruposSeleccionados.value.length > 0) {
    mostrarDialogoConfirmacionEliminar.value = true;
  }
};

const eliminarGruposSeleccionados = async () => {
  try {
    const ids = gruposSeleccionados.value.map((grupo) => grupo.id_grupo);
    await axiosInstance.delete("grupos", { data: { ids } });
    grupos.value = grupos.value.filter((grupo) => !ids.includes(grupo.id_grupo));
    gruposSeleccionados.value = [];
    mostrarDialogoConfirmacionEliminar.value = false;
    mostrarExito('Grupos eliminados correctamente');
  } catch (error) {
    mostrarError('Error al eliminar grupos');
    console.error("Error eliminando grupos:", error);
  }
};

const mostrarExito = (mensaje: string) => {
  toast.add({ severity: 'success', summary: 'Éxito', detail: mensaje, life: 3000 });
};

const mostrarError = (mensaje: string) => {
  toast.add({ severity: 'error', summary: 'Error', detail: mensaje, life: 3000 });
};
const descargarPlantilla = async (idGrupo: number) => {
  try {
    const response = await axiosInstance.get(
      `grupos/${idGrupo}/plantilla-calificaciones`,
      { responseType: 'blob' }
    );
    
    // Crear enlace de descarga
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Plantilla_Calificaciones_${idGrupo}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();

    // Mostrar notificación
    toast.add({
      severity: 'success',
      summary: 'Descarga exitosa',
      detail: 'Plantilla generada correctamente',
      life: 3000
    });
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo generar la plantilla',
      life: 3000
    });
    console.error("Error descargando plantilla:", error);
  }
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