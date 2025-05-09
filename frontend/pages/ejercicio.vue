<template>
    <h1>
        {{ texto }}
    </h1>
    <Button 
        icon="pi pi-home"
        severity="info" 
        @click="aumentaTexto()"
        label="Presionar" />

    <ul>
        <li>1</li>
        <li>2</li>
        <li>3</li>
    </ul>
</template>

<script setup lang="ts">
const texto=ref<number>(4)

const aumentaTexto=()=>{
    texto.value++
}
texto.value=5
</script>

<style scoped lang="css">
</style>
