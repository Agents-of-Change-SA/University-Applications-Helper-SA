import axios, {AxiosInstance} from 'axios';

class HttpClient {
  private static instance: AxiosInstance = axios.create();

  static configure(baseURL: string): void {
    HttpClient.instance = axios.create({baseURL});
  }

  static async get<T>(url: string): Promise<T> {
    const response = await HttpClient.instance.get<T>(url);
    return response.data;
  }

  static async post<T>(url: string, data: unknown): Promise<T> {
    const response = await HttpClient.instance.post<T>(url, data);
    return response.data;
  }

  static async patch<T>(url: string, data: unknown): Promise<T> {
    const response = await HttpClient.instance.patch<T>(url, data);
    return response.data;
  }
}

export default HttpClient;
