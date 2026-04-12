import {
  SchoolSubject,
  ExtendedCourse,
  CareerAspiration,
  QualificationCheckResponse,
} from './types';
import {calculateAPS} from '../common/utils/apsCalculator';
import {mockExtendedCourses} from '../mock/extendedCourses';
import SchoolProfileService from './schoolProfileService';
import CareerAspirationsService from './careerAspirationsService';

class QualificationService {
  /**
   * Evaluates whether a learner qualifies for a single course.
   * Returns true iff APS >= course.minimumAPS AND all subject requirements met
   * (case-insensitive subject name matching).
   */
  static evaluateCourse(
    subjects: SchoolSubject[],
    aps: number,
    course: ExtendedCourse,
  ): boolean {
    if (aps < course.minimumAPS) {
      return false;
    }

    for (const req of course.subjectRequirements) {
      const learnerSubject = subjects.find(
        s => s.name.toLowerCase() === req.subjectName.toLowerCase(),
      );
      if (!learnerSubject || learnerSubject.percentage < req.minimumPercentage) {
        return false;
      }
    }

    return true;
  }

  /**
   * Matches qualifying courses against career aspirations.
   * Case-insensitive keyword containment: a course is an aspiration match
   * if its courseName (lowercased) contains at least one whitespace-delimited
   * keyword from any aspiration string (lowercased).
   */
  static matchAspirations(
    courses: ExtendedCourse[],
    aspirations: CareerAspiration[],
  ): {aspirationMatches: ExtendedCourse[]; otherCourses: ExtendedCourse[]} {
    const aspirationMatches: ExtendedCourse[] = [];
    const otherCourses: ExtendedCourse[] = [];

    for (const course of courses) {
      const courseNameLower = course.courseName.toLowerCase();
      const isMatch = aspirations.some(aspiration => {
        const keywords = aspiration.aspiration
          .toLowerCase()
          .split(/\s+/)
          .filter(k => k.length > 0);
        return keywords.some(keyword => courseNameLower.includes(keyword));
      });

      if (isMatch) {
        aspirationMatches.push(course);
      } else {
        otherCourses.push(course);
      }
    }

    return {aspirationMatches, otherCourses};
  }

  /**
   * Orchestrates the full qualification check flow:
   * 1. Fetch school profile
   * 2. Calculate APS
   * 3. Filter all extended courses by APS + subject requirements
   * 4. Fetch aspirations and categorise results
   * 5. Sort qualifying by institution, cap suggested at 20 sorted by APS gap
   */
  static async checkQualification(): Promise<QualificationCheckResponse> {
    try {
      const profile = await SchoolProfileService.getSchoolProfile();
      const subjects = profile.subjects;
      const aps = calculateAPS(subjects);

      const qualifyingCourses = mockExtendedCourses.filter(course =>
        QualificationService.evaluateCourse(subjects, aps, course),
      );

      // Sort qualifying courses by institution name ascending
      qualifyingCourses.sort((a, b) =>
        a.institution.localeCompare(b.institution),
      );

      const aspirations = await CareerAspirationsService.getAspirations();

      const {aspirationMatches, otherCourses} =
        QualificationService.matchAspirations(qualifyingCourses, aspirations);

      // Cap suggested courses at 20, sorted by APS gap ascending
      const suggestedCourses = [...otherCourses]
        .sort(
          (a, b) =>
            Math.abs(aps - a.minimumAPS) - Math.abs(aps - b.minimumAPS),
        )
        .slice(0, 20);

      return {
        aps,
        aspirationMatches,
        qualifyingCourses,
        suggestedCourses,
      };
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(
          `Qualification check failed: ${error.message}`,
        );
      }
      throw new Error(
        'Qualification check failed: An unexpected error occurred',
      );
    }
  }
}

export default QualificationService;
