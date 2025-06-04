// types/grupo.ts

import type { Grupo } from "~/features/grupos/models/grupo-model";

export interface Periodo {
  id_periodo: number;
  nombre: string;
  id_grupo: number;
  grupo?: Grupo;
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