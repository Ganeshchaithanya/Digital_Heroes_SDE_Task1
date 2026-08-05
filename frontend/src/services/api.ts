import axios from 'axios';
import { InspectionResponse } from '../types/inspection';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const inspectUrl = async (targetUrl: string): Promise<InspectionResponse> => {
  const response = await axios.post<InspectionResponse>(`${API_BASE_URL}/inspect`, {
    url: targetUrl,
  });
  return response.data;
};
