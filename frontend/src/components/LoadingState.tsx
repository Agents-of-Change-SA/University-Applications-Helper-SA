import React from 'react';
import {View, ActivityIndicator, StyleSheet} from 'react-native';
import {AppText} from './AppText';
import {Colors} from '../common/theme/colors';
import {Spacing} from '../common/theme/spacing';

interface LoadingStateProps {
  message?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({message}) => {
  return (
    <View style={styles.container} accessibilityRole="progressbar">
      <ActivityIndicator size="large" color={Colors.primary} />
      {message ? (
        <AppText variant="body" color={Colors.textSecondary} style={styles.message}>
          {message}
        </AppText>
      ) : null}
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
  message: {
    marginTop: Spacing.md,
    textAlign: 'center',
  },
});
