import {
  filterByInstitutionName,
  applyFilters,
  sortByStatus,
} from '../../src/features/applications/utils/filters';
import { ApplicationEntry } from '../../src/api/types';

const makeEntry = (overrides: Partial<ApplicationEntry> = {}): ApplicationEntry => ({
  id: '1',
  institutionName: 'University of Cape Town',
  openDate: '2025-03-01T00:00:00Z',
  closeDate: '2025-09-30T23:59:59Z',
  applicationFee: 200,
  portalUrl: 'https://uct.ac.za/apply',
  ...overrides,
});

const entries: ApplicationEntry[] = [
  makeEntry({ id: '1', institutionName: 'University of Cape Town', applicationFee: 200, openDate: '2025-03-01T00:00:00Z', closeDate: '2025-09-30T23:59:59Z' }),
  makeEntry({ id: '2', institutionName: 'University of the Witwatersrand', applicationFee: 100, openDate: '2025-04-01T00:00:00Z', closeDate: '2025-10-31T23:59:59Z' }),
  makeEntry({ id: '3', institutionName: 'Stellenbosch University', applicationFee: 0, openDate: '2025-01-01T00:00:00Z', closeDate: '2025-06-30T23:59:59Z' }),
  makeEntry({ id: '4', institutionName: 'Durban University of Technology', applicationFee: 300, openDate: '2024-01-01T00:00:00Z', closeDate: '2024-06-30T23:59:59Z' }),
];

describe('filterByInstitutionName', () => {
  it('returns entries matching a partial name (case-insensitive)', () => {
    const result = filterByInstitutionName(entries, 'cape');
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('1');
  });

  it('returns multiple matches', () => {
    const result = filterByInstitutionName(entries, 'university');
    expect(result).toHaveLength(4);
  });

  it('is case-insensitive', () => {
    const result = filterByInstitutionName(entries, 'STELLENBOSCH');
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('3');
  });

  it('returns empty array when no match', () => {
    const result = filterByInstitutionName(entries, 'xyz');
    expect(result).toHaveLength(0);
  });

  it('returns all entries for empty string', () => {
    const result = filterByInstitutionName(entries, '');
    expect(result).toHaveLength(entries.length);
  });
});

describe('applyFilters', () => {
  it('returns all entries when no filters are active', () => {
    const result = applyFilters(entries, {});
    expect(result).toHaveLength(entries.length);
  });

  it('filters by institution name', () => {
    const result = applyFilters(entries, { institutionName: 'cape' });
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('1');
  });

  it('filters by open date range (from)', () => {
    const result = applyFilters(entries, { openDateFrom: '2025-03-15T00:00:00Z' });
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('2');
  });

  it('filters by open date range (to)', () => {
    const result = applyFilters(entries, { openDateTo: '2025-01-01T00:00:00Z' });
    expect(result).toHaveLength(2);
  });

  it('filters by close date range', () => {
    const result = applyFilters(entries, {
      closeDateFrom: '2025-09-01T00:00:00Z',
      closeDateTo: '2025-11-01T00:00:00Z',
    });
    expect(result).toHaveLength(2);
  });

  it('filters by fee range', () => {
    const result = applyFilters(entries, { minFee: 100, maxFee: 200 });
    expect(result).toHaveLength(2);
  });

  it('combines multiple filters (AND logic)', () => {
    const result = applyFilters(entries, {
      institutionName: 'university',
      minFee: 100,
      maxFee: 200,
    });
    expect(result).toHaveLength(2);
    expect(result.map(e => e.id).sort()).toEqual(['1', '2']);
  });

  it('returns empty when no entries match combined filters', () => {
    const result = applyFilters(entries, {
      institutionName: 'cape',
      maxFee: 50,
    });
    expect(result).toHaveLength(0);
  });
});

describe('sortByStatus', () => {
  // Use a date where entries 1,2,3 are open and entry 4 is closed
  const refDate = new Date('2025-05-15T12:00:00Z');

  it('places Open entries before Closed entries', () => {
    const result = sortByStatus(entries, refDate);
    const statuses = result.map(e => {
      const open = new Date(e.openDate).getTime();
      const close = new Date(e.closeDate).getTime();
      const current = refDate.getTime();
      return current >= open && current <= close ? 'Open' : 'Closed';
    });

    const firstClosedIndex = statuses.indexOf('Closed');
    const lastOpenIndex = statuses.lastIndexOf('Open');
    if (firstClosedIndex !== -1 && lastOpenIndex !== -1) {
      expect(lastOpenIndex).toBeLessThan(firstClosedIndex);
    }
  });

  it('does not mutate the original array', () => {
    const original = [...entries];
    sortByStatus(entries, refDate);
    expect(entries).toEqual(original);
  });

  it('handles all entries being Open', () => {
    const allOpen = entries.slice(0, 3); // entries 1,2,3 are open at refDate
    const result = sortByStatus(allOpen, refDate);
    expect(result).toHaveLength(3);
  });

  it('handles empty array', () => {
    const result = sortByStatus([], refDate);
    expect(result).toHaveLength(0);
  });
});
