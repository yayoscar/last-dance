<template>
    <div>
        <Card>
            <template #title>Planes de Estudio</template>
            
            <template #content>
                <DataTable :value="planesEstudio" stripedRows>
                    <template #header>
                        <div class="flex justify-end">
                            <Button 
                                @click="clickMostrarDialogoCrearPlan"
                                label="Agregar Plan de Estudio" 
                                icon="pi pi-plus"
                            />
                        </div>
                    </template>
                    <Column field="nombre" header="Nombre del Plan"></Column>
                    <Column field="carrera.nombre" header="Carrera"></Column>
                    <Column field="acciones" header="Acciones">
                        <template #body="slotProps">
                            <div class="flex gap-2">
                                <Button 
                                    icon="pi pi-pencil" 
                                    severity="info" 
                                    size="small" 
                                    @click="clickEditarPlan(slotProps.data)"
                                />
                                <Button 
                                    icon="pi pi-trash" 
                                    severity="danger" 
                                    size="small" 
                                    @click="clickEliminarPlan(slotProps.data)"
                                />
                            </div>
                        </template>
                    </Column>                
                </DataTable>
            </template>
        </Card>

        <!-- Dialog Crear/Editar Plan de Estudio -->
        <Dialog 
            v-model:visible="showDialogCrearPlan" 
            modal 
            :header="modoEdicion ? 'Editar Plan de Estudio' : 'Agregar Plan de Estudio'" 
            :style="{ width: '60rem' }"
        >
            <span class="text-surface-500 dark:text-surface-400 block mb-4">
                {{ modoEdicion ? 'Edita la información del plan de estudio.' : 'Agrega información del plan de estudio.' }}
            </span>
            
            <form @submit.prevent="submitPlan">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Nombre del Plan -->
                    <div class="field">
                        <label class="font-semibold" for="nombre">Nombre del Plan *</label>
                        <div class="flex flex-col gap-2 mt-1">
                            <InputText 
                                id="nombre"
                                v-model="modelPlan.nombre"
                                class="w-full" 
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

                    <!-- Carrera -->
                    <div class="field">
                        <label class="font-semibold" for="carrera">Carrera *</label>
                        <div class="flex flex-col gap-2 mt-1">
                            <Dropdown
                                id="carrera"
                                v-model="modelPlan.id_carrera"
                                :options="carreras"
                                optionLabel="nombre"
                                optionValue="id_carrera"
                                placeholder="Selecciona una carrera"
                                class="w-full"
                                :class="{ 'p-invalid': $v.id_carrera.$error }"
                                @blur="$v.id_carrera.$touch"
                            />
                            <small 
                                v-if="$v.id_carrera.$error" 
                                class="p-error"
                            >
                                {{ $v.id_carrera.$errors[0].$message }}
                            </small>
                        </div>
                    </div>
                </div>
                
                <div class="flex justify-end gap-2 mt-6">
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
                <span>
                    ¿Estás seguro de que quieres eliminar el plan de estudio 
                    <strong>{{ planAEliminar?.nombre }}</strong> 
                    de la carrera <strong>{{ planAEliminar?.carrera?.nombre }}</strong>?
                </span>
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
                    @click="confirmarEliminarPlan"
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
import type { Carrera } from '~/features/carreras/models/carrera-model'
import type { PlanEstudio, PlanEstudioCreate, PlanEstudioUpdate } from '~/features/plan_estudios/models/plan-estudio-mode'
import axiosInstance from "~/utils/axiosConfig"

// Composables
const toast = useToast()

// Estados reactivos
const planesEstudio = ref<PlanEstudio[]>([])
const carreras = ref<Carrera[]>([])
const loading = ref(false)

// Dialog states
const showDialogCrearPlan = ref(false)
const showDialogEliminar = ref(false)
const modoEdicion = ref(false)
const planAEliminar = ref<PlanEstudio | null>(null)

