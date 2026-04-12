import React from 'react';
import {StyleSheet} from 'react-native';
import {AppCard} from '../../../components/AppCard';
import {AppText} from '../../../components/AppText';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';

interface RecommendationCardProps {
  subject: string;
  explanation: string;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  subject,
  explanation,
}) => {
  return (
    <AppCard style={styles.card}>
      <AppText variant="subheading">{subject}</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.explanation}>
        {explanation}
      </AppText>
    </AppCard>
  );
};

const styles = StyleSheet.create({
  card: {
    marginBottom: Spacing.md,
  },
  explanation: {
    marginTop: Spacing.xs,
  },
});
