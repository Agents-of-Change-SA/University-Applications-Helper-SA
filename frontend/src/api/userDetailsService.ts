import {
  UserDetails,
  CreateUserDetailsRequest,
  UpdateUserDetailsRequest,
} from './types';
import {mockUserDetails} from '../mock/userProfile';

class UserDetailsService {
  static async getUserDetails(): Promise<UserDetails> {
    await new Promise(resolve => setTimeout(resolve, 300));
    return {...mockUserDetails};
  }

  static async createUserDetails(
    data: CreateUserDetailsRequest,
  ): Promise<UserDetails> {
    await new Promise(resolve => setTimeout(resolve, 300));
    return {id: Date.now().toString(), ...data};
  }

  static async updateUserDetails(
    data: UpdateUserDetailsRequest,
  ): Promise<UserDetails> {
    await new Promise(resolve => setTimeout(resolve, 300));
    return {...mockUserDetails, ...data};
  }
}

export default UserDetailsService;
