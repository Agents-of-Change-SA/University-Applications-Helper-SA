import React from 'react';
import {
  TouchableOpacity,
  TouchableOpacityProps,
  ActivityIndicator,
  StyleSheet,
  StyleProp,
  TextStyle,
} from 'react-native';
import {AppText} from './AppText';
import {Colors} from '../common/theme/colors';
import {Spacing} from '../common/theme/spacing';

interface AppButtonProps extends TouchableOpacityProps {
  title: string;
  variant?: 'primary' | 'secondary' | 'link';
  loading?: boolean;
  compact?: boolean;
  textStyle?: StyleProp<TextStyle>;
}

export const AppButton: React.FC<AppButtonProps> = ({
  title,
  variant = 'primary',
  loading = false,
  compact = false,
  textStyle,
  disabled,
  style,
  ...rest
}) => {
  const isDisabled = disabled || loading;

  return (
    <TouchableOpacity
      style={[
        styles.base,
        compact && styles.compact,
        variant === 'primary' && styles.primary,
        variant === 'secondary' && styles.secondary,
        variant === 'link' && styles.link,
        isDisabled && styles.disabled,
        style,
      ]}
      disabled={isDisabled}
      accessibilityRole="button"
      accessibilityState={{disabled: isDisabled, busy: loading}}
      {...rest}>
      {loading ? (
        <ActivityIndicator
          color={variant === 'primary' ? Colors.white : Colors.primary}
          size="small"
        />
      ) : (
        <AppText
          variant="label"
          style={[
            variant === 'primary' && styles.primaryText,
            variant === 'secondary' && styles.secondaryText,
            variant === 'link' && styles.linkText,
            textStyle,
          ]}>
          {title}
        </AppText>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  base: {
    borderRadius: 10,
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.xl,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 48,
  },
  compact: {
    paddingVertical: Spacing.sm,
    paddingHorizontal: Spacing.lg,
    minHeight: 36,
  },
  primary: {
    backgroundColor: Colors.primary,
  },
  secondary: {
    backgroundColor: Colors.transparent,
    borderWidth: 1,
    borderColor: Colors.primary,
  },
  link: {
    backgroundColor: Colors.transparent,
    paddingHorizontal: 0,
    minHeight: 0,
  },
  disabled: {
    opacity: 0.5,
  },
  primaryText: {
    color: Colors.textInverse,
  },
  secondaryText: {
    color: Colors.primary,
  },
  linkText: {
    color: Colors.primary,
  },
});
