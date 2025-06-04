<template>
    <div>
        <Card>
            <template #title>Grupos</template>
            
            <template #content>
                <DataTable :value="grupos" stripedRows>
                    <template #header>
                        <div class="flex justify-end">
                            <Button 
                                @click="clickMostrarDialogoCrearGrupo"
                                label="Agregar Grupo" 
                                icon="pi pi-plus"
                            />
                        </div>
                    </template>
                    <Column field="nombre" header="Nombre del Grupo"></Column>
                    <Column field="Periodo.nombre" header="Periodo"></Column>
                    <Column field="acciones" header="Acciones">
                        <template #body="slotProps">
                            <div class="flex gap-2">
                                <Button 
                                    icon="pi pi-pencil" 
                                    severity="info" 
                                    size="small" 
                                    @click="clickEditarGrupo(slotProps.data)"
                                />
                                <Button 
                                    icon="pi pi-trash" 
                                    severity="danger" 
                                    size="small" 
                                    @click="clickEliminarGrupo(slotProps.data)"
                                />
                            </div>
                        </template>
                    </Column>                
                </DataTable>
            </template>
        </Card>

        <!-- Dialog Crear/Editar Grupo -->
        <Dialog 
            v-model:visible="showDialogCrearGrupo" 
            modal 
            :header="modoEdicion ? 'Editar Grupo' : 'Agregar Grupo'" 
            :style="{ width: '60rem' }"
        >
            <span class="text-surface-500 dark:text-surface-400 block mb-4">
                {{ modoEdicion ? 'Edita la información del grupo.' : 'Agrega información del grupo.' }}
            </span>
            
            <form @submit.prevent="submitGrupo">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Nombre del Grupo -->
                    <div class="field">
                        <label class="font-semibold" for="nombre">Nombre del Grupo *</label>
                        <div class="flex flex-col gap-2 mt-1">
                            <InputText 
                                id="nombre"
                                v-model="modelGrupo.nombre"
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

                    <!-- Periodos -->
                    <div class="field">
                        <label class="font-semibold" for="periodo">Periodo *</label>
                        <div class="flex flex-col gap-2 mt-1">
                            <Dropdown
                                id="periodo"
                                v-model="modelGrupo.id_periodo"
                                :options="periodos"
                                optionLabel="nombre"
                                optionValue="id_periodo"
                                placeholder="Selecciona un periodo"
                                class="w-full"
                                :class="{ 'p-invalid': $v.id_periodo.$error }"
                                @blur="$v.id_periodo.$touch"
                            />
                            <small 
                                v-if="$v.id_periodo.$error" 
                                class="p-error"
                            >
                                {{ $v.id_periodo.$errors[0].$message }}
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
                    ¿Estás seguro de que quieres eliminar el Grupo
                    <strong>{{ grupoAEliminar?.nombre }}</strong> 
                     <strong>{{ grupoAEliminar?.grupo?.nombre }}</strong>?
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
                    @click="confirmarEliminarGrupo"
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
import type { Carrera } from '~/features/grupos/models/grupo-mode'
import type { Grupo, GrupoCreate, GrupoUpdate } from '~/features/grupos/models/grupo-mode'
import axiosInstance from "~/utils/axiosConfig"

// Composables
const toast = useToast()

// Estados reactivos
const grupo = ref<Grupo[]>([])
const periodo = ref<Periodo[]>([])
const loading = ref(false)

// Dialog states
const showDialogCrearGrupo = ref(false)
const showDialogEliminar = ref(false)
const modoEdicion = ref(false)
const grupoAEliminar = ref<Grupo | null>(null)

// Modelo del formulario
const modelGrupo = ref<GrupoCreate | (GrupoUpdate & { id_grupo?: number })>({
    nombre: "",
    id_periodo: null as any
})

// Reglas de validación
const rules = {
    nombre: {
        required: required,
        minLength: minLength(3)
    },
    id_periodo: {
        required: required
    }
}

