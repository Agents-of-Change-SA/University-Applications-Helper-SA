import React, {useState} from 'react';
import {FlatList, StyleSheet} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppInput} from '../../../components/AppInput';
import {AppButton} from '../../../components/AppButton';
import {LoadingState} from '../../../components/LoadingState';
import {ErrorState} from '../../../components/ErrorState';
import {EmptyState} from '../../../components/EmptyState';
import {SectionHeading} from '../../../components/SectionHeading';
import {RecommendationCard} from '../components/RecommendationCard';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import CareerGuidanceService from '../../../api/careerGuidanceService';
import {SubjectRecommendation} from '../../../api/types';

const CareerGuidanceScreen: React.FC = () => {
  const navigation = useNavigation();
  const [aspiration, setAspiration] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'error' | 'success'>('idle');
  const [results, setResults] = useState<SubjectRecommendation[]>([]);
  const [errorMsg, setErrorMsg] = useState('');

  const fetchGuidance = async () => {
    if (!aspiration.trim()) return;
    setStatus('loading');
    try {
      const response = await CareerGuidanceService.getGuidance(aspiration.trim());
      setResults(response.recommendations);
      setStatus('success');
    } catch {
      setErrorMsg('Failed to get career guidance');
      setStatus('error');
    }
  };

  if (status === 'loading') {
    return <LoadingState message="Getting recommendations..." />;
  }

  return (
    <ScreenWrapper scrollable={false}>
      <AppText variant="heading">Career Guidance</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        Enter your career aspiration to get subject recommendations
      </AppText>

      <AppInput
        label="Career Aspiration"
        placeholder="e.g. Software Engineer, Doctor, Lawyer"
        value={aspiration}
        onChangeText={setAspiration}
      />
      <AppButton title="Get Recommendations" onPress={fetchGuidance} style={styles.submitBtn} />

      {status === 'error' && (
        <ErrorState message={errorMsg} onRetry={fetchGuidance} />
      )}

      {status === 'success' && results.length === 0 && (
        <EmptyState message="No recommendations found for this aspiration. Try a different career." />
      )}

      {status === 'success' && results.length > 0 && (
        <>
          <SectionHeading title="Recommended Subjects" />
          <FlatList
            data={results}
            keyExtractor={(_, i) => String(i)}
            renderItem={({item}) => (
              <RecommendationCard subject={item.subject} explanation={item.explanation} />
            )}
            style={styles.list}
          />
        </>
      )}

      <AppButton title="Back" variant="link" onPress={() => navigation.goBack()} style={styles.backBtn} />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.xl},
  submitBtn: {marginBottom: Spacing.lg},
  list: {flex: 1},
  backBtn: {marginTop: Spacing.md},
});

export default CareerGuidanceScreen;
