export interface ColonyCoordinate {
  x: number;
  y: number;
}

export interface AnalysisResponse {
  colony_count: number;
  coordinates: ColonyCoordinate[];
  result_image: string; // base64-encoded PNG
}

export interface AnalysisError {
  detail: string;
}
