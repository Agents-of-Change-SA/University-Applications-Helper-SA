import {SchoolSubject} from '../../api/types';

/**
 * Converts a percentage mark to an APS rating point.
 * 7 = 90–100%, 6 = 80–89%, 5 = 70–79%, 4 = 60–69%,
 * 3 = 50–59%, 2 = 40–49%, 1 = 30–39%, 0 = below 30%
 */
export function percentageToRating(percentage: number): number {
  if (percentage >= 90) {
    return 7;
  }
  if (percentage >= 80) {
    return 6;
  }
  if (percentage >= 70) {
    return 5;
  }
  if (percentage >= 60) {
    return 4;
  }
  if (percentage >= 50) {
    return 3;
  }
  if (percentage >= 40) {
    return 2;
  }
  if (percentage >= 30) {
    return 1;
  }
  return 0;
}

/**
 * Calculates APS from a SchoolSubject array.
 * Excludes Life Orientation, takes best 6 subjects by rating, sums rating points.
 * Returns 0 if fewer than 1 qualifying subject.
 */
export function calculateAPS(subjects: SchoolSubject[]): number {
  const qualifying = subjects.filter(
    s => s.name.toLowerCase() !== 'life orientation',
  );

  if (qualifying.length < 1) {
    return 0;
  }

  const ratings = qualifying.map(s => percentageToRating(s.percentage));

  ratings.sort((a, b) => b - a);

  const bestSix = ratings.slice(0, 6);

  return bestSix.reduce((sum, r) => sum + r, 0);
}
