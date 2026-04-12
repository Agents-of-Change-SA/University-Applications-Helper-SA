import React from 'react';
import {View, StyleSheet} from 'react-native';
import {AppText} from '../../../components/AppText';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';

interface StatusBadgeProps {
  status: 'Open' | 'Closed';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({status}) => {
  const isOpen = status === 'Open';

  return (
    <View
      style={[styles.badge, isOpen ? styles.open : styles.closed]}
      accessibilityRole="text"
      accessibilityLabel={`Application status: ${status}`}>
      <AppText
        variant="caption"
        color={isOpen ? Colors.success : Colors.textSecondary}
        style={styles.text}>
        {status}
      </AppText>
    </View>
  );
};

const styles = StyleSheet.create({
  badge: {
    alignSelf: 'flex-start',
    paddingHorizontal: Spacing.sm,
    paddingVertical: Spacing.xxs,
    borderRadius: 12,
  },
  open: {
    backgroundColor: Colors.successLight,
  },
  closed: {
    backgroundColor: Colors.divider,
  },
  text: {
    fontWeight: '600',
  },
});
