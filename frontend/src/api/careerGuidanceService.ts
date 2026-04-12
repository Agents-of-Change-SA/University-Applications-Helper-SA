import {CareerGuidanceResponse} from './types';
import {mockCareerGuidance} from '../mock/careerGuidance';

class CareerGuidanceService {
  static async getGuidance(aspiration: string): Promise<CareerGuidanceResponse> {
    await new Promise(resolve => setTimeout(resolve, 500));

    const key = Object.keys(mockCareerGuidance).find(
      k => k.toLowerCase() === aspiration.toLowerCase(),
    );

    if (key) {
      return mockCareerGuidance[key];
    }

    // Default response for unknown aspirations
    return {
      aspiration,
      recommendations: [],
    };
  }
}

export default CareerGuidanceService;
