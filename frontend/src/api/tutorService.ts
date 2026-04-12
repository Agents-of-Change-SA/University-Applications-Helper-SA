import {Tutor} from './types';
import {mockTutors} from '../mock/tutors';

class TutorService {
  static async getTutors(): Promise<Tutor[]> {
    await new Promise<void>(resolve => setTimeout(resolve, 300));
    return [...mockTutors];
  }
}

export default TutorService;
