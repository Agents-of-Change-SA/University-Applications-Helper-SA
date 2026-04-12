import React, {useState, useEffect, useCallback} from 'react';
import {StyleSheet} from 'react-native';
import {useForm, Controller} from 'react-hook-form';
import {useNavigation} from '@react-navigation/native';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {AppText} from '../../../components/AppText';
import {AppInput} from '../../../components/AppInput';
import {AppButton} from '../../../components/AppButton';
import {LoadingState} from '../../../components/LoadingState';
import {ErrorState} from '../../../components/ErrorState';
import {validationRules} from '../../../common/utils/validation';
import {Spacing} from '../../../common/theme/spacing';
import {Colors} from '../../../common/theme/colors';
import UserDetailsService from '../../../api/userDetailsService';

interface FormData {
  name: string;
  surname: string;
  age: string;
  careerAspiration: string;
}

const UserDetailsScreen: React.FC = () => {
  const navigation = useNavigation();
  const [status, setStatus] = useState<'loading' | 'error' | 'ready' | 'success'>('loading');
  const [errorMsg, setErrorMsg] = useState('');
  const [isExisting, setIsExisting] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const {control, handleSubmit, reset, formState: {errors}} = useForm<FormData>({
    defaultValues: {name: '', surname: '', age: '', careerAspiration: ''},
  });

  const loadDetails = useCallback(async () => {
    setStatus('loading');
    try {
      const details = await UserDetailsService.getUserDetails();
      setIsExisting(true);
      reset({
        name: details.name,
        surname: details.surname,
        age: String(details.age),
        careerAspiration: details.careerAspiration ?? '',
      });
      setStatus('ready');
    } catch {
      setStatus('error');
      setErrorMsg('Failed to load user details');
    }
  }, [reset]);

  useEffect(() => {
    loadDetails();
  }, [loadDetails]);

  const onSubmit = async (data: FormData) => {
    setSubmitting(true);
    try {
      const payload = {
        name: data.name,
        surname: data.surname,
        age: Number(data.age),
        careerAspiration: data.careerAspiration || undefined,
      };
      if (isExisting) {
        await UserDetailsService.updateUserDetails(payload);
      } else {
        await UserDetailsService.createUserDetails(payload);
      }
      setStatus('success');
    } catch {
      setErrorMsg('Failed to save user details');
    } finally {
      setSubmitting(false);
    }
  };

  if (status === 'loading') {
    return <LoadingState message="Loading your details..." />;
  }
  if (status === 'error') {
    return <ErrorState message={errorMsg} onRetry={loadDetails} />;
  }

  return (
    <ScreenWrapper>
      <AppText variant="heading">User Details</AppText>
      <AppText variant="body" color={Colors.textSecondary} style={styles.subtitle}>
        {isExisting ? 'Update your personal information' : 'Tell us about yourself'}
      </AppText>

      {status === 'success' && (
        <AppText variant="body" color={Colors.success} style={styles.successMsg}>
          Details saved successfully
        </AppText>
      )}

      <Controller
        control={control}
        name="name"
        rules={validationRules.required('Name')}
        render={({field: {onChange, onBlur, value}}) => (
          <AppInput label="Name" required value={value} onChangeText={onChange} onBlur={onBlur} error={errors.name?.message} />
        )}
      />
      <Controller
        control={control}
        name="surname"
        rules={validationRules.required('Surname')}
        render={({field: {onChange, onBlur, value}}) => (
          <AppInput label="Surname" required value={value} onChangeText={onChange} onBlur={onBlur} error={errors.surname?.message} />
        )}
      />
      <Controller
        control={control}
        name="age"
        rules={validationRules.positiveInteger('Age')}
        render={({field: {onChange, onBlur, value}}) => (
          <AppInput label="Age" required value={value} onChangeText={onChange} onBlur={onBlur} keyboardType="numeric" error={errors.age?.message} />
        )}
      />
      <Controller
        control={control}
        name="careerAspiration"
        render={({field: {onChange, onBlur, value}}) => (
          <AppInput label="Career Aspiration (optional)" value={value} onChangeText={onChange} onBlur={onBlur} />
        )}
      />

      <AppButton title={isExisting ? 'Update' : 'Save'} onPress={handleSubmit(onSubmit)} loading={submitting} style={styles.saveBtn} />
      <AppButton title="Back" variant="link" onPress={() => navigation.goBack()} />
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  subtitle: {marginTop: Spacing.xs, marginBottom: Spacing.xl},
  successMsg: {marginBottom: Spacing.lg},
  saveBtn: {marginTop: Spacing.md, marginBottom: Spacing.md},
});

export default UserDetailsScreen;
