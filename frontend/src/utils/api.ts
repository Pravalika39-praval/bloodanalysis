import axios from "axios";

const API_BASE_URL = "http://192.168.0.132:8000";

export const uploadBloodReport = async (formData: any) => {
  return await axios.post(`${API_BASE_URL}/predict`, formData, {
    headers: { "Content-Type": "application/json" },
    
  });
};
