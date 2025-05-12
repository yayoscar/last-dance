<template>
    <Card>
        <template #title>Carreras</template>
        
        <template #content>
            <DataTable :value="carreras" stripedRows >
                <template #header>
                    <div class="flex justify-end">
                        <Button 
                        @click="clickMostrarDialogoCrearCarrera"
                        label="Agregar Carrera" icon="pi pi-plus"/>
                    </div>
                </template>
                <Column field="nombre" header="Nombre de la carrera"></Column>
                <Column field="acciones" header="Acciones"></Column>                
            </DataTable>
        </template>
    </Card>

    <!-- Dialogos -->
    <Dialog v-model:visible="showDialogCrearCarrera" modal header="Agregar una Carrera" :style="{ width: '50rem' }">
        <span class="text-surface-500 dark:text-surface-400 block mb-4">Agrega información de la carrera.</span>
        <label class="font-semibold w-24">Nombre de la Carrera</label>
        <div class="flex items-center gap-4 mt-1 mb-4">
            <InputText 
                v-model="modelCarrera.nombre"
                class="flex-auto" autocomplete="off" />
        </div>
        
        <div class="flex justify-end gap-2">
            <Button type="button" label="Cancelar" severity="secondary" @click="showDialogCrearCarrera = false"></Button>
            <Button type="button" label="Agregar" severity="primary" @click="clickAgregarCarrera"></Button>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import axiosInstance from "~/utils/axiosConfig"
onMounted(async () => {
    try {
        const response = await axiosInstance.get("carreras");
        carreras.value = response.data;
    } catch (error) {
        console.error("Error fetching carreras:", error);
    }
});

const carreras = ref<any[]>([]);

//Dialog Agregar Carrera
const showDialogCrearCarrera = ref(false);

const clickMostrarDialogoCrearCarrera = () => {
    showDialogCrearCarrera.value = true;
};

const modelCarrera=ref(
    {
        nombre: ""
    }
);

const clickAgregarCarrera = async () => {
    try {
        const response = await axiosInstance.post("carreras",modelCarrera.value);
        console.log("Carrera agregada:", response.data);
        carreras.value.push(response.data);
        showDialogCrearCarrera.value = false;
    } catch (error) {
        console.error("Error fetching carreras:", error);
    }
};
</script>

<style scoped lang="css">
</style>