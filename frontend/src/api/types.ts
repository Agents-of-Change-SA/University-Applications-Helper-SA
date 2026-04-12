// === Auth ===

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}

export interface RegisterResponse {
  token: string;
  user: User;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  email: string;
  code: string;
  newPassword: string;
}

// === User ===

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface UserDetails {
  id: string;
  name: string;
  surname: string;
  age: number;
  careerAspiration?: string;
}

export interface CreateUserDetailsRequest {
  name: string;
  surname: string;
  age: number;
  careerAspiration?: string;
}

export interface UpdateUserDetailsRequest {
  name?: string;
  surname?: string;
  age?: number;
  careerAspiration?: string;
}

// === School Profile ===

export interface SchoolSubject {
  name: string;
  percentage: number;
  level: number;
}

export interface SchoolProfile {
  id: string;
  schoolName: string;
  subjects: SchoolSubject[];
}

export interface SchoolProfileRequest {
  name: string;
  subjects: SchoolSubject[];
}

// === Career Guidance ===

export interface CareerGuidanceResponse {
  aspiration: string;
  recommendations: SubjectRecommendation[];
}

export interface SubjectRecommendation {
  subject: string;
  explanation: string;
}

// === Career Aspirations ===

export interface CareerAspiration {
  id: string;
  aspiration: string;
  createdAt: string;
}

export interface CreateAspirationRequest {
  aspiration: string;
}

export interface UpdateAspirationRequest {
  aspiration: string;
}

// === Courses ===

export interface CourseResult {
  id: string;
  courseName: string;
  institution: string;
  apsSummary: string;
  requirements: string;
}

export interface CourseSearchResponse {
  topResult: CourseResult | null;
  results: CourseResult[];
}

// === Tutors ===

export interface Tutor {
  id: string;
  name: string;
  subject: string;
  contact: string;
}
