import React, {useState, useEffect, useCallback} from 'react';
import {View, StyleSheet} from 'react-native';
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
import SchoolProfileService from '../../../api/schoolProfileService';
import QualificationService from '../../../api/qualificationService';
import {calculateAPS} from '../../../common/utils/apsCalculator';
import type {SchoolProfile} from '../../../api/types';
import type {CourseStackParamList} from '../../../navigation/MainTabNavigator';

type NavProp = NativeStackNavigationProp<CourseStackParamList, typeof ROUTES.QualificationCheck>;

type ScreenStatus = 'idle' | 'loading' | 'error';

const QualificationCheckScreen: React.FC = () => {
  const navigation = useNavigation<NavProp>();
  const [profileStatus, setProfileStatus] = useState<'loading' | 'loaded' | 'none'>('loading');
  const [profile, setProfile] = useState<SchoolProfile | null>(null);
  const [aps, setAps] = useState(0);
  const [status, setStatus] = useState<ScreenStatus>('idle');
  const [errorMsg, setErrorMsg] = useState('');

  const loadProfile = useCallback(async () => {
    setProfileStatus('loading');
    try {
      const schoolProfile = await SchoolProfileService.getSchoolProfile();
      if (schoolProfile && schoolProfile.subjects.length > 0) {
        setProfile(schoolProfile);
        setAps(calculateAPS(schoolProfile.subjects));
        setProfileStatus('loaded');
      } else {
        setProfileStatus('none');
      }
    } catch {
      setProfileStatus('none');
    }
  }, []);

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const handleCheck = async () => {
    setStatus('loading');
    try {
      const response = await QualificationService.checkQualification();
      setStatus('idle');
      navigation.navigate(ROUTES.QualificationResults, {response});
    } catch {
      setErrorMsg('Failed to check qualifications. Please try again.');
      setStatus('error');
    }
  };

  if (profileStatus === 'loading') {
    return <LoadingState message="Loading your school profile..." />;
  }

  if (status === 'loading') {
    return <LoadingState message="Checking your qualifications..." />;
  }

  if (status === 'error') {
    return <ErrorState message={errorMsg} onRetry={handleCheck} />;
  }

  return (
    <ScreenWrapper>
      <AppText variant="heading">Qualification Check</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        See which courses you qualify for based on your school profile
      </AppText>

      {profileStatus === 'none' ? (
        <View style={styles.promptContainer}>
          <AppText variant="subheading" center>
            No School Profile Found
          </AppText>
          <AppText
            variant="body"
            color={Colors.textSecondary}
            center
            style={styles.promptText}>
            Please complete your school profile with your subjects and marks
            before checking qualifications.
          </AppText>
          <AppButton
            title="Go to School Profile"
            variant="secondary"
            onPress={() => navigation.goBack()}
            style={styles.promptBtn}
          />
        </View>
      ) : (
        <>
          <View style={styles.apsContainer}>
            <AppText variant="label" color={Colors.textSecondary}>
              Your APS Score
            </AppText>
            <AppText variant="heading" color={Colors.primary}>
              {aps}
            </AppText>
          </View>

          <AppText variant="subheading" style={styles.sectionTitle}>
            Your Subjects
          </AppText>
          {profile?.subjects.map((subject, index) => (
            <View key={index} style={styles.subjectRow}>
              <AppText variant="body" style={styles.subjectName}>
                {subject.name}
              </AppText>
              <AppText variant="body" bold>
                {subject.percentage}%
              </AppText>
            </View>
          ))}

          <AppButton
            title="Check My Qualifications"
            onPress={handleCheck}
            style={styles.checkBtn}
          />
        </>
      )}
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.xl},
  promptContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: Spacing.xxxl,
  },
  promptText: {marginTop: Spacing.sm, marginBottom: Spacing.xl},
  promptBtn: {marginTop: Spacing.md},
  apsContainer: {
    backgroundColor: Colors.primaryLight,
    borderRadius: 12,
    padding: Spacing.lg,
    alignItems: 'center',
    marginBottom: Spacing.xl,
  },
  sectionTitle: {marginBottom: Spacing.md},
  subjectRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: Spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: Colors.divider,
  },
  subjectName: {flex: 1},
  checkBtn: {marginTop: Spacing.xxl},
});

export default QualificationCheckScreen;
