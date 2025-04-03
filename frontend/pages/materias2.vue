<template>
    <DataTable :value="materias" tableStyle="min-width: 50rem">
        <Column field="code" header="Nombre"></Column>
        <Column field="name" header="Creditos"></Column>
        <Column field="category" header="Tipo"></Column>
    </DataTable>
</template>
<script setup lang="ts">
import { Materia } from '~/features/materias/models/materia-model';

    const materias=ref<Materia[]>([]);
    onMounted(async() => {
        const response = await fetch('http://localhost:3200/api/v1/materias');
        const data = await response.json();
        materias.value = data;
    });

</script>