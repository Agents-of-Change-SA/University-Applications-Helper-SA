import React from 'react';
import {StyleSheet} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppButton} from '../../../components/AppButton';
import {ROUTES} from '../../../common/constants/routes';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import type {CourseStackParamList} from '../../../navigation/MainTabNavigator';

type NavProp = NativeStackNavigationProp<CourseStackParamList, typeof ROUTES.CourseSearch>;

const CourseSearchScreen: React.FC = () => {
  const navigation = useNavigation<NavProp>();

  const handleCheckCourses = () => {
    navigation.navigate(ROUTES.QualificationCheck);
  };

  return (
    <ScreenWrapper>
      <AppText variant="heading">Course Search</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        Find courses you qualify for based on your school profile
      </AppText>

      <AppButton title="Check My Courses" onPress={handleCheckCourses} style={styles.searchBtn} />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.xxl},
  searchBtn: {marginTop: Spacing.lg},
});

export default CourseSearchScreen;
