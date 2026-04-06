import React from 'react';
import {StyleSheet} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppButton} from '../../../components/AppButton';
import {SectionHeading} from '../../../components/SectionHeading';
import {ProfileSummary} from '../components/ProfileSummary';
import {useAuth} from '../../../context/AuthContext';
import {ROUTES} from '../../../common/constants/routes';
import {Spacing} from '../../../common/theme/spacing';

type ProfileNavProp = NativeStackNavigationProp<Record<string, undefined>>;

const ProfileScreen: React.FC = () => {
  const navigation = useNavigation<ProfileNavProp>();
  const {user, logout} = useAuth();

  return (
    <ScreenWrapper>
      <ProfileSummary
        name={user?.name ?? 'Learner'}
        email={user?.email ?? ''}
      />

      <SectionHeading title="My Account" />

      <AppButton
        title="User Details"
        variant="secondary"
        onPress={() => navigation.navigate(ROUTES.UserDetails)}
        style={styles.navButton}
      />
      <AppButton
        title="School Profile"
        variant="secondary"
        onPress={() => navigation.navigate(ROUTES.SchoolProfile)}
        style={styles.navButton}
      />
      <AppButton
        title="Career Aspirations"
        variant="secondary"
        onPress={() => navigation.navigate(ROUTES.CareerAspirations)}
        style={styles.navButton}
      />

      <AppButton
        title="Sign Out"
        variant="link"
        onPress={logout}
        style={styles.signOut}
      />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  navButton: {
    marginBottom: Spacing.md,
  },
  signOut: {
    marginTop: Spacing.xl,
    alignSelf: 'center',
  },
});

export default ProfileScreen;
