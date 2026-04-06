import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  ForgotPasswordRequest,
  ResetPasswordRequest,
} from './types';

class AuthService {
  static async login(request: LoginRequest): Promise<LoginResponse> {
    // Mock: simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));
    return {
      token: 'mock-jwt-token-' + Date.now(),
      user: {id: '1', name: 'Thandi Mkhize', email: request.email},
    };
  }

  static async register(request: RegisterRequest): Promise<RegisterResponse> {
    await new Promise(resolve => setTimeout(resolve, 500));
    return {
      token: 'mock-jwt-token-' + Date.now(),
      user: {id: '2', name: request.name, email: request.email},
    };
  }

  static async forgotPassword(
    _request: ForgotPasswordRequest,
  ): Promise<{message: string}> {
    await new Promise(resolve => setTimeout(resolve, 500));
    return {message: 'Password reset link sent to your email.'};
  }

  static async resetPassword(
    _request: ResetPasswordRequest,
  ): Promise<{message: string}> {
    await new Promise(resolve => setTimeout(resolve, 500));
    return {message: 'Password has been reset successfully.'};
  }
}

export default AuthService;
