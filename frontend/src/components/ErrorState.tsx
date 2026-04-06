import React from 'react';
import {View, StyleSheet} from 'react-native';
import {AppText} from './AppText';
import {AppButton} from './AppButton';
import {Colors} from '../common/theme/colors';
import {Spacing} from '../common/theme/spacing';

interface ErrorStateProps {
  message: string;
  onRetry: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({message, onRetry}) => {
  return (
    <View style={styles.container} accessibilityRole="alert">
      <AppText variant="body" color={Colors.error} center style={styles.message}>
        {message}
      </AppText>
      <AppButton title="Retry" variant="secondary" compact onPress={onRetry} />
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
    marginBottom: Spacing.lg,
  },
});
