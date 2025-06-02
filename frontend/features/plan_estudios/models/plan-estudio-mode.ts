// types/planEstudio.ts

import type { Carrera } from "~/features/carreras/models/carrera-model";

export interface PlanEstudio {
  id_plan_estudio: number;
  nombre: string;
  id_carrera: number;
  carrera?: Carrera;
}

export interface PlanEstudioCreate {
  nombre: string;
  id_carrera: number;
}

export interface PlanEstudioUpdate {
  nombre: string;
  id_carrera: number;
}

export interface MateriaAsignacion {
  id_materia: number;
  semestre: number;
}

export interface PlanEstudioMateriaAgregar {
  materias: MateriaAsignacion[];
}

export interface MateriaPlan {
  id_materia: number;
  nombre: string;
  creditos: number;
  tipo: string;
  id_modulo: number;
  semestre: number;
}

export interface PlanEstudioConMaterias extends PlanEstudio {
  materias: MateriaPlan[];
}