// Modelo del formulario
const modelPlan = ref<PlanEstudioCreate | (PlanEstudioUpdate & { id_plan_estudio?: number })>({
    nombre: "",
    id_carrera: null as any
})

// Reglas de validación
const rules = {
    nombre: {
        required: required,
        minLength: minLength(3)
    },
    id_carrera: {
        required: required
    }
}

// Vuelidate
const $v = useVuelidate(rules, modelPlan)

// Métodos
const cargarPlanesEstudio = async () => {
    try {
        loading.value = true
        const response = await axiosInstance.get<PlanEstudio[]>("planes_estudio")
        planesEstudio.value = response.data
    } catch (error) {
        console.error("Error al obtener planes de estudio:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Error al cargar los planes de estudio',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const cargarCarreras = async () => {
    try {
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
    }
}

const clickMostrarDialogoCrearPlan = () => {
    modoEdicion.value = false
    modelPlan.value = { 
        nombre: "", 
        id_carrera: null as any 
    }
    $v.value.$reset()
    showDialogCrearPlan.value = true
}

const clickEditarPlan = (plan: PlanEstudio) => {
    modoEdicion.value = true
    modelPlan.value = { 
        ...plan,
        id_plan_estudio: plan.id_plan_estudio
    }
    $v.value.$reset()
    showDialogCrearPlan.value = true
}

const clickEliminarPlan = (plan: PlanEstudio) => {
    planAEliminar.value = plan
    showDialogEliminar.value = true
}

const submitPlan = async () => {
    // Validar formulario
    const isValid = await $v.value.$validate()
    if (!isValid) {
        return
    }

    try {
        loading.value = true
        
        if (modoEdicion.value) {
            // Editar plan existente
            const planUpdate = modelPlan.value as PlanEstudioUpdate & { id_plan_estudio: number }
            const response = await axiosInstance.patch<PlanEstudio>(
                `planes_estudio/${planUpdate.id_plan_estudio}`, 
                {
                    nombre: planUpdate.nombre,
                    id_carrera: planUpdate.id_carrera
                }
            )
            
            // Actualizar el plan en la lista
            const index = planesEstudio.value.findIndex(p => p.id_plan_estudio === planUpdate.id_plan_estudio)
            if (index !== -1) {
                planesEstudio.value[index] = response.data
            }
            
            toast.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Plan de estudio actualizado exitosamente',
                life: 3000
            })
        } else {
            // Crear nuevo plan
            const planCreate = modelPlan.value as PlanEstudioCreate
            const response = await axiosInstance.post<PlanEstudio>("planes_estudio", planCreate)
            
            // Agregar el nuevo plan a la lista
            planesEstudio.value.push(response.data)
            
            toast.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Plan de estudio agregado exitosamente',
                life: 3000
            })
        }
        
        showDialogCrearPlan.value = false
        
    } catch (error: any) {
        console.error("Error al guardar plan de estudio:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.detail || 'Error al guardar el plan de estudio',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const confirmarEliminarPlan = async () => {
    if (!planAEliminar.value) return

    try {
        loading.value = true
        
        await axiosInstance.delete(`planes_estudio/${planAEliminar.value.id_plan_estudio}`)
        
        // Remover el plan de la lista
        planesEstudio.value = planesEstudio.value.filter(
            p => p.id_plan_estudio !== planAEliminar.value?.id_plan_estudio
        )
        
        toast.add({
            severity: 'success',
            summary: 'Éxito',
            detail: 'Plan de estudio eliminado exitosamente',
            life: 3000
        })
        
        showDialogEliminar.value = false
        planAEliminar.value = null
        
    } catch (error: any) {
        console.error("Error al eliminar plan de estudio:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.detail || 'Error al eliminar el plan de estudio',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const cancelarDialog = () => {
    showDialogCrearPlan.value = false
    $v.value.$reset()
    modelPlan.value = { 
        nombre: "", 
        id_carrera: null as any 
    }
}

// Lifecycle
onMounted(async () => {
    await Promise.all([
        cargarPlanesEstudio(),
        cargarCarreras()
    ])
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