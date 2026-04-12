import React from 'react';
import {StyleSheet} from 'react-native';
import {AppCard} from '../../../components/AppCard';
import {AppText} from '../../../components/AppText';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';

interface CourseCardProps {
  courseName: string;
  institution: string;
  apsSummary: string;
  requirements: string;
}

export const CourseCard: React.FC<CourseCardProps> = ({
  courseName,
  institution,
  apsSummary,
  requirements,
}) => {
  return (
    <AppCard style={styles.card}>
      <AppText variant="subheading">{courseName}</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.institution}>
        {institution}
      </AppText>
      <AppText variant="label" color={Colors.primary} style={styles.aps}>
        {apsSummary}
      </AppText>
      <AppText variant="caption" color={Colors.textSecondary}>
        {requirements}
      </AppText>
    </AppCard>
  );
};

const styles = StyleSheet.create({
  card: {
    marginBottom: Spacing.md,
  },
  institution: {
    marginTop: Spacing.xxs,
  },
  aps: {
    marginTop: Spacing.sm,
  },
});
