<template>
    <div>
        <Card>
            <template #title>Periodos</template>
            
            <template #content>
                <DataTable :value="periodos" stripedRows>
                    <template #header>
                        <div class="flex justify-end">
                            <Button 
                                @click="clickMostrarDialogoCrearPeriodo"
                                label="Agregar Periodo" 
                                icon="pi pi-plus"
                            />
                        </div>
                    </template>
                    <Column field="nombre" header="Nombre del periodo"></Column>
                    <Column field="acciones" header="Acciones">
                        <template #body="slotProps">
                            <div class="flex gap-2">
                                <Button 
                                    icon="pi pi-pencil" 
                                    severity="info" 
                                    size="small" 
                                    @click="clickEditarPeriodo(slotProps.data)"
                                />
                                <Button 
                                    icon="pi pi-trash" 
                                    severity="danger" 
                                    size="small" 
                                    @click="clickEliminarPeriodo(slotProps.data)"
                                />
                            </div>
                        </template>
                    </Column>                
                </DataTable>
            </template>
        </Card>

        <!-- Dialog Crear/Editar Periodo -->
        <Dialog 
            v-model:visible="showDialogCrearPeriodo" 
            modal 
            :header="modoEdicion ? 'Editar Periodo' : 'Agregar un Periodo'" 
            :style="{ width: '50rem' }"
        >
            <span class="text-surface-500 dark:text-surface-400 block mb-4">
                {{ modoEdicion ? 'Edita la información del periodo.' : 'Agrega información del periodo.' }}
            </span>
            
            <form @submit.prevent="submitPeriodo">
                <div class="field">
                    <label class="font-semibold w-24" for="nombre">Nombre del Periodo *</label>
                    <div class="flex flex-col gap-2 mt-1 mb-4">
                        <InputText 
                            id="nombre"
                            v-model="modelPeriodo.nombre"
                            class="flex-auto" 
                            autocomplete="off"
                            :class="{ 'p-invalid': $v.nombre.$error }"
                            @blur="$v.nombre.$touch"
                        />
                        <small 
                            v-if="$v.nombre.$error" 
                            class="p-error"
                        >
                            {{ $v.nombre.$errors[0].$message }}
                        </small>
                    </div>
                </div>
                
                <div class="flex justify-end gap-2">
                    <Button 
                        type="button" 
                        label="Cancelar" 
                        severity="secondary" 
                        @click="cancelarDialog"
                    />
                    <Button 
                        type="submit" 
                        :label="modoEdicion ? 'Actualizar' : 'Agregar'" 
                        severity="primary"
                        :loading="loading"
                    />
                </div>
            </form>
        </Dialog>

        <!-- Dialog Confirmar Eliminación -->
        <Dialog 
            v-model:visible="showDialogEliminar" 
            modal 
            header="Confirmar Eliminación" 
            :style="{ width: '30rem' }"
        >
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle text-orange-500" style="font-size: 2rem"></i>
                <span>¿Estás seguro de que quieres eliminar el periodo <strong>{{ periodoAEliminar?.nombre }}</strong>?</span>
            </div>
            
            <div class="flex justify-end gap-2 mt-4">
                <Button 
                    type="button" 
                    label="Cancelar" 
                    severity="secondary" 
                    @click="showDialogEliminar = false"
                />
                <Button 
                    type="button" 
                    label="Eliminar" 
                    severity="danger"
                    :loading="loading"
                    @click="confirmarEliminarPeriodo"
                />
            </div>
        </Dialog>

        <!-- Toast para notificaciones -->
        <Toast />
    </div>
</template>

<script setup lang="ts">
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'
import { useToast } from 'primevue/usetoast'
import type { Periodo, PeriodoCreate,PeriodoUpdate } from '~/features/periodos/models/periodo-model'
import axiosInstance from "~/utils/axiosConfig"

// Composables
const toast = useToast()

// Estados reactivos
const periodos = ref<Periodo[]>([])
const loading = ref(false)

