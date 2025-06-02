// types/carrera.ts
export interface Carrera {
  id_carrera?: number;
  nombre: string;
}

export interface CarreraCreate {
  nombre: string;
}

export interface CarreraUpdate {
  nombre: string;
  id_carrera: number;
}