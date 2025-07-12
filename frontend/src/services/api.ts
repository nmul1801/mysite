import axios from 'axios';
import type {
  LeagueAssemblyRequest,
  LeagueAssemblyResponse,
  AnalysisResponse,
  DebugResponse,
  DraftProcessingResponse,
} from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const leagueApi = {
  // Assembly endpoints
  assembleScoring: async (data: LeagueAssemblyRequest): Promise<LeagueAssemblyResponse> => {
    const response = await api.post('/leagues/assemble-scoring/', data);
    return response.data;
  },

  assembleScoringStream: async (data: LeagueAssemblyRequest): Promise<Response> => {
    return fetch(`${API_BASE_URL}/leagues/assemble-scoring-stream/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  },

  assembleDraft: async (data: LeagueAssemblyRequest): Promise<LeagueAssemblyResponse> => {
    const response = await api.post('/leagues/assemble-draft/', data);
    return response.data;
  },

  // Draft processing
  processDraft: async (leagueId: string): Promise<DraftProcessingResponse> => {
    const response = await api.post(`/leagues/${leagueId}/process-draft/`);
    return response.data;
  },

  // Progress tracking
  getProgress: async (assemblyId: string): Promise<any> => {
    const response = await api.get(`/progress/${assemblyId}/`);
    return response.data;
  },

  // Debug endpoint
  getDebugInfo: async (leagueId: string): Promise<DebugResponse> => {
    const response = await api.get(`/leagues/${leagueId}/debug/`);
    return response.data;
  },

  // Scoring analysis endpoints
  getExpectedWins: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/scoring/expected-wins/`);
    return response.data;
  },

  getEWDifference: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/scoring/ew-difference/`);
    return response.data;
  },

  getLuckAnalysis: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/scoring/luck/`);
    return response.data;
  },

  getBonageAnalysis: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/scoring/bonage/`);
    return response.data;
  },

  getConsistencyAnalysis: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/scoring/consistency/`);
    return response.data;
  },

  getProbabilityCurve: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/scoring/probability-curve/`);
    return response.data;
  },

  // Draft analysis endpoints
  getSleepers: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/draft/sleepers/`);
    return response.data;
  },

  getPositionalRanks: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/draft/positional-ranks/`);
    return response.data;
  },

  getDraftInjury: async (leagueId: string): Promise<AnalysisResponse> => {
    const response = await api.get(`/leagues/${leagueId}/draft/injury-table/`);
    return response.data;
  },
};

export default api; 