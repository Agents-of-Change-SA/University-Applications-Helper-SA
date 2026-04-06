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

interface RegisterFormData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

type RegisterNavProp = NativeStackNavigationProp<AuthStackParamList>;

const RegisterScreen: React.FC = () => {
  const navigation = useNavigation<RegisterNavProp>();
  const {register, isLoading} = useAuth();
  const [error, setError] = useState<string | null>(null);

  const {control, handleSubmit, watch, formState: {errors}} = useForm<RegisterFormData>({
    defaultValues: {name: '', email: '', password: '', confirmPassword: ''},
  });

  const passwordValue = watch('password');

  const onSubmit = async (data: RegisterFormData) => {
    setError(null);
    try {
      await register(data.name, data.email, data.password);
    } catch (e: any) {
      setError(e.message || 'Registration failed. Please try again.');
    }
  };

  return (
    <ScreenWrapper>
      <View style={styles.container}>
        <AppText variant="heading" center style={styles.title}>
          Create Account
        </AppText>
        <AppText variant="body" center color={Colors.textSecondary} style={styles.subtitle}>
          Sign up to get started
        </AppText>

        {error && (
          <AppText variant="caption" color={Colors.error} center style={styles.errorMsg}>
            {error}
          </AppText>
        )}

        <Controller
          control={control}
          name="name"
          rules={validationRules.required('Name')}
          render={({field: {onChange, onBlur, value}}) => (
            <AppInput
              label="Name"
              required
              placeholder="Enter your name"
              autoCapitalize="words"
              onBlur={onBlur}
              onChangeText={onChange}
              value={value}
              error={errors.name?.message}
            />
          )}
        />

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
          name="password"
          rules={validationRules.required('Password')}
          render={({field: {onChange, onBlur, value}}) => (
            <AppInput
              label="Password"
              required
              placeholder="Enter your password"
              secureTextEntry
              onBlur={onBlur}
              onChangeText={onChange}
              value={value}
              error={errors.password?.message}
            />
          )}
        />

        <Controller
          control={control}
          name="confirmPassword"
          rules={validationRules.matchField('Passwords', passwordValue)}
          render={({field: {onChange, onBlur, value}}) => (
            <AppInput
              label="Confirm Password"
              required
              placeholder="Confirm your password"
              secureTextEntry
              onBlur={onBlur}
              onChangeText={onChange}
              value={value}
              error={errors.confirmPassword?.message}
            />
          )}
        />

        <AppButton
          title="Register"
          onPress={handleSubmit(onSubmit)}
          loading={isLoading}
          style={styles.submitBtn}
        />

        <View style={styles.footer}>
          <AppText variant="body" color={Colors.textSecondary}>
            Already have an account?{' '}
          </AppText>
          <AppButton
            title="Sign In"
            variant="link"
            onPress={() => navigation.navigate(ROUTES.Login)}
          />
        </View>
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
  errorMsg: {
    marginBottom: Spacing.lg,
  },
  submitBtn: {
    marginTop: Spacing.sm,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: Spacing.xl,
  },
});

export default RegisterScreen;
