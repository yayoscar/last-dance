<template>
    <Card>
        <template #title>Alumnos</template>
        
        <template #content>
            <DataTable :value="alumnos" stripedRows>
                <template #header>
                    <div class="flex justify-end">
                        <Button 
                            @click="clickMostrarDialogoCrearAlumno" 
                            label="Agregar Alumno" 
                            icon="pi pi-plus"
                        />
                    </div>
                </template>
                <Column field="nombre" header="Nombre del alumno"></Column>
                <Column field="ape_paterno" header="Apellido Paterno"></Column>
                <Column field="ape_materno" header="Apellido Materno"></Column>
                <Column field="carrera.nombre" header="Carrera"></Column>    
                <Column field="turno" header="Turno"></Column>           
                <Column field="num_control" header="Número de control"></Column>    
                <Column field="generacion" header="Generación"></Column> 
                <Column field="curp" header="CURP"></Column> 
                <Column field="plan_estudio.nombre" header="Plan de Estudios"></Column>
                <Column header="Acciones">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" class="p-button-rounded p-button-text" />
                        <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger" />
                    </template>
                </Column>
            </DataTable>
        </template>
    </Card>

    <!-- Diálogo para agregar alumno -->
    <Dialog 
        v-model:visible="showDialogCrearAlumno" 
        modal 
        header="Agregar un Alumno" 
        :style="{ width: '50rem' }"
    >
        <div class="grid gap-4">
            <div class="col-12">
                <label class="font-semibold block mb-2">Nombre del Alumno</label>
                <InputText 
                    v-model="modelAlumno.nombre"
                    class="w-full" 
                    autocomplete="off" 
                />
            </div>

            <div class="col-12">
                <label class="font-semibold block mb-2">Apellido Paterno</label>
                <InputText 
                    v-model="modelAlumno.ape_paterno"
                    class="w-full" 
                />
            </div>

            <div class="col-12">
                <label class="font-semibold block mb-2">Apellido Materno</label>
                <InputText 
                    v-model="modelAlumno.ape_materno"
                    class="w-full" 
                />
            </div>

            <div class="col-12">
                <label class="font-semibold block mb-2">Plan de Estudios</label>
                <Dropdown 
                    v-model="modelAlumno.id_plan_estudio"
                    :options="planesEstudio" 
                    optionLabel="nombre"
                    optionValue="id_plan_estudio"
                    placeholder="Selecciona un plan"
                    class="w-full"
                    :showClear="true"
                />
            </div>

            <div class="col-12">
                <label class="font-semibold block mb-2">Turno</label>
                <Dropdown 
                    v-model="modelAlumno.turno"
                    :options="opcionesTurno" 
                    placeholder="Selecciona un turno"
                    class="w-full"
                    :showClear="true"
                />
            </div>

            <div class="col-12">
                <label class="font-semibold block mb-2">Número de Control</label>
                <InputText 
                    v-model="modelAlumno.num_control"
                    class="w-full" 
                />
            </div>

            <div class="col-12">
                <label class="font-semibold block mb-2">Generación</label>
                <InputNumber 
                    v-model="modelAlumno.generacion"
                    class="w-full"
                    :min="1978"
                    :max="2100"
                    :maxlength="4"
                    :useGrouping="false"
                    @keypress="soloNumeros"
                />
                <small v-if="!generacionValida" class="p-error">La generación debe ser un año entre 1978 y 2100</small>
            </div>
        </div>

        <template #footer>
            <div class="flex justify-end gap-2">
                <Button 
                    type="button" 
                    label="Cancelar" 
                    severity="secondary" 
                    @click="showDialogCrearAlumno = false"
                />
                <Button 
                    type="button" 
                    label="Agregar" 
                    severity="primary" 
                    @click="clickAgregarAlumno"
                    :disabled="!formValido"
                />
            </div>
        </template>
    </Dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axiosInstance from "~/utils/axiosConfig";
import Dropdown from 'primevue/dropdown';
import InputNumber from 'primevue/inputnumber';

// Datos
const alumnos = ref<any[]>([]);
const planesEstudio = ref<any[]>([]);
const opcionesTurno = ref(['MATUTINO', 'VESPERTINO']);

// Diálogo
const showDialogCrearAlumno = ref(false);

// Modelo del alumno
const modelAlumno = ref({
    nombre: "",
    ape_paterno: "",
    ape_materno: "",
    id_plan_estudio: null,
    turno: null,
    num_control: "",
    generacion: null
});

// Validación de generación
const generacionValida = computed(() => {
    if (modelAlumno.value.generacion === null) return true;
    return modelAlumno.value.generacion >= 1978 && modelAlumno.value.generacion <= 2100;
});

// Validación del formulario
const formValido = computed(() => {
    return (
        modelAlumno.value.nombre.trim() !== "" &&
        modelAlumno.value.ape_paterno.trim() !== "" &&
        modelAlumno.value.id_plan_estudio !== null &&
        modelAlumno.value.turno !== null &&
        generacionValida.value
    );
});

// Función para solo permitir números
const soloNumeros = (e: KeyboardEvent) => {
    const charCode = e.which ? e.which : e.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        e.preventDefault();
    }
};

// Cargar datos iniciales
onMounted(async () => {
    try {
        const [alumnosResponse, planesResponse] = await Promise.all([
            axiosInstance.get("alumnos"),
            axiosInstance.get("planes-estudio")
        ]);
        
        alumnos.value = alumnosResponse.data;
        planesEstudio.value = planesResponse.data;
    } catch (error) {
        console.error("Error cargando datos:", error);
    }
});

// Mostrar diálogo
const clickMostrarDialogoCrearAlumno = () => {
    showDialogCrearAlumno.value = true;
};

// Agregar alumno
const clickAgregarAlumno = async () => {
    try {
        const response = await axiosInstance.post("alumnos", modelAlumno.value);
        alumnos.value.push(response.data);
        
        // Resetear formulario
        modelAlumno.value = {
            nombre: "",
            ape_paterno: "",
            ape_materno: "",
            id_plan_estudio: null,
            turno: null,
            num_control: "",
            generacion: null
        };
        
        showDialogCrearAlumno.value = false;
    } catch (error) {
        console.error("Error agregando alumno:", error);
    }
};
</script>

<style scoped>
/* Estilos personalizados si los necesitas */
</style>