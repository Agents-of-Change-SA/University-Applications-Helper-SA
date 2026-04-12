import React, {useState, useEffect, useCallback, useMemo} from 'react';
import {FlatList, StyleSheet} from 'react-native';
import {useRoute, RouteProp} from '@react-navigation/native';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {LoadingState} from '../../../components/LoadingState';
import {ErrorState} from '../../../components/ErrorState';
import {EmptyState} from '../../../components/EmptyState';
import {AppText} from '../../../components/AppText';
import {FilterPanel} from '../components/FilterPanel';
import {ApplicationEntryCard} from '../components/ApplicationEntryCard';
import ApplicationService from '../../../api/applicationService';
import {applyFilters, sortByStatus} from '../utils/filters';
import {ApplicationEntry, ApplicationDatesRequest} from '../../../api/types';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import {ROUTES} from '../../../common/constants/routes';

type ApplicationDatesRouteParams = {
  [ROUTES.ApplicationDates]: {institutionName?: string} | undefined;
};

const EMPTY_FILTERS: ApplicationDatesRequest = {};

const ApplicationDatesScreen: React.FC = () => {
  const route =
    useRoute<RouteProp<ApplicationDatesRouteParams, typeof ROUTES.ApplicationDates>>();
  const institutionParam = route.params?.institutionName;

  const [entries, setEntries] = useState<ApplicationEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<ApplicationDatesRequest>(() =>
    institutionParam ? {institutionName: institutionParam} : EMPTY_FILTERS,
  );

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await ApplicationService.getApplicationDates();
      setEntries(response.entries);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : 'Failed to load application dates.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const filteredAndSorted = useMemo(() => {
    const filtered = applyFilters(entries, filters);
    return sortByStatus(filtered);
  }, [entries, filters]);

  const hasActiveFilters = useMemo(() => {
    return Object.values(filters).some(
      v => v !== undefined && v !== '',
    );
  }, [filters]);

  const handleFiltersChange = useCallback(
    (newFilters: ApplicationDatesRequest) => {
      setFilters(newFilters);
    },
    [],
  );

  const handleClearFilters = useCallback(() => {
    setFilters(EMPTY_FILTERS);
  }, []);

  const renderItem = useCallback(
    ({item}: {item: ApplicationEntry}) => (
      <ApplicationEntryCard entry={item} />
    ),
    [],
  );

  const keyExtractor = useCallback(
    (item: ApplicationEntry) => item.id,
    [],
  );

  if (loading) {
    return (
      <ScreenWrapper>
        <LoadingState message="Loading application dates..." />
      </ScreenWrapper>
    );
  }

  if (error) {
    return (
      <ScreenWrapper>
        <ErrorState message={error} onRetry={fetchData} />
      </ScreenWrapper>
    );
  }

  if (entries.length === 0) {
    return (
      <ScreenWrapper>
        <EmptyState message="No application dates available." />
      </ScreenWrapper>
    );
  }

  return (
    <ScreenWrapper scrollable={false}>
      <AppText variant="heading" style={styles.title}>
        Application Dates
      </AppText>
      <AppText
        variant="body"
        color={Colors.textSecondary}
        style={styles.subtitle}>
        Browse and filter university application dates
      </AppText>

      <FlatList
        data={filteredAndSorted}
        renderItem={renderItem}
        keyExtractor={keyExtractor}
        ListHeaderComponent={
          <FilterPanel
            filters={filters}
            onFiltersChange={handleFiltersChange}
            onClear={handleClearFilters}
          />
        }
        ListEmptyComponent={
          hasActiveFilters ? (
            <EmptyState message="No applications match your current filters." />
          ) : (
            <EmptyState message="No application dates available." />
          )
        }
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  title: {
    marginBottom: Spacing.xs,
  },
  subtitle: {
    marginBottom: Spacing.md,
  },
  listContent: {
    flexGrow: 1,
  },
});

export default ApplicationDatesScreen;
