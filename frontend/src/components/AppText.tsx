import React from 'react';
import {Text, TextProps, StyleSheet} from 'react-native';
import {Colors} from '../common/theme/colors';
import {FontSize, FontWeight, LineHeight} from '../common/theme/typography';

interface AppTextProps extends TextProps {
  variant?: 'heading' | 'subheading' | 'body' | 'caption' | 'label';
  color?: string;
  center?: boolean;
  bold?: boolean;
}

export const AppText: React.FC<AppTextProps> = ({
  variant = 'body',
  color,
  center = false,
  bold = false,
  style,
  children,
  ...rest
}) => {
  return (
    <Text
      style={[
        styles[variant],
        center && styles.center,
        bold && styles.bold,
        color ? {color} : undefined,
        style,
      ]}
      accessibilityRole="text"
      {...rest}>
      {children}
    </Text>
  );
};

const styles = StyleSheet.create({
  heading: {
    fontSize: FontSize.xxl,
    fontWeight: FontWeight.bold,
    lineHeight: LineHeight.xxl,
    color: Colors.textPrimary,
  },
  subheading: {
    fontSize: FontSize.lg,
    fontWeight: FontWeight.semiBold,
    lineHeight: LineHeight.lg,
    color: Colors.textPrimary,
  },
  body: {
    fontSize: FontSize.md,
    fontWeight: FontWeight.regular,
    lineHeight: LineHeight.md,
    color: Colors.textPrimary,
  },
  caption: {
    fontSize: FontSize.xs,
    fontWeight: FontWeight.regular,
    lineHeight: LineHeight.xs,
    color: Colors.textSecondary,
  },
  label: {
    fontSize: FontSize.sm,
    fontWeight: FontWeight.medium,
    lineHeight: LineHeight.sm,
    color: Colors.textPrimary,
  },
  center: {
    textAlign: 'center',
  },
  bold: {
    fontWeight: FontWeight.bold,
  },
});
