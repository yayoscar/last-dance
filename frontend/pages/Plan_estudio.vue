<template>
    <Card>
        <template #title>Plan Estudio</template>
        
        <template #content>
            <DataTable :value="plan_estudio" stripedRows >
                <template #header>
                    <div class="flex justify-end">
                        <Button 
                        @click="clickMostrarDialogoCrearPlan_estudio"
                        label="Agregar Plan Estudio" icon="pi pi-plus"/>
                    </div>
                </template>
                <Column field="nombre" header="Nombre del Plan de Estudio"></Column>
                <Column field="acciones" header="Acciones"></Column>                
            </DataTable>
        </template>
    </Card>

    <!-- Dialogos -->
    <Dialog v-model:visible="showDialogCrearPlan_estudio" modal header="Agregar un plan estudio" :style="{ width: '50rem' }">
        <span class="text-surface-500 dark:text-surface-400 block mb-4">Agrega información del plan de estudio.</span>
        <label class="font-semibold w-24">Nombre del plan de estudio</label>
        <div class="flex items-center gap-4 mt-1 mb-4">
            <InputText 
                v-model="modelPlan_estudio.nombre"
                class="flex-auto" autocomplete="off" />
        </div>

        
        
        <div class="flex justify-end gap-2">
            <Button type="button" label="Cancelar" severity="secondary" @click="showDialogCrearPlan_estudio = false"></Button>
            <Button type="button" label="Agregar" severity="primary" @click="clickAgregarPlan_estudio"></Button>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import axiosInstance from "~/utils/axiosConfig"
onMounted(async () => {
    try {
        const response = await axiosInstance.get("planes_estudio");
        plan_estudio.value = response.data;
    } catch (error) {
        console.error("Error fetching plan estudio:", error);
    }
});

const plan_estudio = ref<any[]>([]);

//Dialog Agregar Plan de estudio
const showDialogCrearPlan_estudio = ref(false);

const clickMostrarDialogoCrearPlan_estudio = () => {
    showDialogCrearPlan_estudio.value = true;
};

const modelPlan_estudio=ref(
    {
        nombre: ""
    }
);

const clickAgregarPlan_estudio = async () => {
    try {
        const response = await axiosInstance.post("planes_estudio",modelPlan_estudio.value);
        console.log("Plan de estudio agregada:", response.data);
        plan_estudio.value.push(response.data);
        showDialogCrearPlan_estudio.value = false;
    } catch (error) {
        console.error("Error fetching plan de estudio:", error);
    }
};
</script>

<style scoped lang="css">
</style>