import {ApplicationDatesRequest, ApplicationDatesResponse} from './types';
import {mockApplicationDates} from '../mock/applicationDates';
// import HttpClient from './httpClient';

class ApplicationService {
  static async getApplicationDates(
    request?: ApplicationDatesRequest,
  ): Promise<ApplicationDatesResponse> {
    try {
      // Mock mode: simulate network delay, return mock data
      await new Promise<void>(resolve => setTimeout(resolve, 500));
      return {entries: mockApplicationDates};

      // Future backend integration:
      // return await HttpClient.post<ApplicationDatesResponse>(
      //   '/api/application-dates',
      //   request ?? {},
      // );
    } catch (error) {
      throw new Error(
        'Failed to fetch application dates. Please try again later.',
      );
    }
  }
}

export default ApplicationService;
