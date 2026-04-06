import React, {useState} from 'react';
import {View, StyleSheet} from 'react-native';
import {useForm, Controller} from 'react-hook-form';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';
import {useNavigation} from '@react-navigation/native';
import {AppText} from '../../../components/AppText';
import {AppInput} from '../../../components/AppInput';
import {AppButton} from '../../../components/AppButton';
import {ScreenWrapper} from '../../../components/ScreenWrapper';
import {useAuth} from '../../../context/AuthContext';
import {validationRules} from '../../../common/utils/validation';
import {ROUTES} from '../../../common/constants/routes';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import {AuthStackParamList} from '../../../navigation/AuthStack';

interface ForgotPasswordFormData {
  email: string;
}

type ForgotPwdNavProp = NativeStackNavigationProp<AuthStackParamList>;

const ForgotPasswordScreen: React.FC = () => {
  const navigation = useNavigation<ForgotPwdNavProp>();
  const {forgotPassword, isLoading} = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const {control, handleSubmit, formState: {errors}} = useForm<ForgotPasswordFormData>({
    defaultValues: {email: ''},
  });

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setError(null);
    setSuccess(false);
    try {
      await forgotPassword(data.email);
      setSuccess(true);
    } catch (e: any) {
      setError(e.message || 'Failed to send reset email. Please try again.');
    }
  };

  return (
    <ScreenWrapper>
      <View style={styles.container}>
        <AppText variant="heading" center style={styles.title}>
          Forgot Password
        </AppText>
        <AppText variant="body" center color={Colors.textSecondary} style={styles.subtitle}>
          Enter your email to receive a reset code
        </AppText>

        {error && (
          <AppText variant="caption" color={Colors.error} center style={styles.message}>
            {error}
          </AppText>
        )}

        {success && (
          <AppText variant="caption" color={Colors.success} center style={styles.message}>
            A reset code has been sent to your email.
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

        <AppButton
          title="Send Reset Code"
          onPress={handleSubmit(onSubmit)}
          loading={isLoading}
          style={styles.submitBtn}
        />

        {success && (
          <AppButton
            title="Enter Reset Code"
            variant="secondary"
            onPress={() => navigation.navigate(ROUTES.ResetPassword)}
            style={styles.resetBtn}
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
  resetBtn: {
    marginTop: Spacing.md,
  },
  linkBtn: {
    marginTop: Spacing.xl,
    alignSelf: 'center',
  },
});

export default ForgotPasswordScreen;
