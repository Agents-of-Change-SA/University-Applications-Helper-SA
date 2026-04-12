import {ExtendedCourse} from '../api/types';

export const mockExtendedCourses: ExtendedCourse[] = [
  // === University of Cape Town (UCT) ===
  {
    id: 'ext-1',
    courseName: 'Bachelor of Science in Computer Science',
    institution: 'University of Cape Town',
    apsSummary: 'APS: 34+',
    requirements: 'Mathematics 60%, English 50%',
    minimumAPS: 34,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },
  {
    id: 'ext-2',
    courseName: 'Bachelor of Medicine and Surgery (MBChB)',
    institution: 'University of Cape Town',
    apsSummary: 'APS: 42+',
    requirements:
      'Mathematics 70%, Physical Sciences 70%, English 60%, Life Sciences 70%',
    minimumAPS: 42,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 70},
      {subjectName: 'Physical Sciences', minimumPercentage: 70},
      {subjectName: 'English', minimumPercentage: 60},
      {subjectName: 'Life Sciences', minimumPercentage: 70},
    ],
  },

  // === University of the Witwatersrand (Wits) ===
  {
    id: 'ext-3',
    courseName: 'Bachelor of Commerce in Accounting',
    institution: 'University of the Witwatersrand',
    apsSummary: 'APS: 38+',
    requirements: 'Mathematics 70%, English 60%, Accounting 60%',
    minimumAPS: 38,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 70},
      {subjectName: 'English', minimumPercentage: 60},
      {subjectName: 'Accounting', minimumPercentage: 60},
    ],
  },
  {
    id: 'ext-4',
    courseName: 'Bachelor of Science in Engineering (Electrical)',
    institution: 'University of the Witwatersrand',
    apsSummary: 'APS: 36+',
    requirements: 'Mathematics 70%, Physical Sciences 60%, English 50%',
    minimumAPS: 36,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 70},
      {subjectName: 'Physical Sciences', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },

  // === Stellenbosch University ===
  {
    id: 'ext-5',
    courseName: 'Bachelor of Engineering in Civil Engineering',
    institution: 'Stellenbosch University',
    apsSummary: 'APS: 36+',
    requirements: 'Mathematics 70%, Physical Sciences 60%, English 50%',
    minimumAPS: 36,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 70},
      {subjectName: 'Physical Sciences', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },
  {
    id: 'ext-6',
    courseName: 'Bachelor of Arts in Humanities',
    institution: 'Stellenbosch University',
    apsSummary: 'APS: 30+',
    requirements: 'English 60%',
    minimumAPS: 30,
    subjectRequirements: [
      {subjectName: 'English', minimumPercentage: 60},
    ],
  },

  // === University of Pretoria (UP) ===
  {
    id: 'ext-7',
    courseName: 'Bachelor of Science in Information Technology',
    institution: 'University of Pretoria',
    apsSummary: 'APS: 32+',
    requirements: 'Mathematics 60%, English 50%, Information Technology 50%',
    minimumAPS: 32,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
      {subjectName: 'Information Technology', minimumPercentage: 50},
    ],
  },
  {
    id: 'ext-8',
    courseName: 'Bachelor of Veterinary Science (BVSc)',
    institution: 'University of Pretoria',
    apsSummary: 'APS: 40+',
    requirements:
      'Mathematics 60%, Physical Sciences 60%, Life Sciences 60%, English 50%',
    minimumAPS: 40,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 60},
      {subjectName: 'Physical Sciences', minimumPercentage: 60},
      {subjectName: 'Life Sciences', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },

  // === University of KwaZulu-Natal (UKZN) ===
  {
    id: 'ext-9',
    courseName: 'Bachelor of Laws (LLB)',
    institution: 'University of KwaZulu-Natal',
    apsSummary: 'APS: 32+',
    requirements: 'English 60%',
    minimumAPS: 32,
    subjectRequirements: [
      {subjectName: 'English', minimumPercentage: 60},
    ],
  },
  {
    id: 'ext-10',
    courseName: 'Bachelor of Science in Life Sciences',
    institution: 'University of KwaZulu-Natal',
    apsSummary: 'APS: 30+',
    requirements: 'Mathematics 50%, Life Sciences 60%, English 50%',
    minimumAPS: 30,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 50},
      {subjectName: 'Life Sciences', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },

  // === Durban University of Technology (DUT) ===
  {
    id: 'ext-11',
    courseName: 'Diploma in Information Technology',
    institution: 'Durban University of Technology',
    apsSummary: 'APS: 26+',
    requirements: 'Mathematics 50%, English 50%',
    minimumAPS: 26,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 50},
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },
  {
    id: 'ext-12',
    courseName: 'Diploma in Accounting',
    institution: 'Durban University of Technology',
    apsSummary: 'APS: 24+',
    requirements: 'Mathematical Literacy 60%, English 50%, Accounting 50%',
    minimumAPS: 24,
    subjectRequirements: [
      {subjectName: 'Mathematical Literacy', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
      {subjectName: 'Accounting', minimumPercentage: 50},
    ],
  },
  {
    id: 'ext-13',
    courseName: 'Diploma in Public Relations',
    institution: 'Durban University of Technology',
    apsSummary: 'APS: 22+',
    requirements: 'English 50%',
    minimumAPS: 22,
    subjectRequirements: [
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },

  // === University of Johannesburg (UJ) ===
  {
    id: 'ext-14',
    courseName: 'Bachelor of Education in Foundation Phase',
    institution: 'University of Johannesburg',
    apsSummary: 'APS: 28+',
    requirements: 'English 50%, Mathematical Literacy 50%',
    minimumAPS: 28,
    subjectRequirements: [
      {subjectName: 'English', minimumPercentage: 50},
      {subjectName: 'Mathematical Literacy', minimumPercentage: 50},
    ],
  },
  {
    id: 'ext-15',
    courseName: 'Bachelor of Commerce in Finance',
    institution: 'University of Johannesburg',
    apsSummary: 'APS: 34+',
    requirements: 'Mathematics 60%, English 50%, Accounting 60%',
    minimumAPS: 34,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
      {subjectName: 'Accounting', minimumPercentage: 60},
    ],
  },
  {
    id: 'ext-16',
    courseName: 'Bachelor of Science in Physical Sciences',
    institution: 'University of Johannesburg',
    apsSummary: 'APS: 30+',
    requirements: 'Mathematics 50%, Physical Sciences 50%, English 50%',
    minimumAPS: 30,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 50},
      {subjectName: 'Physical Sciences', minimumPercentage: 50},
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },

  // === Additional courses for broader coverage ===
  {
    id: 'ext-17',
    courseName: 'Bachelor of Pharmacy',
    institution: 'University of KwaZulu-Natal',
    apsSummary: 'APS: 36+',
    requirements:
      'Mathematics 60%, Physical Sciences 60%, Life Sciences 60%, English 50%',
    minimumAPS: 36,
    subjectRequirements: [
      {subjectName: 'Mathematics', minimumPercentage: 60},
      {subjectName: 'Physical Sciences', minimumPercentage: 60},
      {subjectName: 'Life Sciences', minimumPercentage: 60},
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },
  {
    id: 'ext-18',
    courseName: 'Diploma in Tourism Management',
    institution: 'University of Johannesburg',
    apsSummary: 'APS: 24+',
    requirements: 'English 50%',
    minimumAPS: 24,
    subjectRequirements: [
      {subjectName: 'English', minimumPercentage: 50},
    ],
  },
];