// Dialog states
const showDialogCrearPeriodo = ref(false)
const showDialogEliminar = ref(false)
const modoEdicion = ref(false)
const periodoAEliminar = ref<Periodo | null>(null)

// Modelo del formulario
const modelPeriodo = ref<PeriodoCreate | PeriodoUpdate>({
    nombre: ""
})

// Reglas de validación
const rules = {
    nombre: {
        required: required,
        minLength: minLength(3)
    }
}

// Vuelidate
const $v = useVuelidate(rules, modelPeriodo)

// Métodos
const cargarPeriodos = async () => {
    try {
        loading.value = true
        const response = await axiosInstance.get<Periodos[]>("periodos")
        periodos.value = response.data
    } catch (error) {
        console.error("Error al obtener periodos:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Error al cargar los periodos',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const clickMostrarDialogoCrearPeriodo = () => {
    modoEdicion.value = false
    modelPeriodo.value = { nombre: "" }
    $v.value.$reset()
    showDialogCrearPeriodo.value = true
}

const clickEditarPeriodo = (periodo: Periodo) => {
    modoEdicion.value = true
    modelPeriodo.value = { ...periodo }
    $v.value.$reset()
    showDialogCrearPeriodo.value = true
}

const clickEliminarPeriodo = (periodo: Periodo) => {
    periodoAEliminar.value = periodo
    showDialogEliminar.value = true
}

const submitPeriodo = async () => {
    // Validar formulario
    const isValid = await $v.value.$validate()
    if (!isValid) {
        return
    }

    try {
        loading.value = true
        
        if (modoEdicion.value) {
            // Editar periodo existente
            const periodoUpdate = modelPeriodo.value as PeriodoUpdate
            const response = await axiosInstance.patch<Periodo>(
                `periodos/${periodoUpdate.id_periodo}`, 
                periodoUpdate
            )
            
            // Actualizar el periodo en la lista
            const index = periodos.value.findIndex(c => c.id_periodo === periodoUpdate.id_periodo)
            if (index !== -1) {
                periodos.value[index] = response.data
            }
            
            toast.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Periodo actualizado exitosamente',
                life: 3000
            })
        } else {
            // Crear nuevo periodo
            const periodoCreate = modelPeriodo.value as PeriodoCreate
            const response = await axiosInstance.post<Periodo>("periodos", periodoCreate)
            
            // Agregar el nuevo periodo a la lista
            periodos.value.push(response.data)
            
            toast.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Periodo agregada exitosamente',
                life: 3000
            })
        }
        
        showDialogCrearPeriodo.value = false
        
    } catch (error: any) {
        console.error("Error al guardar periodo:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.detail || 'Error al guardar el periodo',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const confirmarEliminarPeriodo = async () => {
    if (!periodoAEliminar.value) return

    try {
        loading.value = true
        
        await axiosInstance.delete(`periodos/${periodoAEliminar.value.id_periodo}`)
        
        // Remover el periodo de la lista
        periodos.value = periodos.value.filter(
            c => c.id_periodo !== periodoAEliminar.value?.id_periodo
        )
        
        toast.add({
            severity: 'success',
            summary: 'Éxito',
            detail: 'Periodo eliminado exitosamente',
            life: 3000
        })
        
        showDialogEliminar.value = false
        periodoAEliminar.value = null
        
    } catch (error: any) {
        console.error("Error al eliminar periodo:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.detail || 'Error al eliminar el periodo',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const cancelarDialog = () => {
    showDialogCrearPeriodo.value = false
    $v.value.$reset()
    modelPeriodo.value = { nombre: "" }
}

// Lifecycle
onMounted(() => {
    cargarPeriodos()
})
</script>

<style scoped>
.field {
    margin-bottom: 1rem;
}

.p-invalid {
    border-color: #e24c4c;
}

.p-error {
    color: #e24c4c;
    font-size: 0.875rem;
}
</style>