import React, {useState} from 'react';
import {View, StyleSheet} from 'react-native';
import {useForm, Controller} from 'react-hook-form';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';
import {useNavigation} from '@react-navigation/native';
import {AppText} from '../../../components/AppText';
import {AppInput} from '../../../components/AppInput';
import {AppButton} from '../../../components/AppButton';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import AuthService from '../../../api/authService';
import {validationRules} from '../../../common/utils/validation';
import {ROUTES} from '../../../common/constants/routes';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import {AuthStackParamList} from '../../../navigation/AuthStack';

interface ResetPasswordFormData {
  email: string;
  code: string;
  newPassword: string;
}

type ResetPwdNavProp = NativeStackNavigationProp<AuthStackParamList>;

const ResetPasswordScreen: React.FC = () => {
  const navigation = useNavigation<ResetPwdNavProp>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const {control, handleSubmit, formState: {errors}} = useForm<ResetPasswordFormData>({
    defaultValues: {email: '', code: '', newPassword: ''},
  });

  const onSubmit = async (data: ResetPasswordFormData) => {
    setError(null);
    setSuccess(false);
    setLoading(true);
    try {
      await AuthService.resetPassword({
        email: data.email,
        code: data.code,
        newPassword: data.newPassword,
      });
      setSuccess(true);
    } catch (e: any) {
      setError(e.message || 'Failed to reset password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScreenWrapper>
      <View style={styles.container}>
        <AppText variant="heading" center style={styles.title}>
          Reset Password
        </AppText>
        <AppText variant="body" center color={Colors.textSecondary} style={styles.subtitle}>
          Enter the code sent to your email and your new password
        </AppText>

        {error && (
          <AppText variant="caption" color={Colors.error} center style={styles.message}>
            {error}
          </AppText>
        )}

        {success && (
          <AppText variant="caption" color={Colors.success} center style={styles.message}>
            Password reset successfully.
          </AppText>
        )}

        <Controller
          control={control}
          name="email"
          rules={validationRules.email()}
          render={({field: {onChange, onBlur, value}}) => (
            <AppInput
              label="Email"
              required
              placeholder="Enter your email"
              keyboardType="email-address"
              autoCapitalize="none"
              onBlur={onBlur}
              onChangeText={onChange}
              value={value}
              error={errors.email?.message}
            />
          )}
        />

        <Controller
          control={control}
          name="code"
          rules={validationRules.required('Reset code')}
          render={({field: {onChange, onBlur, value}}) => (
            <AppInput
              label="Reset Code"
              required
              placeholder="Enter the code from your email"
              autoCapitalize="none"
              onBlur={onBlur}
              onChangeText={onChange}
              value={value}
              error={errors.code?.message}
            />
          )}
        />

        <Controller
          control={control}
          name="newPassword"
          rules={validationRules.required('New password')}
          render={({field: {onChange, onBlur, value}}) => (
            <AppInput
              label="New Password"
              required
              placeholder="Enter your new password"
              secureTextEntry
              onBlur={onBlur}
              onChangeText={onChange}
              value={value}
              error={errors.newPassword?.message}
            />
          )}
        />

        <AppButton
          title="Reset Password"
          onPress={handleSubmit(onSubmit)}
          loading={loading}
          style={styles.submitBtn}
        />

        {success && (
          <AppButton
            title="Back to Sign In"
            variant="secondary"
            onPress={() => navigation.navigate(ROUTES.Login)}
            style={styles.loginBtn}
          />
        )}

        <AppButton
          title="Back to Sign In"
          variant="link"
          onPress={() => navigation.navigate(ROUTES.Login)}
          style={styles.linkBtn}
        />
      </View>
    </ScreenWrapper>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: Spacing.lg,
  },
  title: {
    marginBottom: Spacing.sm,
  },
  subtitle: {
    marginBottom: Spacing.xxl,
  },
  message: {
    marginBottom: Spacing.lg,
  },
  submitBtn: {
    marginTop: Spacing.sm,
  },
  loginBtn: {
    marginTop: Spacing.md,
  },
  linkBtn: {
    marginTop: Spacing.xl,
    alignSelf: 'center',
  },
});

export default ResetPasswordScreen;
