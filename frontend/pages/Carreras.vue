<template>
    <div>
        <Card>
            <template #title>Carreras</template>
            
            <template #content>
                <DataTable :value="carreras" stripedRows>
                    <template #header>
                        <div class="flex justify-end">
                            <Button
                                @click="clickMostrarDialogoCrearCarrera"
                                label="Agregar Carrera" 
                                icon="pi pi-plus"
                            />
                        </div>
                    </template>
                    <Column field="nombre" header="Nombre de la carrera"></Column>
                    <Column field="acciones" header="Acciones">
                        <template #body="slotProps">
                            <div class="flex gap-2">
                                <Button 
                                    icon="pi pi-pencil" 
                                    severity="info" 
                                    size="small" 
                                    @click="clickEditarCarrera(slotProps.data)"
                                />
                                <Button 
                                    icon="pi pi-trash" 
                                    severity="danger" 
                                    size="small" 
                                    @click="clickEliminarCarrera(slotProps.data)"
                                />
                            </div>
                        </template>
                    </Column>                
                </DataTable>
            </template>
        </Card>

        <!-- Dialog Crear/Editar Carrera -->
        <Dialog 
            v-model:visible="showDialogCrearCarrera" 
            modal 
            :header="modoEdicion ? 'Editar Carrera' : 'Agregar una Carrera'" 
            :style="{ width: '50rem' }"
        >
            <span class="text-surface-500 dark:text-surface-400 block mb-4">
                {{ modoEdicion ? 'Edita la información de la carrera.' : 'Agrega información de la carrera.' }}
            </span>
            
            <form @submit.prevent="submitCarrera">
                <div class="field">
                    <label class="font-semibold w-24" for="nombre">Nombre de la Carrera *</label>
                    <div class="flex flex-col gap-2 mt-1 mb-4">
                        <InputText 
                            id="nombre"
                            v-model="modelCarrera.nombre"
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
                <span>¿Estás seguro de que quieres eliminar la carrera <strong>{{ carreraAEliminar?.nombre }}</strong>?</span>
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
                    @click="confirmarEliminarCarrera"
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
import type { Carrera, CarreraCreate,CarreraUpdate } from '~/features/carreras/models/carrera-model'
import axiosInstance from "~/utils/axiosConfig"

// Composables
const toast = useToast()

// Estados reactivos
const carreras = ref<Carrera[]>([])
const loading = ref(false)

// Dialog states
const showDialogCrearCarrera = ref(false)
const showDialogEliminar = ref(false)
const modoEdicion = ref(false)
const carreraAEliminar = ref<Carrera | null>(null)

// Modelo del formulario
const modelCarrera = ref<CarreraCreate | CarreraUpdate>({
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
const $v = useVuelidate(rules, modelCarrera)

// Métodos
const cargarCarreras = async () => {
    try {
        loading.value = true
        const response = await axiosInstance.get<Carrera[]>("carreras")
        carreras.value = response.data
    } catch (error) {
        console.error("Error al obtener carreras:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Error al cargar las carreras',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const clickMostrarDialogoCrearCarrera = () => {
    modoEdicion.value = false
    modelCarrera.value = { nombre: "" }
    $v.value.$reset()
    showDialogCrearCarrera.value = true
}

const clickEditarCarrera = (carrera: Carrera) => {
    modoEdicion.value = true
    modelCarrera.value = { ...carrera }
    $v.value.$reset()
    showDialogCrearCarrera.value = true
}

const clickEliminarCarrera = (carrera: Carrera) => {
    carreraAEliminar.value = carrera
    showDialogEliminar.value = true
}

const submitCarrera = async () => {
    // Validar formulario
    const isValid = await $v.value.$validate()
    if (!isValid) {
        return
    }

    try {
        loading.value = true
        
        if (modoEdicion.value) {
            // Editar carrera existente
            const carreraUpdate = modelCarrera.value as CarreraUpdate
            const response = await axiosInstance.patch<Carrera>(
                `carreras/${carreraUpdate.id_carrera}`, 
                carreraUpdate
            )
            
            // Actualizar la carrera en la lista
            const index = carreras.value.findIndex(c => c.id_carrera === carreraUpdate.id_carrera)
            if (index !== -1) {
                carreras.value[index] = response.data
            }
            
            toast.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Carrera actualizada exitosamente',
                life: 3000
            })
        } else {
            // Crear nueva carrera
            const carreraCreate = modelCarrera.value as CarreraCreate
            const response = await axiosInstance.post<Carrera>("carreras", carreraCreate)
            
            // Agregar la nueva carrera a la lista
            carreras.value.push(response.data)
            
            toast.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Carrera agregada exitosamente',
                life: 3000
            })
        }
        
        showDialogCrearCarrera.value = false
        
    } catch (error: any) {
        console.error("Error al guardar carrera:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.detail || 'Error al guardar la carrera',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const confirmarEliminarCarrera = async () => {
    if (!carreraAEliminar.value) return

    try {
        loading.value = true
        
        await axiosInstance.delete(`carreras/${carreraAEliminar.value.id_carrera}`)
        
        // Remover la carrera de la lista
        carreras.value = carreras.value.filter(
            c => c.id_carrera !== carreraAEliminar.value?.id_carrera
        )
        
        toast.add({
            severity: 'success',
            summary: 'Éxito',
            detail: 'Carrera eliminada exitosamente',
            life: 3000
        })
        
        showDialogEliminar.value = false
        carreraAEliminar.value = null
        
    } catch (error: any) {
        console.error("Error al eliminar carrera:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.detail || 'Error al eliminar la carrera',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const cancelarDialog = () => {
    showDialogCrearCarrera.value = false
    $v.value.$reset()
    modelCarrera.value = { nombre: "" }
}

// Lifecycle
onMounted(() => {
    cargarCarreras()
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