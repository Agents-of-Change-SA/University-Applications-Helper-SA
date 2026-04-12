import {
  percentageToRating,
  calculateAPS,
} from '../../src/common/utils/apsCalculator';
import {SchoolSubject} from '../../src/api/types';

describe('percentageToRating', () => {
  it('returns 7 for 90–100%', () => {
    expect(percentageToRating(90)).toBe(7);
    expect(percentageToRating(95)).toBe(7);
    expect(percentageToRating(100)).toBe(7);
  });

  it('returns 6 for 80–89%', () => {
    expect(percentageToRating(80)).toBe(6);
    expect(percentageToRating(89)).toBe(6);
  });

  it('returns 5 for 70–79%', () => {
    expect(percentageToRating(70)).toBe(5);
    expect(percentageToRating(79)).toBe(5);
  });

  it('returns 4 for 60–69%', () => {
    expect(percentageToRating(60)).toBe(4);
    expect(percentageToRating(69)).toBe(4);
  });

  it('returns 3 for 50–59%', () => {
    expect(percentageToRating(50)).toBe(3);
    expect(percentageToRating(59)).toBe(3);
  });

  it('returns 2 for 40–49%', () => {
    expect(percentageToRating(40)).toBe(2);
    expect(percentageToRating(49)).toBe(2);
  });

  it('returns 1 for 30–39%', () => {
    expect(percentageToRating(30)).toBe(1);
    expect(percentageToRating(39)).toBe(1);
  });

  it('returns 0 for below 30%', () => {
    expect(percentageToRating(29)).toBe(0);
    expect(percentageToRating(0)).toBe(0);
  });
});

describe('calculateAPS', () => {
  const makeSubject = (name: string, percentage: number): SchoolSubject => ({
    name,
    percentage,
    level: 1,
  });

  it('returns 0 for an empty subject array', () => {
    expect(calculateAPS([])).toBe(0);
  });

  it('returns 0 when only Life Orientation is present', () => {
    expect(calculateAPS([makeSubject('Life Orientation', 95)])).toBe(0);
  });

  it('excludes Life Orientation from calculation', () => {
    const subjects = [
      makeSubject('Mathematics', 90), // 7
      makeSubject('English', 80), // 6
      makeSubject('Life Orientation', 100), // excluded
    ];
    expect(calculateAPS(subjects)).toBe(13); // 7 + 6
  });

  it('sums best 6 subjects when more than 6 non-LO subjects exist', () => {
    const subjects = [
      makeSubject('Mathematics', 90), // 7
      makeSubject('English', 80), // 6
      makeSubject('Physical Sciences', 70), // 5
      makeSubject('Life Sciences', 60), // 4
      makeSubject('Accounting', 50), // 3
      makeSubject('History', 40), // 2
      makeSubject('Geography', 30), // 1 — excluded (7th best)
    ];
    expect(calculateAPS(subjects)).toBe(27); // 7+6+5+4+3+2
  });

  it('handles exactly 6 non-LO subjects', () => {
    const subjects = [
      makeSubject('Mathematics', 90), // 7
      makeSubject('English', 80), // 6
      makeSubject('Physical Sciences', 70), // 5
      makeSubject('Life Sciences', 60), // 4
      makeSubject('Accounting', 50), // 3
      makeSubject('History', 40), // 2
    ];
    expect(calculateAPS(subjects)).toBe(27);
  });

  it('handles a single qualifying subject', () => {
    expect(calculateAPS([makeSubject('Mathematics', 75)])).toBe(5);
  });
});
