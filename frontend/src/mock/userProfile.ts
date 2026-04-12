import {UserDetails, SchoolProfile, CareerAspiration} from '../api/types';

export const mockUserDetails: UserDetails = {
  id: '1',
  name: 'Thandi',
  surname: 'Mkhize',
  age: 17,
  careerAspiration: 'Software Engineer',
};

export const mockSchoolProfile: SchoolProfile = {
  id: '1',
  schoolName: 'Pretoria High School for Girls',
  subjects: [
    {name: 'Mathematics', percentage: 78, level: 7},
    {name: 'English', percentage: 72, level: 6},
    {name: 'Physical Sciences', percentage: 65, level: 5},
    {name: 'Information Technology', percentage: 85, level: 7},
    {name: 'Life Sciences', percentage: 70, level: 6},
    {name: 'Afrikaans', percentage: 60, level: 5},
  ],
};

export const mockAspirations: CareerAspiration[] = [
  {
    id: '1',
    aspiration: 'Software Engineer',
    createdAt: '2025-01-15T10:00:00Z',
  },
];
