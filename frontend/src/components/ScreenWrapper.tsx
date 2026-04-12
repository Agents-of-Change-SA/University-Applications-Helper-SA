import React from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  View,
  StyleProp,
  ViewStyle,
} from 'react-native';
import {Colors} from '../common/theme/colors';
import {Spacing} from '../common/theme/spacing';

interface ScreenWrapperProps {
  children: React.ReactNode;
  scrollable?: boolean;
  padding?: number;
  style?: StyleProp<ViewStyle>;
}

export const ScreenWrapper: React.FC<ScreenWrapperProps> = ({
  children,
  scrollable = true,
  padding = Spacing.lg,
  style,
}) => {
  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar barStyle="dark-content" backgroundColor={Colors.background} />
      {scrollable ? (
        <ScrollView
          style={styles.flex}
          contentContainerStyle={[{padding}, style]}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}>
          {children}
        </ScrollView>
      ) : (
        <View style={[styles.flex, {padding}, style]}>{children}</View>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  flex: {
    flex: 1,
  },
});
