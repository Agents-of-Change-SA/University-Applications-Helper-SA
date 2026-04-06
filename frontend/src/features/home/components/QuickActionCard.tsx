import React from 'react';
import {View, StyleSheet} from 'react-native';
import {AppCard} from '../../../components/AppCard';
import {AppText} from '../../../components/AppText';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';

interface QuickActionCardProps {
  title: string;
  icon?: string;
  onPress: () => void;
}

export const QuickActionCard: React.FC<QuickActionCardProps> = ({
  title,
  icon,
  onPress,
}) => {
  return (
    <AppCard onPress={onPress} style={styles.card}>
      <View style={styles.iconArea}>
        <AppText variant="heading" center>
          {icon ?? '📚'}
        </AppText>
      </View>
      <AppText variant="label" center>
        {title}
      </AppText>
    </AppCard>
  );
};

const styles = StyleSheet.create({
  card: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: Spacing.lg,
    paddingHorizontal: Spacing.sm,
  },
  iconArea: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: Colors.primaryLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: Spacing.sm,
  },
});
