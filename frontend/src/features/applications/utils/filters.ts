import { ApplicationEntry, ApplicationDatesRequest } from '../../../api/types';
import { getApplicationStatus } from './formatters';

/**
 * Filter entries by institution name using case-insensitive partial match.
 */
export function filterByInstitutionName(
  entries: ApplicationEntry[],
  name: string,
): ApplicationEntry[] {
  const lowerName = name.toLowerCase();
  return entries.filter(entry =>
    entry.institutionName.toLowerCase().includes(lowerName),
  );
}

/**
 * Filter entries by all active criteria in the request.
 * Returns entries matching ALL active filters.
 */
export function applyFilters(
  entries: ApplicationEntry[],
  filters: ApplicationDatesRequest,
): ApplicationEntry[] {
  return entries.filter(entry => {
    // Institution name filter
    if (
      filters.institutionName &&
      !entry.institutionName
        .toLowerCase()
        .includes(filters.institutionName.toLowerCase())
    ) {
      return false;
    }

    // Open date range filter
    if (filters.openDateFrom) {
      const openDate = new Date(entry.openDate).getTime();
      const from = new Date(filters.openDateFrom).getTime();
      if (isNaN(openDate) || isNaN(from) || openDate < from) {
        return false;
      }
    }
    if (filters.openDateTo) {
      const openDate = new Date(entry.openDate).getTime();
      const to = new Date(filters.openDateTo).getTime();
      if (isNaN(openDate) || isNaN(to) || openDate > to) {
        return false;
      }
    }

    // Close date range filter
    if (filters.closeDateFrom) {
      const closeDate = new Date(entry.closeDate).getTime();
      const from = new Date(filters.closeDateFrom).getTime();
      if (isNaN(closeDate) || isNaN(from) || closeDate < from) {
        return false;
      }
    }
    if (filters.closeDateTo) {
      const closeDate = new Date(entry.closeDate).getTime();
      const to = new Date(filters.closeDateTo).getTime();
      if (isNaN(closeDate) || isNaN(to) || closeDate > to) {
        return false;
      }
    }

    // Fee range filter
    if (filters.minFee !== undefined && entry.applicationFee < filters.minFee) {
      return false;
    }
    if (filters.maxFee !== undefined && entry.applicationFee > filters.maxFee) {
      return false;
    }

    return true;
  });
}

/**
 * Sort entries so "Open" status entries appear before "Closed" entries.
 */
export function sortByStatus(
  entries: ApplicationEntry[],
  currentDate?: Date,
): ApplicationEntry[] {
  return [...entries].sort((a, b) => {
    const statusA = getApplicationStatus(a.openDate, a.closeDate, currentDate);
    const statusB = getApplicationStatus(b.openDate, b.closeDate, currentDate);

    if (statusA === statusB) {
      return 0;
    }
    return statusA === 'Open' ? -1 : 1;
  });
}
