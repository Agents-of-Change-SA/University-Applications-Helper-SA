import React, {useState, useEffect, useCallback} from 'react';
import {FlatList, StyleSheet} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppButton} from '../../../components/AppButton';
import {AppCard} from '../../../components/AppCard';
import {LoadingState} from '../../../components/LoadingState';
import {ErrorState} from '../../../components/ErrorState';
import {EmptyState} from '../../../components/EmptyState';
import {AspirationForm} from '../components/AspirationForm';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import CareerAspirationsService from '../../../api/careerAspirationsService';
import {CareerAspiration} from '../../../api/types';

type Mode = 'list' | 'create' | 'edit';

const CareerAspirationsScreen: React.FC = () => {
  const navigation = useNavigation();
  const [status, setStatus] = useState<'loading' | 'error' | 'ready'>('loading');
  const [aspirations, setAspirations] = useState<CareerAspiration[]>([]);
  const [errorMsg, setErrorMsg] = useState('');
  const [mode, setMode] = useState<Mode>('list');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const loadAspirations = useCallback(async () => {
    setStatus('loading');
    try {
      const data = await CareerAspirationsService.getAspirations();
      setAspirations(data);
      setStatus('ready');
    } catch {
      setErrorMsg('Failed to load aspirations');
      setStatus('error');
    }
  }, []);

  useEffect(() => {
    loadAspirations();
  }, [loadAspirations]);

  const handleSave = async (text: string) => {
    setSaving(true);
    try {
      if (mode === 'edit' && editingId) {
        const updated = await CareerAspirationsService.updateAspiration(editingId, {aspiration: text});
        setAspirations(prev => prev.map(a => (a.id === editingId ? updated : a)));
      } else {
        const created = await CareerAspirationsService.createAspiration({aspiration: text});
        setAspirations(prev => [...prev, created]);
      }
      setMode('list');
      setEditingId(null);
    } catch {
      setErrorMsg('Failed to save aspiration');
    } finally {
      setSaving(false);
    }
  };

  if (status === 'loading') {
    return <LoadingState message="Loading aspirations..." />;
  }
  if (status === 'error') {
    return <ErrorState message={errorMsg} onRetry={loadAspirations} />;
  }

  if (mode === 'create' || mode === 'edit') {
    const initial = mode === 'edit' ? aspirations.find(a => a.id === editingId)?.aspiration : '';
    return (
      <ScreenWrapper>
        <AppText variant="heading">{mode === 'edit' ? 'Edit Aspiration' : 'New Aspiration'}</AppText>
        <AspirationForm
          initialValue={initial}
          onSave={handleSave}
          onCancel={() => { setMode('list'); setEditingId(null); }}
          loading={saving}
        />
      </ScreenWrapper>
    );
  }

  return (
    <ScreenWrapper scrollable={false}>
      <AppText variant="heading">Career Aspirations</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        Track and refine your career goals
      </AppText>

      {aspirations.length === 0 ? (
        <EmptyState message="No aspirations yet. Add your first career goal." />
      ) : (
        <FlatList
          data={aspirations}
          keyExtractor={item => item.id}
          renderItem={({item}) => (
            <AppCard onPress={() => { setEditingId(item.id); setMode('edit'); }} style={styles.card}>
              <AppText variant="subheading">{item.aspiration}</AppText>
              <AppText variant="caption" color={Colors.textSecondary}>
                Added {new Date(item.createdAt).toLocaleDateString()}
              </AppText>
            </AppCard>
          )}
          style={styles.list}
        />
      )}

      <AppButton title="Add Aspiration" onPress={() => setMode('create')} style={styles.addBtn} />
      <AppButton title="Back" variant="link" onPress={() => navigation.goBack()} />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.xl},
  card: {marginBottom: Spacing.md},
  list: {flex: 1},
  addBtn: {marginTop: Spacing.md, marginBottom: Spacing.md},
});

export default CareerAspirationsScreen;
