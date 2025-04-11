<template>
  <div>
    <div class="card">
      <Toolbar class="mb-6">
        <template #start>
          <Button label="Nuevo" icon="pi pi-plus" class="mr-2" @click="openNew" />
          <Button label="Eliminar" icon="pi pi-trash" severity="danger" outlined @click="confirmDeleteSelected" :disabled="!selectedProducts || !selectedProducts.length" />
        </template>
      </Toolbar>

      <DataTable
        ref="dt"
        v-model:selection="selectedProducts"
        :value="products"
        dataKey="id"
        :paginator="true"
        :rows="5"
        :filters="filters"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
      >
        <template #header>
          <div class="flex justify-end">
            <IconField>
              <InputIcon><i class="pi pi-search" /></InputIcon>
              <InputText v-model="filters['global'].value" placeholder="Buscar..." />
            </IconField>
          </div>
        </template>

        <Column selectionMode="multiple" style="width: 3rem" :exportable="false" />
        <Column field="codigo" header="Código" sortable style="min-width: 12rem" />
        <Column field="nombre" header="Nombre" sortable style="min-width: 16rem" />
        <Column field="creditos" header="Créditos" sortable style="min-width: 8rem" />
        <Column field="tipo.name" header="Tipo" sortable style="min-width: 12rem" />
        <Column header="Acciones" style="min-width: 8rem">
          <template #body="slotProps">
            <Button icon="pi pi-pencil" rounded text @click="editProduct(slotProps.data)" />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Diálogo de nuevo/editar producto -->
    <Dialog v-model:visible="productDialog" :style="{ width: '450px' }" :header="dialogTitle" :modal="true" class="p-fluid">
  <div class="p-4 space-y-4">
    <!-- Nombre -->
    <div>
      <label for="nombre" class="block font-semibold mb-1">Nombre</label>
      <InputText id="nombre" v-model.trim="product.nombre" required autofocus class="w-full" />
    </div>

    <!-- Créditos -->
    <div>
      <label for="creditos" class="block font-semibold mb-1">Créditos</label>
      <InputNumber id="creditos" v-model="product.creditos" inputId="integeronly" class="w-full" />
    </div>

    <!-- Tipo -->
    <div>
      <label for="tipo" class="block font-semibold mb-1">Tipo</label>
      <Dropdown v-model="product.tipo" :options="tipos" optionLabel="name" placeholder="Selecciona un tipo" class="w-full" />
    </div>
  </div>

  <template #footer>
    <Button label="Cancelar" icon="pi pi-times" text @click="hideDialog" />
    <Button label="Guardar" icon="pi pi-check" @click="saveProduct" />
  </template>
</Dialog>


    <!-- Diálogo de confirmación para eliminar -->
    <Dialog v-model:visible="deleteProductsDialog" :style="{ width: '450px' }" header="Confirmar" :modal="true">
      <div class="flex items-center gap-4">
        <i class="pi pi-exclamation-triangle !text-3xl" />
        <span>¿Estás seguro de que deseas eliminar la materia seleccionada?</span>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" text @click="deleteProductsDialog = false" />
        <Button label="Sí" icon="pi pi-check" @click="deleteSelectedProducts" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import { FilterMatchMode } from '@primevue/core/api';

export default {
  data() {
    return {
      products: [],
      productDialog: false,
      deleteProductsDialog: false,
      product: {
        nombre: '',
        creditos: null,
        tipo: null
      },
      isEdit: false,
      selectedProducts: null,
      filters: {},
      tipos: [
        { name: 'Materia', code: 'M' },
        { name: 'Módulo', code: 'MO' }
      ]
    };
  },
  computed: {
    dialogTitle() {
      return this.isEdit ? 'Editar Materia' : 'Nueva Materia';
    }
  },
  created() {
    this.initFilters();
    this.loadSampleData();
  },
  methods: {
    openNew() {
      this.product = { nombre: '', creditos: null, tipo: null };
      this.isEdit = false;
      this.productDialog = true;
    },
    editProduct(producto) {
      this.product = { ...producto }; // Clonar para no modificar directo
      this.isEdit = true;
      this.productDialog = true;
    },
    hideDialog() {
      this.productDialog = false;
    },
    saveProduct() {
      if (this.product.nombre && this.product.creditos && this.product.tipo) {
        if (this.isEdit) {
          const index = this.products.findIndex(p => p.id === this.product.id);
          this.products[index] = { ...this.product };
        } else {
          const newProduct = {
            ...this.product,
            id: this.createId(),
            codigo: this.createId()
          };
          this.products.push(newProduct);
        }
        this.productDialog = false;
        this.product = { nombre: '', creditos: null, tipo: null };
        this.isEdit = false;
      } else {
        alert('Por favor llena todos los campos.');
      }
    },
    confirmDeleteSelected() {
      this.deleteProductsDialog = true;
    },
    deleteSelectedProducts() {
      this.products = this.products.filter(p => !this.selectedProducts.includes(p));
      this.selectedProducts = null;
      this.deleteProductsDialog = false;
    },
    createId() {
      let id = '';
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      for (let i = 0; i < 5; i++) {
        id += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return id;
    },
    initFilters() {
      this.filters = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS }
      };
    },
    loadSampleData() {
      this.products = [
        { id: '1', codigo: 'P001', nombre: 'Programación', creditos: 4, tipo: { name: 'Materia' } },
        { id: '2', codigo: 'P002', nombre: 'Base de Datos', creditos: 3, tipo: { name: 'Módulo' } }
      ];
    }
  }
};
</script>
