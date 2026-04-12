import {RegisterOptions, FieldValues, Path} from 'react-hook-form';

export const validationRules = {
  required: (fieldName: string): RegisterOptions<FieldValues, Path<FieldValues>> => ({
    required: `${fieldName} is required`,
    validate: (value: string) =>
      (typeof value === 'string' && value.trim().length > 0) ||
      `${fieldName} is required`,
  }),

  email: (): RegisterOptions<FieldValues, Path<FieldValues>> => ({
    required: 'Email is required',
    pattern: {
      value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: 'Please enter a valid email address',
    },
  }),

  positiveInteger: (fieldName: string): RegisterOptions<FieldValues, Path<FieldValues>> => ({
    required: `${fieldName} is required`,
    validate: (value: string | number) => {
      const num = typeof value === 'string' ? Number(value) : value;
      if (isNaN(num)) {
        return `${fieldName} must be a number`;
      }
      if (!Number.isInteger(num) || num <= 0) {
        return `${fieldName} must be a positive integer`;
      }
      return true;
    },
  }),

  percentage: (): RegisterOptions<FieldValues, Path<FieldValues>> => ({
    required: 'Percentage is required',
    validate: (value: string | number) => {
      const num = typeof value === 'string' ? Number(value) : value;
      if (isNaN(num)) {
        return 'Percentage must be a number';
      }
      if (num < 0 || num > 100) {
        return 'Percentage must be between 0 and 100';
      }
      return true;
    },
  }),

  matchField: (fieldName: string, watchValue: string): RegisterOptions<FieldValues, Path<FieldValues>> => ({
    validate: (value: string) =>
      value === watchValue || `${fieldName} must match`,
  }),

  nonEmptyString: (fieldName: string): RegisterOptions<FieldValues, Path<FieldValues>> => ({
    required: `${fieldName} is required`,
    validate: (value: string) =>
      (typeof value === 'string' && value.trim().length > 0) ||
      `${fieldName} cannot be empty`,
  }),
};
