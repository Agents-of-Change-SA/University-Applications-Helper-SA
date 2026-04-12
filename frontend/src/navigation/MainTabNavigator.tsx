import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import {ROUTES} from '../common/constants/routes';
import {CourseResult} from '../api/types';
import HomeScreen from '../features/home/screens/HomeScreen';
import CourseSearchScreen from '../features/courses/screens/CourseSearchScreen';
import CourseResultsScreen from '../features/courses/screens/CourseResultsScreen';
import TutorsScreen from '../features/tutors/screens/TutorsScreen';
import ProfileScreen from '../features/profile/screens/ProfileScreen';
import UserDetailsScreen from '../features/profile/screens/UserDetailsScreen';
import SchoolProfileScreen from '../features/school/screens/SchoolProfileScreen';
import CareerGuidanceScreen from '../features/careers/screens/CareerGuidanceScreen';
import CareerAspirationsScreen from '../features/careers/screens/CareerAspirationsScreen';

// -- Home Stack --
export type HomeStackParamList = {
  [ROUTES.Home]: undefined;
  [ROUTES.CareerGuidance]: undefined;
};

const HomeStack = createNativeStackNavigator<HomeStackParamList>();

const HomeStackScreen: React.FC = () => (
  <HomeStack.Navigator screenOptions={{headerShown: false}}>
    <HomeStack.Screen name={ROUTES.Home} component={HomeScreen} />
    <HomeStack.Screen
      name={ROUTES.CareerGuidance}
      component={CareerGuidanceScreen}
    />
  </HomeStack.Navigator>
);

// -- Course Stack --
export type CourseStackParamList = {
  [ROUTES.CourseSearch]: undefined;
  [ROUTES.CourseResults]: {topResult: CourseResult | null; results: CourseResult[]};
};

const CourseStack = createNativeStackNavigator<CourseStackParamList>();

const CourseStackScreen: React.FC = () => (
  <CourseStack.Navigator screenOptions={{headerShown: false}}>
    <CourseStack.Screen
      name={ROUTES.CourseSearch}
      component={CourseSearchScreen}
    />
    <CourseStack.Screen
      name={ROUTES.CourseResults}
      component={CourseResultsScreen}
    />
  </CourseStack.Navigator>
);

// -- Profile Stack --
export type ProfileStackParamList = {
  [ROUTES.Profile]: undefined;
  [ROUTES.UserDetails]: undefined;
  [ROUTES.SchoolProfile]: undefined;
  [ROUTES.CareerAspirations]: undefined;
};

const ProfileStack = createNativeStackNavigator<ProfileStackParamList>();

const ProfileStackScreen: React.FC = () => (
  <ProfileStack.Navigator screenOptions={{headerShown: false}}>
    <ProfileStack.Screen name={ROUTES.Profile} component={ProfileScreen} />
    <ProfileStack.Screen
      name={ROUTES.UserDetails}
      component={UserDetailsScreen}
    />
    <ProfileStack.Screen
      name={ROUTES.SchoolProfile}
      component={SchoolProfileScreen}
    />
    <ProfileStack.Screen
      name={ROUTES.CareerAspirations}
      component={CareerAspirationsScreen}
    />
  </ProfileStack.Navigator>
);

// -- Bottom Tabs --
const Tab = createBottomTabNavigator();

export const MainTabNavigator: React.FC = () => {
  return (
    <Tab.Navigator screenOptions={{headerShown: false}}>
      <Tab.Screen name="HomeTab" component={HomeStackScreen} options={{title: 'Home'}} />
      <Tab.Screen name="CoursesTab" component={CourseStackScreen} options={{title: 'Courses'}} />
      <Tab.Screen name="TutorsTab" component={TutorsScreen} options={{title: 'Tutors'}} />
      <Tab.Screen name="ProfileTab" component={ProfileStackScreen} options={{title: 'Profile'}} />
    </Tab.Navigator>
  );
};