// Vuelidate
const $v = useVuelidate(rules, modelGrupo)

// Métodos
const cargarGrupo = async () => {
    try {
        loading.value = true
        const response = await axiosInstance.get<Grupo[]>("grupo")
        grupo.value = response.data
    } catch (error) {
        console.error("Error al obtener grupos:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Error al cargar los grupos',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const cargarPeriodos = async () => {
    try {
        const response = await axiosInstance.get<Periodo[]>("periodos")
        periodos.value = response.data
    } catch (error) {
        console.error("Error al obtener periodos:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Error al cargar los periodos',
            life: 3000
        })
    }
}

const clickMostrarDialogoCrearGrupo = () => {
    modoEdicion.value = false
    modelGrupo.value = { 
        nombre: "", 
        id_periodo: null as any 
    }
    $v.value.$reset()
    showDialogCrearGrupo.value = true
}

const clickEditarGrupo = (grupo: Grupo) => {
    modoEdicion.value = true
    modelGrupo.value = { 
        ...grupo,
        id_grupo: grupo.id_grupo
    }
    $v.value.$reset()
    showDialogCrearGrupo.value = true
}

const clickEliminarGrupo = (grupo: Grupo) => {
    grupoAEliminar.value = grupo
    showDialogEliminar.value = true
}

const submitGrupo = async () => {
    // Validar formulario
    const isValid = await $v.value.$validate()
    if (!isValid) {
        return
    }

    try {
        loading.value = true
        
        if (modoEdicion.value) {
            // Editar grupo existente
            const grupoUpdate = modelGrupo.value as GrupoUpdate & { id_grupo: number }
            const response = await axiosInstance.patch<Grupo>(
                `grupo/${grupoUpdate.id_grupo}`, 
                {
                    nombre: grupoUpdate.nombre,
                    id_periodo: grupoUpdate.id_periodo
                }
            )
            
            // Actualizar el grupo en la lista
            const index = grupos.value.findIndex(p => p.id_grupo === grupoUpdate.id_grupo)
            if (index !== -1) {
                grupos.value[index] = response.data
            }
            
            toast.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Grupo actualizado exitosamente',
                life: 3000
            })
        } else {
            // Crear nuevo grupo
            const grupoCreate = modelGrupovalue as GrupoCreate
            const response = await axiosInstance.post<Grupo>("grupos", grupoCreate)
            
            // Agregar el nuevo grupo a la lista
            grupos.value.push(response.data)
            
            toast.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Grupo agregado exitosamente',
                life: 3000
            })
        }
        
        showDialogCrearGrupo.value = false
        
    } catch (error: any) {
        console.error("Error al guardar el grupo:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.detail || 'Error al guardar el grupo',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const confirmarEliminarGrupo = async () => {
    if (!grupoAEliminar.value) return

    try {
        loading.value = true
        
        await axiosInstance.delete(`grupos/${grupoAEliminar.value.id_grupo}`)
        
        // Remover el grupo de la lista
        grupo.value = grupos.value.filter(
            p => p.id_grupo !== GrupoAEliminar.value?.id_grupo
        )
        
        toast.add({
            severity: 'success',
            summary: 'Éxito',
            detail: 'Grupo eliminado exitosamente',
            life: 3000
        })
        
        showDialogEliminar.value = false
        grupoAEliminar.value = null
        
    } catch (error: any) {
        console.error("Error al eliminar el grupo:", error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.detail || 'Error al eliminar el grupo',
            life: 3000
        })
    } finally {
        loading.value = false
    }
}

const cancelarDialog = () => {
    showDialogCrearGrupo.value = false
    $v.value.$reset()
    modelGrupo.value = { 
        nombre: "", 
        id_periodo: null as any 
    }
}

// Lifecycle
onMounted(async () => {
    await Promise.all([
        cargarGrupos(),
        cargarPeriodos()
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