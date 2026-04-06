import React from 'react';
import {View, StyleSheet} from 'react-native';
import {AppText} from './AppText';
import {Colors} from '../common/theme/colors';
import {Spacing} from '../common/theme/spacing';

interface EmptyStateProps {
  message: string;
  icon?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({message, icon}) => {
  return (
    <View style={styles.container}>
      {icon ? <View style={styles.icon}>{icon}</View> : null}
      <AppText variant="body" color={Colors.textSecondary} center>
        {message}
      </AppText>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.xl,
  },
  icon: {
    marginBottom: Spacing.md,
  },
});
