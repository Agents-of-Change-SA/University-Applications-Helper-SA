import React from 'react';
import {View, TouchableOpacity, StyleSheet} from 'react-native';
import {AppInput} from '../../../components/AppInput';
import {AppText} from '../../../components/AppText';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';

interface SubjectRowProps {
  index: number;
  name: string;
  percentage: string;
  level: string;
  nameError?: string;
  percentageError?: string;
  levelError?: string;
  onChangeName: (val: string) => void;
  onChangePercentage: (val: string) => void;
  onChangeLevel: (val: string) => void;
  onRemove: () => void;
}

export const SubjectRow: React.FC<SubjectRowProps> = ({
  index,
  name,
  percentage,
  level,
  nameError,
  percentageError,
  levelError,
  onChangeName,
  onChangePercentage,
  onChangeLevel,
  onRemove,
}) => {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <AppText variant="label">Subject {index + 1}</AppText>
        <TouchableOpacity onPress={onRemove} accessibilityRole="button" accessibilityLabel={`Remove subject ${index + 1}`}>
          <AppText color={Colors.error}>Remove</AppText>
        </TouchableOpacity>
      </View>
      <AppInput label="Subject Name" required value={name} onChangeText={onChangeName} error={nameError} />
      <View style={styles.row}>
        <View style={styles.halfField}>
          <AppInput label="Percentage" required value={percentage} onChangeText={onChangePercentage} keyboardType="numeric" error={percentageError} />
        </View>
        <View style={styles.gap} />
        <View style={styles.halfField}>
          <AppInput label="Level" required value={level} onChangeText={onChangeLevel} keyboardType="numeric" error={levelError} />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: Spacing.lg,
    marginBottom: Spacing.md,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: Spacing.md,
  },
  row: {
    flexDirection: 'row',
  },
  halfField: {
    flex: 1,
  },
  gap: {
    width: Spacing.sm,
  },
});
