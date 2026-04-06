import React, {useState} from 'react';
import {
  View,
  TouchableOpacity,
  FlatList,
  Modal,
  StyleSheet,
} from 'react-native';
import {AppText} from './AppText';
import {Colors} from '../common/theme/colors';
import {Spacing} from '../common/theme/spacing';

interface DropdownOption {
  label: string;
  value: string;
}

interface AppDropdownProps {
  label: string;
  options: DropdownOption[];
  selectedValue?: string;
  onValueChange: (value: string) => void;
  error?: string;
}

export const AppDropdown: React.FC<AppDropdownProps> = ({
  label,
  options,
  selectedValue,
  onValueChange,
  error,
}) => {
  const [visible, setVisible] = useState(false);
  const selectedLabel = options.find(o => o.value === selectedValue)?.label;

  return (
    <View style={styles.container}>
      <AppText variant="label" style={styles.label}>
        {label}
      </AppText>
      <TouchableOpacity
        style={[styles.selector, error ? styles.selectorError : undefined]}
        onPress={() => setVisible(true)}
        accessibilityRole="combobox"
        accessibilityLabel={label}>
        <AppText
          color={selectedLabel ? Colors.textPrimary : Colors.textDisabled}>
          {selectedLabel || 'Select...'}
        </AppText>
      </TouchableOpacity>
      {error ? (
        <AppText variant="caption" color={Colors.error} style={styles.error}>
          {error}
        </AppText>
      ) : null}
      <Modal visible={visible} transparent animationType="fade">
        <TouchableOpacity
          style={styles.overlay}
          activeOpacity={1}
          onPress={() => setVisible(false)}>
          <View style={styles.dropdown}>
            <FlatList
              data={options}
              keyExtractor={item => item.value}
              renderItem={({item}) => (
                <TouchableOpacity
                  style={[
                    styles.option,
                    item.value === selectedValue && styles.optionSelected,
                  ]}
                  onPress={() => {
                    onValueChange(item.value);
                    setVisible(false);
                  }}>
                  <AppText>{item.label}</AppText>
                </TouchableOpacity>
              )}
            />
          </View>
        </TouchableOpacity>
      </Modal>
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
  selector: {
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: 10,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.md,
    backgroundColor: Colors.white,
    minHeight: 48,
    justifyContent: 'center',
  },
  selectorError: {
    borderColor: Colors.error,
  },
  error: {
    marginTop: Spacing.xs,
  },
  overlay: {
    flex: 1,
    backgroundColor: Colors.overlay,
    justifyContent: 'center',
    paddingHorizontal: Spacing.xl,
  },
  dropdown: {
    backgroundColor: Colors.white,
    borderRadius: 12,
    maxHeight: 300,
    overflow: 'hidden',
  },
  option: {
    paddingVertical: Spacing.md,
    paddingHorizontal: Spacing.lg,
  },
  optionSelected: {
    backgroundColor: Colors.primaryLight,
  },
});
