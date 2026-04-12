import {
  formatDate,
  formatFee,
  getApplicationStatus,
} from '../../src/features/applications/utils/formatters';

describe('formatDate', () => {
  it('formats a valid ISO 8601 date to "DD Mon YYYY"', () => {
    expect(formatDate('2025-01-15T00:00:00Z')).toBe('15 Jan 2025');
  });

  it('formats dates with different months correctly', () => {
    expect(formatDate('2025-03-01T00:00:00Z')).toBe('01 Mar 2025');
    expect(formatDate('2025-12-25T00:00:00Z')).toBe('25 Dec 2025');
  });

  it('pads single-digit days with a leading zero', () => {
    expect(formatDate('2025-06-05T00:00:00Z')).toBe('05 Jun 2025');
  });

  it('returns the raw string for an invalid date', () => {
    expect(formatDate('not-a-date')).toBe('not-a-date');
    expect(formatDate('')).toBe('');
  });
});

describe('formatFee', () => {
  it('formats a number as "R{amount}"', () => {
    expect(formatFee(200)).toBe('R200');
  });

  it('formats zero fee', () => {
    expect(formatFee(0)).toBe('R0');
  });

  it('formats large fees', () => {
    expect(formatFee(1500)).toBe('R1500');
  });
});

describe('getApplicationStatus', () => {
  it('returns "Open" when current date is between open and close dates', () => {
    const result = getApplicationStatus(
      '2025-01-01T00:00:00Z',
      '2025-12-31T23:59:59Z',
      new Date('2025-06-15T12:00:00Z'),
    );
    expect(result).toBe('Open');
  });

  it('returns "Open" when current date equals the open date', () => {
    const result = getApplicationStatus(
      '2025-06-15T00:00:00Z',
      '2025-12-31T23:59:59Z',
      new Date('2025-06-15T00:00:00Z'),
    );
    expect(result).toBe('Open');
  });

  it('returns "Open" when current date equals the close date', () => {
    const result = getApplicationStatus(
      '2025-01-01T00:00:00Z',
      '2025-06-15T23:59:59Z',
      new Date('2025-06-15T23:59:59Z'),
    );
    expect(result).toBe('Open');
  });

  it('returns "Closed" when current date is before the open date', () => {
    const result = getApplicationStatus(
      '2025-06-01T00:00:00Z',
      '2025-12-31T23:59:59Z',
      new Date('2025-01-01T00:00:00Z'),
    );
    expect(result).toBe('Closed');
  });

  it('returns "Closed" when current date is after the close date', () => {
    const result = getApplicationStatus(
      '2025-01-01T00:00:00Z',
      '2025-06-30T23:59:59Z',
      new Date('2025-12-01T00:00:00Z'),
    );
    expect(result).toBe('Closed');
  });

  it('returns "Closed" for unparseable open date', () => {
    const result = getApplicationStatus(
      'invalid',
      '2025-12-31T23:59:59Z',
      new Date('2025-06-15T12:00:00Z'),
    );
    expect(result).toBe('Closed');
  });

  it('returns "Closed" for unparseable close date', () => {
    const result = getApplicationStatus(
      '2025-01-01T00:00:00Z',
      'invalid',
      new Date('2025-06-15T12:00:00Z'),
    );
    expect(result).toBe('Closed');
  });
});
