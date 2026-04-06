import React from 'react';
import {View, StyleSheet} from 'react-native';
import {AppText} from '../../../components/AppText';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';

interface ProfileSummaryProps {
  name: string;
  email: string;
}

export const ProfileSummary: React.FC<ProfileSummaryProps> = ({name, email}) => {
  return (
    <View style={styles.container}>
      <View style={styles.avatar}>
        <AppText variant="heading" color={Colors.white} center>
          {name.charAt(0).toUpperCase()}
        </AppText>
      </View>
      <AppText variant="subheading" style={styles.name}>
        {name}
      </AppText>
      <AppText variant="body" color={Colors.textSecondary}>
        {email}
      </AppText>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingVertical: Spacing.xl,
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: Spacing.md,
  },
  name: {
    marginBottom: Spacing.xs,
  },
});
