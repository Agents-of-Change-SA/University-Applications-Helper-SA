import React, {useState, useEffect, useCallback} from 'react';
import {StyleSheet} from 'react-native';
import {useForm, Controller, useFieldArray} from 'react-hook-form';
import {useNavigation} from '@react-navigation/native';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppInput} from '../../../components/AppInput';
import {AppButton} from '../../../components/AppButton';
import {LoadingState} from '../../../components/LoadingState';
import {ErrorState} from '../../../components/ErrorState';
import {SubjectRow} from '../components/SubjectRow';
import SchoolProfileService from '../../../api/schoolProfileService';
import {Spacing} from '../../../common/theme/spacing';
import {Colors} from '../../../common/theme/colors';

interface SubjectField {
  name: string;
  percentage: string;
  level: string;
}

interface FormData {
  schoolName: string;
  subjects: SubjectField[];
}

const SchoolProfileScreen: React.FC = () => {
  const navigation = useNavigation();
  const [status, setStatus] = useState<'loading' | 'error' | 'ready' | 'success'>('loading');
  const [errorMsg, setErrorMsg] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const {control, handleSubmit, reset, formState: {errors}} = useForm<FormData>({
    defaultValues: {schoolName: '', subjects: []},
  });

  const {fields, append, remove} = useFieldArray({control, name: 'subjects'});

  const loadProfile = useCallback(async () => {
    setStatus('loading');
    try {
      const profile = await SchoolProfileService.getSchoolProfile();
      reset({
        schoolName: profile.schoolName,
        subjects: profile.subjects.map(s => ({
          name: s.name,
          percentage: String(s.percentage),
          level: String(s.level),
        })),
      });
      setStatus('ready');
    } catch {
      setStatus('error');
      setErrorMsg('Failed to load school profile');
    }
  }, [reset]);

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const onSubmit = async (data: FormData) => {
    setSubmitting(true);
    try {
      await SchoolProfileService.saveSchoolProfile({
        name: data.schoolName,
        subjects: data.subjects.map(s => ({
          name: s.name,
          percentage: Number(s.percentage),
          level: Number(s.level),
        })),
      });
      setStatus('success');
    } catch {
      setErrorMsg('Failed to save school profile');
    } finally {
      setSubmitting(false);
    }
  };

  if (status === 'loading') {
    return <LoadingState message="Loading school profile..." />;
  }
  if (status === 'error') {
    return <ErrorState message={errorMsg} onRetry={loadProfile} />;
  }

  return (
    <ScreenWrapper>
      <AppText variant="heading">School Profile</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        Manage your school and subjects
      </AppText>

      {status === 'success' && (
        <AppText variant="body" color={Colors.success} style={styles.successMsg}>
          Profile saved successfully
        </AppText>
      )}

      <Controller
        control={control}
        name="schoolName"
        rules={{
          required: 'School name is required',
          validate: (v: string) => v.trim().length > 0 || 'School name is required',
        }}
        render={({field: {onChange, onBlur, value}}) => (
          <AppInput label="School Name" required value={value} onChangeText={onChange} onBlur={onBlur} error={errors.schoolName?.message} />
        )}
      />

      {fields.map((field, index) => (
        <Controller
          key={field.id}
          control={control}
          name={`subjects.${index}`}
          rules={{
            validate: (val: SubjectField) => {
              if (!val.name || !val.name.trim()) return 'Subject name is required';
              const pct = Number(val.percentage);
              if (isNaN(pct)) return 'Percentage must be a number';
              if (pct < 0 || pct > 100) return 'Percentage must be between 0 and 100';
              const lvl = Number(val.level);
              if (isNaN(lvl) || !Number.isInteger(lvl) || lvl <= 0) return 'Level must be a positive integer';
              return true;
            },
          }}
          render={({field: {value, onChange}}) => (
            <SubjectRow
              index={index}
              name={value.name}
              percentage={value.percentage}
              level={value.level}
              nameError={errors.subjects?.[index]?.message && !value.name.trim() ? 'Subject name is required' : undefined}
              percentageError={errors.subjects?.[index]?.message && (isNaN(Number(value.percentage)) || Number(value.percentage) < 0 || Number(value.percentage) > 100) ? errors.subjects[index]?.message : undefined}
              levelError={errors.subjects?.[index]?.message && (isNaN(Number(value.level)) || Number(value.level) <= 0) ? errors.subjects[index]?.message : undefined}
              onChangeName={v => onChange({...value, name: v})}
              onChangePercentage={v => onChange({...value, percentage: v})}
              onChangeLevel={v => onChange({...value, level: v})}
              onRemove={() => remove(index)}
            />
          )}
        />
      ))}

      <AppButton
        title="Add Subject"
        variant="secondary"
        onPress={() => append({name: '', percentage: '', level: ''})}
        style={styles.addBtn}
      />

      <AppButton title="Save Profile" onPress={handleSubmit(onSubmit)} loading={submitting} style={styles.saveBtn} />
      <AppButton title="Back" variant="link" onPress={() => navigation.goBack()} />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.xl},
  successMsg: {marginBottom: Spacing.lg},
  addBtn: {marginBottom: Spacing.lg},
  saveBtn: {marginTop: Spacing.md, marginBottom: Spacing.md},
});

export default SchoolProfileScreen;
