<template>
    <h1>Hola {{ nombre }}</h1>
    <h3>Contador: {{ contador }}</h3>
    <Button 
        @click="contador++" 
        icon="pi pi-plus" 
        aria-label="Save" 
    />
    <Button 
        @click="contador--" 
        icon="pi pi-minus" 
        aria-label="Save" 
    />
    
</template>

<script setup lang="ts">
const nombre = ref<string>('Pepito')
const contador = ref<number>(0)

</script>