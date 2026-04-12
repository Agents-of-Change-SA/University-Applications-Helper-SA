import React from 'react';
import {StyleSheet} from 'react-native';
import {AppCard} from '../../../components/AppCard';
import {AppText} from '../../../components/AppText';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';

interface TutorCardProps {
  name: string;
  subject: string;
  contact: string;
}

export const TutorCard: React.FC<TutorCardProps> = ({name, subject, contact}) => {
  return (
    <AppCard style={styles.card}>
      <AppText variant="subheading">{name}</AppText>
      <AppText variant="label" color={Colors.primary} style={styles.subject}>
        {subject}
      </AppText>
      <AppText variant="caption" color={Colors.textSecondary}>
        {contact}
      </AppText>
    </AppCard>
  );
};

const styles = StyleSheet.create({
  card: {
    marginBottom: Spacing.md,
  },
  subject: {
    marginTop: Spacing.xxs,
    marginBottom: Spacing.xxs,
  },
});
