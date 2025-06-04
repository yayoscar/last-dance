// types/periodo.ts
export interface Periodo {
  id_periodo?: number;
  nombre: string;
}

export interface PeriodoCreate {
  nombre: string;
}

export interface PeriodoUpdate {
  nombre: string;
  id_periodo: number;
}