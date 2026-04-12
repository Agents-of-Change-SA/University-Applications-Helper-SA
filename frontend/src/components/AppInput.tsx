import React from 'react';
import {View, TextInput, TextInputProps, StyleSheet, StyleProp, ViewStyle} from 'react-native';
import {AppText} from './AppText';
import {Colors} from '../common/theme/colors';
import {FontSize} from '../common/theme/typography';
import {Spacing} from '../common/theme/spacing';

interface AppInputProps extends TextInputProps {
  label: string;
  error?: string;
  required?: boolean;
  containerStyle?: StyleProp<ViewStyle>;
}

export const AppInput: React.FC<AppInputProps> = ({
  label,
  error,
  required = false,
  containerStyle,
  style,
  ...rest
}) => {
  return (
    <View style={[styles.container, containerStyle]}>
      <AppText variant="label" style={styles.label}>
        {label}
        {required && <AppText color={Colors.error}> *</AppText>}
      </AppText>
      <TextInput
        style={[styles.input, error ? styles.inputError : undefined, style]}
        placeholderTextColor={Colors.textDisabled}
        accessibilityLabel={label}
        accessibilityState={{disabled: rest.editable === false}}
        {...rest}
      />
      {error ? (
        <AppText variant="caption" color={Colors.error} style={styles.error}>
          {error}
        </AppText>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: Spacing.lg,
  },
  label: {
    marginBottom: Spacing.xs,
  },
  input: {
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: 10,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.md,
    fontSize: FontSize.md,
    color: Colors.textPrimary,
    backgroundColor: Colors.white,
    minHeight: 48,
  },
  inputError: {
    borderColor: Colors.error,
  },
  error: {
    marginTop: Spacing.xs,
  },
});
