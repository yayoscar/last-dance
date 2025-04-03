<template>
    <div class="p-5">
      <h1 class="text-2xl font-bold mb-4">Materias</h1>
      
      <table class="w-full border-collapse border border-gray-300">
        <thead>
          <tr class="bg-gray-200">
            <th class="border border-gray-300 p-2">ID</th>
            <th class="border border-gray-300 p-2">Nombre</th>
            <th class="border border-gray-300 p-2">Tipo</th>
            <th class="border border-gray-300 p-2">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="materia in materias" :key="materia.id" class="text-center">
            <td class="border border-gray-300 p-2">{{ materia.id }}</td>
            <td class="border border-gray-300 p-2">{{ materia.nombre }}</td>
            <td class="border border-gray-300 p-2">{{ materia.tipo }}</td>
            <td class="border border-gray-300 p-2">
              <!-- Botón Eliminar con icono y estilo más visible -->
              <button 
                class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 focus:outline-none"
                @click="eliminarMateria(materia.id)"
              >
                <i class="pi pi-trash"></i> Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <button 
        class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        @click="mostrarModal = true"
      >
        Agregar Materia
      </button>
  
      <!-- Modal para agregar materia -->
      <div v-if="mostrarModal" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
        <div class="bg-white p-5 rounded shadow-lg w-96">
          <h2 class="text-xl font-bold mb-4">Nueva Materia</h2>
          
          <label class="block mb-2">Nombre:</label>
          <input v-model="nuevaMateria.nombre" type="text" class="w-full border p-2 rounded mb-4" />
          
          <label class="block mb-2">Tipo:</label>
          <select v-model="nuevaMateria.tipo" class="w-full border p-2 rounded mb-4">
            <option value="materia">Materia</option>
            <option value="submodulo">Submódulo</option>
          </select>
          
          <div class="flex justify-end gap-2">
            <button @click="mostrarModal = false" class="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500">Cancelar</button>
            <button @click="agregarMateria" class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">Agregar</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        materias: [
          { id: 1, nombre: "Matemáticas", tipo: "Materia" },
          { id: 2, nombre: "Física", tipo: "Materia" },
          { id: 3, nombre: "Química", tipo: "Materia" }
        ],
        mostrarModal: false,
        nuevaMateria: {
          nombre: "",
          tipo: "materia"
        }
      };
    },
    methods: {
      agregarMateria() {
        if (this.nuevaMateria.nombre.trim() === "") return;
        
        const nueva = {
          id: this.materias.length + 1,
          nombre: this.nuevaMateria.nombre,
          tipo: this.nuevaMateria.tipo
        };
        
        this.materias.push(nueva);
        this.nuevaMateria.nombre = "";
        this.nuevaMateria.tipo = "materia";
        this.mostrarModal = false;
      },
      eliminarMateria(id) {
        this.materias = this.materias.filter(materia => materia.id !== id);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilos para mejorar la visibilidad del botón eliminar */
  button {
    font-size: 0.875rem; /* Tamaño de fuente más pequeño */
    display: flex;
    align-items: center;
    gap: 5px;
  }
  button:hover {
    background-color: #e11d48; /* Fondo rojo oscuro en hover */
  }
  </style>
  