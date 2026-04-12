import React from 'react';
import {TouchableOpacity, View, StyleSheet, StyleProp, ViewStyle} from 'react-native';
import {Colors} from '../common/theme/colors';
import {Spacing} from '../common/theme/spacing';

interface AppCardProps {
  children: React.ReactNode;
  onPress?: () => void;
  style?: StyleProp<ViewStyle>;
}

export const AppCard: React.FC<AppCardProps> = ({children, onPress, style}) => {
  if (onPress) {
    return (
      <TouchableOpacity
        style={[styles.card, style]}
        onPress={onPress}
        accessibilityRole="button"
        activeOpacity={0.7}>
        {children}
      </TouchableOpacity>
    );
  }

  return <View style={[styles.card, style]}>{children}</View>;
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: Spacing.lg,
    shadowColor: Colors.textPrimary,
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 2,
  },
});
