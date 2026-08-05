import axios from 'axios';
import { InspectionResponse } from '../types/inspection';

const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'https://digital-heroes-sde-task1.onrender.com/api/v1';

export const inspectUrl = async (targetUrl: string): Promise<InspectionResponse> => {
  const response = await axios.post<InspectionResponse>(`${API_BASE_URL}/inspect`, {
    url: targetUrl,
  });
  return response.data;
};
