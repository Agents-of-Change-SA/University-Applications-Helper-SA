import React, {useState} from 'react';
import {View, StyleSheet, Image} from 'react-native';
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

interface LoginFormData {
  email: string;
  password: string;
}

type LoginNavProp = NativeStackNavigationProp<AuthStackParamList>;

const LoginScreen: React.FC = () => {
  const navigation = useNavigation<LoginNavProp>();
  const {login, isLoading} = useAuth();
  const [error, setError] = useState<string | null>(null);

  const {control, handleSubmit, formState: {errors}} = useForm<LoginFormData>({
    defaultValues: {email: '', password: ''},
  });

  const onSubmit = async (data: LoginFormData) => {
    setError(null);
    try {
      await login(data.email, data.password);
    } catch (e: any) {
      setError(e.message || 'Login failed. Please try again.');
    }
  };

  return (
    <ScreenWrapper>
      <View style={styles.container}>
        <Image
          source={require('../../../../logo.png')}
          style={styles.logo}
          resizeMode="contain"
          accessibilityLabel="Univice logo"
        />
        <AppText variant="heading" center style={styles.title}>
          Welcome Back
        </AppText>
        <AppText variant="body" center color={Colors.textSecondary} style={styles.subtitle}>
          Sign in to continue
        </AppText>

        {error && (
          <AppText variant="caption" color={Colors.error} center style={styles.errorMsg}>
            {error}
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

        <AppButton
          title="Sign In"
          onPress={handleSubmit(onSubmit)}
          loading={isLoading}
          style={styles.submitBtn}
        />

        <AppButton
          title="Forgot Password?"
          variant="link"
          onPress={() => navigation.navigate(ROUTES.ForgotPassword)}
          style={styles.linkBtn}
        />

        <View style={styles.footer}>
          <AppText variant="body" color={Colors.textSecondary}>
            Don't have an account?{' '}
          </AppText>
          <AppButton
            title="Register"
            variant="link"
            onPress={() => navigation.navigate(ROUTES.Register)}
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
  logo: {
    width: 120,
    height: 120,
    alignSelf: 'center',
    marginBottom: Spacing.lg,
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
  linkBtn: {
    marginTop: Spacing.md,
    alignSelf: 'center',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: Spacing.xl,
  },
});

export default LoginScreen;
