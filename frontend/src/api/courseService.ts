import {CourseSearchResponse} from './types';
import {mockCourses} from '../mock/courses';

class CourseService {
  static async searchCourses(): Promise<CourseSearchResponse> {
    await new Promise<void>(resolve => setTimeout(resolve, 500));
    return {
      topResult: mockCourses.length > 0 ? mockCourses[0] : null,
      results: mockCourses,
    };
  }
}

export default CourseService;
