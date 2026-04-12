const MONTH_NAMES = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
];

/**
 * Format ISO 8601 date string to "DD Mon YYYY" (e.g. "15 Jan 2025").
 * Returns the raw string as fallback for invalid dates.
 */
export function formatDate(isoDate: string): string {
  const date = new Date(isoDate);
  if (isNaN(date.getTime())) {
    return isoDate;
  }
  const day = String(date.getUTCDate()).padStart(2, '0');
  const month = MONTH_NAMES[date.getUTCMonth()];
  const year = date.getUTCFullYear();
  return `${day} ${month} ${year}`;
}

/**
 * Format number to South African Rand string (e.g. "R200").
 */
export function formatFee(fee: number): string {
  return `R${fee}`;
}

/**
 * Compute application status based on current date.
 * Returns "Open" if currentDate is between openDate and closeDate inclusive,
 * "Closed" otherwise. Defaults to "Closed" for unparseable dates.
 */
export function getApplicationStatus(
  openDate: string,
  closeDate: string,
  currentDate: Date = new Date(),
): 'Open' | 'Closed' {
  const open = new Date(openDate);
  const close = new Date(closeDate);

  if (isNaN(open.getTime()) || isNaN(close.getTime())) {
    return 'Closed';
  }

  // Compare using UTC start-of-day for the current date against the parsed dates
  const current = currentDate.getTime();
  if (current >= open.getTime() && current <= close.getTime()) {
    return 'Open';
  }

  return 'Closed';
}
