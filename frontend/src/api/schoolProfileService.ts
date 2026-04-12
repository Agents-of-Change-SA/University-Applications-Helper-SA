import {SchoolProfile, SchoolProfileRequest} from './types';
import {mockSchoolProfile} from '../mock/userProfile';

class SchoolProfileService {
  static async getSchoolProfile(): Promise<SchoolProfile> {
    await new Promise<void>(resolve => setTimeout(resolve, 300));
    return {...mockSchoolProfile, subjects: [...mockSchoolProfile.subjects]};
  }

  static async saveSchoolProfile(
    data: SchoolProfileRequest,
  ): Promise<SchoolProfile> {
    await new Promise<void>(resolve => setTimeout(resolve, 300));
    return {
      id: mockSchoolProfile.id,
      schoolName: data.name,
      subjects: data.subjects,
    };
  }
}

export default SchoolProfileService;
