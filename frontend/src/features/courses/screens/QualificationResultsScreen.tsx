import React, {useState, useEffect} from 'react';
import {View, StyleSheet} from 'react-native';
import {useNavigation, useRoute, RouteProp} from '@react-navigation/native';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppButton} from '../../../components/AppButton';
import {SectionHeading} from '../../../components/SectionHeading';
import {QualificationCourseCard} from '../components/QualificationCourseCard';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import {ROUTES} from '../../../common/constants/routes';
import SchoolProfileService from '../../../api/schoolProfileService';
import type {SchoolSubject} from '../../../api/types';
import type {CourseStackParamList} from '../../../navigation/MainTabNavigator';

type ResultsRoute = RouteProp<CourseStackParamList, typeof ROUTES.QualificationResults>;

const QualificationResultsScreen: React.FC = () => {
  const navigation = useNavigation();
  const route = useRoute<ResultsRoute>();
  const {response} = route.params;
  const {aps, aspirationMatches, qualifyingCourses, suggestedCourses} = response;

  const [learnerSubjects, setLearnerSubjects] = useState<SchoolSubject[]>([]);

  useEffect(() => {
    SchoolProfileService.getSchoolProfile()
      .then(profile => setLearnerSubjects(profile.subjects))
      .catch(() => setLearnerSubjects([]));
  }, []);

  const totalQualifying = aspirationMatches.length + qualifyingCourses.length;
  const hasNoResults =
    aspirationMatches.length === 0 &&
    qualifyingCourses.length === 0 &&
    suggestedCourses.length === 0;

  return (
    <ScreenWrapper>
      <AppText variant="heading">Qualification Results</AppText>

      <View style={styles.apsContainer}>
        <AppText variant="label" color={Colors.textSecondary}>
          Your APS Score
        </AppText>
        <AppText variant="heading" color={Colors.primary}>
          {aps}
        </AppText>
      </View>

      <AppText variant="body" color={Colors.textSecondary} style={styles.countText}>
        {totalQualifying} qualifying course{totalQualifying !== 1 ? 's' : ''} found
      </AppText>

      {hasNoResults && (
        <View style={styles.encouragementContainer}>
          <AppText variant="subheading" center>
            Keep Going!
          </AppText>
          <AppText
            variant="body"
            color={Colors.textSecondary}
            center
            style={styles.encouragementText}>
            You don't currently qualify for any courses in our database, but
            don't be discouraged. Focus on improving your marks and consider
            speaking to a career counsellor about your options.
          </AppText>
        </View>
      )}

      {aspirationMatches.length > 0 && (
        <>
          <SectionHeading title="Courses Matching Your Aspirations" />
          {aspirationMatches.map(course => (
            <QualificationCourseCard
              key={course.id}
              course={course}
              learnerSubjects={learnerSubjects}
              learnerAPS={aps}
            />
          ))}
        </>
      )}

      {qualifyingCourses.length > 0 && (
        <>
          <SectionHeading title="Other Courses You Qualify For" />
          {qualifyingCourses.map(course => (
            <QualificationCourseCard
              key={course.id}
              course={course}
              learnerSubjects={learnerSubjects}
              learnerAPS={aps}
            />
          ))}
        </>
      )}

      {suggestedCourses.length > 0 && (
        <>
          <SectionHeading title="Suggested Courses to Explore" />
          {suggestedCourses.map(course => (
            <QualificationCourseCard
              key={course.id}
              course={course}
              learnerSubjects={learnerSubjects}
              learnerAPS={aps}
            />
          ))}
        </>
      )}

      <AppButton
        title="Back"
        variant="link"
        onPress={() => navigation.goBack()}
        style={styles.backBtn}
      />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  apsContainer: {
    backgroundColor: Colors.primaryLight,
    borderRadius: 12,
    padding: Spacing.lg,
    alignItems: 'center',
    marginTop: Spacing.md,
    marginBottom: Spacing.md,
  },
  countText: {
    marginBottom: Spacing.md,
  },
  encouragementContainer: {
    paddingVertical: Spacing.xxxl,
    paddingHorizontal: Spacing.lg,
  },
  encouragementText: {
    marginTop: Spacing.sm,
  },
  backBtn: {
    marginTop: Spacing.xxl,
    marginBottom: Spacing.lg,
  },
});

export default QualificationResultsScreen;
