import React, {useState, useEffect, useCallback} from 'react';
import {FlatList, StyleSheet} from 'react-native';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {LoadingState} from '../../../components/LoadingState';
import {ErrorState} from '../../../components/ErrorState';
import {EmptyState} from '../../../components/EmptyState';
import {TutorCard} from '../components/TutorCard';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import TutorService from '../../../api/tutorService';
import {Tutor} from '../../../api/types';

const TutorsScreen: React.FC = () => {
  const [status, setStatus] = useState<'loading' | 'error' | 'ready'>('loading');
  const [tutors, setTutors] = useState<Tutor[]>([]);
  const [errorMsg, setErrorMsg] = useState('');

  const loadTutors = useCallback(async () => {
    setStatus('loading');
    try {
      const data = await TutorService.getTutors();
      setTutors(data);
      setStatus('ready');
    } catch {
      setErrorMsg('Failed to load tutors');
      setStatus('error');
    }
  }, []);

  useEffect(() => {
    loadTutors();
  }, [loadTutors]);

  if (status === 'loading') {
    return <LoadingState message="Loading tutors..." />;
  }
  if (status === 'error') {
    return <ErrorState message={errorMsg} onRetry={loadTutors} />;
  }

  return (
    <ScreenWrapper scrollable={false}>
      <AppText variant="heading">Tutors</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        Find academic support for your subjects
      </AppText>

      {tutors.length === 0 ? (
        <EmptyState message="No tutors available at the moment." />
      ) : (
        <FlatList
          data={tutors}
          keyExtractor={item => item.id}
          renderItem={({item}) => (
            <TutorCard name={item.name} subject={item.subject} contact={item.contact} />
          )}
          style={styles.list}
        />
      )}
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.xl},
  list: {flex: 1},
});

export default TutorsScreen;
