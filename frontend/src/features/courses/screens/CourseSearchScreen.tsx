import React, {useState} from 'react';
import {StyleSheet} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppButton} from '../../../components/AppButton';
import {ErrorState} from '../../../components/ErrorState';
import {LoadingState} from '../../../components/LoadingState';
import {ROUTES} from '../../../common/constants/routes';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import CourseService from '../../../api/courseService';
import type {CourseStackParamList} from '../../../navigation/MainTabNavigator';

type NavProp = NativeStackNavigationProp<CourseStackParamList, typeof ROUTES.CourseSearch>;

const CourseSearchScreen: React.FC = () => {
  const navigation = useNavigation<NavProp>();
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState('');

  const handleSearch = async () => {
    setStatus('loading');
    try {
      const response = await CourseService.searchCourses();
      navigation.navigate(ROUTES.CourseResults, {
        topResult: response.topResult,
        results: response.results,
      });
      setStatus('idle');
    } catch {
      setErrorMsg('Failed to search courses');
      setStatus('error');
    }
  };

  if (status === 'loading') {
    return <LoadingState message="Searching for courses..." />;
  }

  return (
    <ScreenWrapper>
      <AppText variant="heading">Course Search</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        Find courses you qualify for based on your school profile
      </AppText>

      {status === 'error' && (
        <ErrorState message={errorMsg} onRetry={handleSearch} />
      )}

      <AppButton title="Check My Courses" onPress={handleSearch} style={styles.searchBtn} />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.xxl},
  searchBtn: {marginTop: Spacing.lg},
});

export default CourseSearchScreen;
