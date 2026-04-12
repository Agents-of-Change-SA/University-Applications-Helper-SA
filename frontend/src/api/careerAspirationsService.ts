import {
  CareerAspiration,
  CreateAspirationRequest,
  UpdateAspirationRequest,
} from './types';
import {mockAspirations} from '../mock/userProfile';

class CareerAspirationsService {
  static async getAspirations(): Promise<CareerAspiration[]> {
    await new Promise(resolve => setTimeout(resolve, 300));
    return [...mockAspirations];
  }

  static async createAspiration(
    data: CreateAspirationRequest,
  ): Promise<CareerAspiration> {
    await new Promise(resolve => setTimeout(resolve, 300));
    return {
      id: Date.now().toString(),
      aspiration: data.aspiration,
      createdAt: new Date().toISOString(),
    };
  }

  static async updateAspiration(
    id: string,
    data: UpdateAspirationRequest,
  ): Promise<CareerAspiration> {
    await new Promise(resolve => setTimeout(resolve, 300));
    const existing = mockAspirations.find(a => a.id === id);
    return {
      id,
      aspiration: data.aspiration,
      createdAt: existing?.createdAt ?? new Date().toISOString(),
    };
  }
}

export default CareerAspirationsService;
