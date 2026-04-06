import React from 'react';
import {FlatList, StyleSheet} from 'react-native';
import {useNavigation, useRoute, RouteProp} from '@react-navigation/native';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppButton} from '../../../components/AppButton';
import {EmptyState} from '../../../components/EmptyState';
import {SectionHeading} from '../../../components/SectionHeading';
import {CourseCard} from '../components/CourseCard';
import {ROUTES} from '../../../common/constants/routes';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import type {CourseStackParamList} from '../../../navigation/MainTabNavigator';

type ResultsRoute = RouteProp<CourseStackParamList, typeof ROUTES.CourseResults>;

const CourseResultsScreen: React.FC = () => {
  const navigation = useNavigation();
  const route = useRoute<ResultsRoute>();
  const {topResult, results} = route.params;

  if (results.length === 0) {
    return (
      <ScreenWrapper>
        <EmptyState message="No matching courses found. Update your school profile and try again." />
        <AppButton title="Back" variant="link" onPress={() => navigation.goBack()} />
      </ScreenWrapper>
    );
  }

  return (
    <ScreenWrapper scrollable={false}>
      <AppText variant="heading">Course Results</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        {results.length} course{results.length !== 1 ? 's' : ''} found
      </AppText>

      {topResult && (
        <>
          <SectionHeading title="Top Match" />
          <CourseCard
            courseName={topResult.courseName}
            institution={topResult.institution}
            apsSummary={topResult.apsSummary}
            requirements={topResult.requirements}
          />
        </>
      )}

      <SectionHeading title="All Results" />
      <FlatList
        data={results}
        keyExtractor={item => item.id}
        renderItem={({item}) => (
          <CourseCard
            courseName={item.courseName}
            institution={item.institution}
            apsSummary={item.apsSummary}
            requirements={item.requirements}
          />
        )}
        style={styles.list}
      />

      <AppButton title="Back" variant="link" onPress={() => navigation.goBack()} style={styles.backBtn} />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.lg},
  list: {flex: 1},
  backBtn: {marginTop: Spacing.md},
});

export default CourseResultsScreen;
