import React from 'react';
import {View, StyleSheet} from 'react-native';
import {AppText} from './AppText';
import {Spacing} from '../common/theme/spacing';

interface SectionHeadingProps {
  title: string;
}

export const SectionHeading: React.FC<SectionHeadingProps> = ({title}) => {
  return (
    <View style={styles.container}>
      <AppText variant="subheading">{title}</AppText>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: Spacing.md,
    marginTop: Spacing.lg,
  },
});
