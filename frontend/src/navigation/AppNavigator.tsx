import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {useAuth} from '../context/AuthContext';
import {AuthStack} from './AuthStack';
import {MainTabNavigator} from './MainTabNavigator';

export const AppNavigator: React.FC = () => {
  const {isAuthenticated} = useAuth();

  return (
    <NavigationContainer>
      {isAuthenticated ? <MainTabNavigator /> : <AuthStack />}
    </NavigationContainer>
  );
};
