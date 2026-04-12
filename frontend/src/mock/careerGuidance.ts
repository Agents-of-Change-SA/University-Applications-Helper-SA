import {CareerGuidanceResponse} from '../api/types';

export const mockCareerGuidance: Record<string, CareerGuidanceResponse> = {
  'Software Engineer': {
    aspiration: 'Software Engineer',
    recommendations: [
      {subject: 'Mathematics', explanation: 'Core requirement for CS degrees and logical thinking'},
      {subject: 'Information Technology', explanation: 'Direct exposure to programming concepts'},
      {subject: 'Physical Sciences', explanation: 'Develops analytical and problem-solving skills'},
    ],
  },
  Doctor: {
    aspiration: 'Doctor',
    recommendations: [
      {subject: 'Life Sciences', explanation: 'Essential foundation for medical studies'},
      {subject: 'Physical Sciences', explanation: 'Required for MBChB admission at most universities'},
      {subject: 'Mathematics', explanation: 'Needed for medical degree entry requirements'},
    ],
  },
  Lawyer: {
    aspiration: 'Lawyer',
    recommendations: [
      {subject: 'English', explanation: 'Critical for legal writing, argumentation, and comprehension'},
      {subject: 'History', explanation: 'Builds understanding of legal systems and precedent'},
      {subject: 'Mathematics', explanation: 'Supports logical reasoning and analytical thinking'},
    ],
  },
  Accountant: {
    aspiration: 'Accountant',
    recommendations: [
      {subject: 'Accounting', explanation: 'Direct prerequisite for BCom Accounting degrees'},
      {subject: 'Mathematics', explanation: 'Essential for financial calculations and analysis'},
      {subject: 'English', explanation: 'Important for business communication and reporting'},
    ],
  },
  Teacher: {
    aspiration: 'Teacher',
    recommendations: [
      {subject: 'English', explanation: 'Foundation for communication and instruction'},
      {subject: 'Mathematics', explanation: 'Widely needed subject for education degrees'},
      {subject: 'Life Orientation', explanation: 'Supports understanding of learner development'},
    ],
  },
};
