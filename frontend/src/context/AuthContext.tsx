import React, {createContext, useContext, useState, useCallback} from 'react';
import AuthService from '../api/authService';
import {User} from '../api/types';

interface AuthState {
  isAuthenticated: boolean;
  token: string | null;
  user: User | null;
  isLoading: boolean;
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  forgotPassword: (email: string) => Promise<void>;
  logout: () => void;
}

const initialState: AuthState = {
  isAuthenticated: false,
  token: null,
  user: null,
  isLoading: false,
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({
  children,
}) => {
  const [state, setState] = useState<AuthState>(initialState);

  const login = useCallback(async (email: string, password: string) => {
    setState(prev => ({...prev, isLoading: true}));
    try {
      const response = await AuthService.login({email, password});
      setState({
        isAuthenticated: true,
        token: response.token,
        user: response.user,
        isLoading: false,
      });
    } catch (error) {
      setState(prev => ({...prev, isLoading: false}));
      throw error;
    }
  }, []);

  const register = useCallback(
    async (name: string, email: string, password: string) => {
      setState(prev => ({...prev, isLoading: true}));
      try {
        const response = await AuthService.register({name, email, password});
        setState({
          isAuthenticated: true,
          token: response.token,
          user: response.user,
          isLoading: false,
        });
      } catch (error) {
        setState(prev => ({...prev, isLoading: false}));
        throw error;
      }
    },
    [],
  );

  const forgotPassword = useCallback(async (email: string) => {
    setState(prev => ({...prev, isLoading: true}));
    try {
      await AuthService.forgotPassword({email});
      setState(prev => ({...prev, isLoading: false}));
    } catch (error) {
      setState(prev => ({...prev, isLoading: false}));
      throw error;
    }
  }, []);

  const logout = useCallback(() => {
    setState(initialState);
  }, []);

  return (
    <AuthContext.Provider
      value={{...state, login, register, forgotPassword, logout}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
