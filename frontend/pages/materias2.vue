<template>
    <DataTable :value="materias" tableStyle="min-width: 50rem">
        <Column field="nombre" header="Nombre"></Column>
        <Column field="creditos" header="Creditos"></Column>
        <Column field="tipo" header="Tipo"></Column>
    </DataTable>
</template>
<script setup lang="ts">
import type { MateriaModel } from '~/features/materias/models/materia-model';


    const materias=ref<MateriaModel[]>([]);
    onMounted(async() => {
        const response = await fetch('http://localhost:3200/api/v1/materias');
        const data = await response.json();
        materias.value = data;
        console.log(data);
    });

</script>