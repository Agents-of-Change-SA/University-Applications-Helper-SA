import React, {useState} from 'react';
import {View, StyleSheet} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppInput} from '../../../components/AppInput';
import {AppButton} from '../../../components/AppButton';
import {AppDropdown} from '../../../components/AppDropdown';
import {SectionHeading} from '../../../components/SectionHeading';
import {QuickActionCard} from '../components/QuickActionCard';
import {ROUTES} from '../../../common/constants/routes';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';

type HomeNavProp = NativeStackNavigationProp<Record<string, undefined>>;

const FILTER_OPTIONS = [
  {label: 'All', value: 'all'},
  {label: 'Courses', value: 'courses'},
  {label: 'Tutors', value: 'tutors'},
  {label: 'Careers', value: 'careers'},
];

const HomeScreen: React.FC = () => {
  const navigation = useNavigation<HomeNavProp>();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterValue, setFilterValue] = useState('all');

  const navigateToCourses = () => {
    navigation.getParent()?.navigate('CoursesTab');
  };

  const navigateToCareerGuidance = () => {
    navigation.navigate(ROUTES.CareerGuidance);
  };

  const navigateToTutors = () => {
    navigation.getParent()?.navigate('TutorsTab');
  };

  return (
    <ScreenWrapper>
      <AppText variant="heading">Welcome to Univice</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        Your guide to higher education in South Africa
      </AppText>

      {/* Search bar placeholder */}
      <AppInput
        label="Search"
        placeholder="Search courses, tutors, careers..."
        value={searchQuery}
        onChangeText={setSearchQuery}
        containerStyle={styles.searchContainer}
      />

      {/* Filter dropdown placeholder */}
      <AppDropdown
        label="Filter"
        options={FILTER_OPTIONS}
        selectedValue={filterValue}
        onValueChange={setFilterValue}
      />

      {/* Check Courses CTA */}
      <AppButton
        title="Check Courses"
        onPress={navigateToCourses}
        style={styles.ctaButton}
      />

      {/* Quick Actions */}
      <SectionHeading title="Quick Actions" />
      <View style={styles.quickActions}>
        <QuickActionCard
          title="Find Courses"
          icon="🎓"
          onPress={navigateToCourses}
        />
        <View style={styles.quickActionGap} />
        <QuickActionCard
          title="Career Guidance"
          icon="🧭"
          onPress={navigateToCareerGuidance}
        />
        <View style={styles.quickActionGap} />
        <QuickActionCard
          title="Find Tutors"
          icon="👩‍🏫"
          onPress={navigateToTutors}
        />
      </View>
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {
    marginTop: Spacing.xs,
    marginBottom: Spacing.xl,
  },
  searchContainer: {
    marginBottom: Spacing.sm,
  },
  ctaButton: {
    marginTop: Spacing.sm,
    marginBottom: Spacing.sm,
  },
  quickActions: {
    flexDirection: 'row',
  },
  quickActionGap: {
    width: Spacing.sm,
  },
});

export default HomeScreen;
