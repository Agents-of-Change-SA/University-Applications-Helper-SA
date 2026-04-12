import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import {ROUTES} from '../common/constants/routes';
import LoginScreen from '../features/auth/screens/LoginScreen';
import RegisterScreen from '../features/auth/screens/RegisterScreen';
import ForgotPasswordScreen from '../features/auth/screens/ForgotPasswordScreen';
import ResetPasswordScreen from '../features/auth/screens/ResetPasswordScreen';

export type AuthStackParamList = {
  [ROUTES.Login]: undefined;
  [ROUTES.Register]: undefined;
  [ROUTES.ForgotPassword]: undefined;
  [ROUTES.ResetPassword]: undefined;
};

const Stack = createNativeStackNavigator<AuthStackParamList>();

export const AuthStack: React.FC = () => {
  return (
    <Stack.Navigator
      initialRouteName={ROUTES.Login}
      screenOptions={{headerShown: false}}>
      <Stack.Screen name={ROUTES.Login} component={LoginScreen} />
      <Stack.Screen name={ROUTES.Register} component={RegisterScreen} />
      <Stack.Screen
        name={ROUTES.ForgotPassword}
        component={ForgotPasswordScreen}
      />
      <Stack.Screen
        name={ROUTES.ResetPassword}
        component={ResetPasswordScreen}
      />
    </Stack.Navigator>
  );
};
