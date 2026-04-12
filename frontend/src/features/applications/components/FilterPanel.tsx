import React, {useState, useEffect, useRef, useCallback} from 'react';
import {View, StyleSheet} from 'react-native';
import {AppInput} from '../../../components/AppInput';
import {AppButton} from '../../../components/AppButton';
import {AppText} from '../../../components/AppText';
import {ApplicationDatesRequest} from '../../../api/types';
import {Spacing} from '../../../common/theme/spacing';

interface FilterPanelProps {
  filters: ApplicationDatesRequest;
  onFiltersChange: (filters: ApplicationDatesRequest) => void;
  onClear: () => void;
}

export const FilterPanel: React.FC<FilterPanelProps> = ({
  filters,
  onFiltersChange,
  onClear,
}) => {
  const [institutionText, setInstitutionText] = useState(
    filters.institutionName ?? '',
  );
  const debounceTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    setInstitutionText(filters.institutionName ?? '');
  }, [filters.institutionName]);

  const handleInstitutionChange = useCallback(
    (text: string) => {
      setInstitutionText(text);
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
      debounceTimer.current = setTimeout(() => {
        onFiltersChange({...filters, institutionName: text || undefined});
      }, 300);
    },
    [filters, onFiltersChange],
  );

  useEffect(() => {
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, []);

  const handleFilterChange = useCallback(
    (field: keyof ApplicationDatesRequest, value: string) => {
      if (field === 'minFee' || field === 'maxFee') {
        const parsed = parseFloat(value);
        onFiltersChange({
          ...filters,
          [field]: isNaN(parsed) ? undefined : parsed,
        });
      } else {
        onFiltersChange({...filters, [field]: value || undefined});
      }
    },
    [filters, onFiltersChange],
  );

  return (
    <View style={styles.container}>
      <AppInput
        label="Institution Name"
        placeholder="Search by institution name"
        value={institutionText}
        onChangeText={handleInstitutionChange}
        accessibilityHint="Filter by institution name"
      />

      <AppText variant="label" style={styles.sectionLabel}>
        Open Date Range
      </AppText>
      <AppInput
        label="From"
        placeholder="YYYY-MM-DD"
        value={filters.openDateFrom ?? ''}
        onChangeText={text => handleFilterChange('openDateFrom', text)}
      />
      <AppInput
        label="To"
        placeholder="YYYY-MM-DD"
        value={filters.openDateTo ?? ''}
        onChangeText={text => handleFilterChange('openDateTo', text)}
      />

      <AppText variant="label" style={styles.sectionLabel}>
        Close Date Range
      </AppText>
      <AppInput
        label="From"
        placeholder="YYYY-MM-DD"
        value={filters.closeDateFrom ?? ''}
        onChangeText={text => handleFilterChange('closeDateFrom', text)}
      />
      <AppInput
        label="To"
        placeholder="YYYY-MM-DD"
        value={filters.closeDateTo ?? ''}
        onChangeText={text => handleFilterChange('closeDateTo', text)}
      />

      <AppText variant="label" style={styles.sectionLabel}>
        Application Fee Range
      </AppText>
      <AppInput
        label="Min Fee"
        placeholder="0"
        value={filters.minFee !== undefined ? String(filters.minFee) : ''}
        onChangeText={text => handleFilterChange('minFee', text)}
        keyboardType="numeric"
      />
      <AppInput
        label="Max Fee"
        placeholder="300"
        value={filters.maxFee !== undefined ? String(filters.maxFee) : ''}
        onChangeText={text => handleFilterChange('maxFee', text)}
        keyboardType="numeric"
      />

      <AppButton
        title="Clear Filters"
        variant="secondary"
        onPress={onClear}
        style={styles.clearButton}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: Spacing.lg,
  },
  sectionLabel: {
    marginBottom: Spacing.sm,
    marginTop: Spacing.sm,
  },
  clearButton: {
    marginTop: Spacing.sm,
  },
});
