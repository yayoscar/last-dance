// types/grupo.ts

import type { Periodo } from "~/features/periodos/models/periodo-model";

export interface Grupo {
  id_grupo: number;
  nombre: string;
  id_periodo: number;
  periodo?: Periodo;
}

export interface GrupoCreate {
  nombre: string;
  id_periodo: number;
}

export interface GrupoUpdate {
  nombre: string;
  id_periodo: number;
}

export interface AlumnoAsignacion {
  id_alumno: number;
  semestre: number;
}

export interface GrupoAlumnoAgregar {
  alumnos: AlumnoAsignacion[];
}

export interface AlumnoGrupo {
  id_alumno: number;
  nombre: string;
  ape_paterno: string
  ape_materno: string
  num_control: string
  curp: string;
  turno:string;
  generacion: string;
  semestre: number;  
}

export interface GrupoConAlumnos extends Grupo {
  alumnos: AlumnoGrupo[];
}