// features/materias/models/materia-model.ts
export interface Materia {
    id_materia: number;  // Cambiado de string a number para coincidir con tu API
    nombre: string;
    creditos: number;
    tipo: string | number;  // Dependiendo de si es string o number en tu backend
    id_modulo?: number;  // Opcional si existe en tu modelo
}

export interface MateriaModel extends Materia {} // Para mantener compatibilidad