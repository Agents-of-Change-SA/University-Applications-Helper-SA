import React from 'react';
import {StyleSheet} from 'react-native';
import {useForm, Controller} from 'react-hook-form';
import {AppInput} from '../../../components/AppInput';
import {AppButton} from '../../../components/AppButton';
import {validationRules} from '../../../common/utils/validation';
import {Spacing} from '../../../common/theme/spacing';

interface AspirationFormProps {
  initialValue?: string;
  onSave: (aspiration: string) => void;
  onCancel: () => void;
  loading?: boolean;
}

interface FormData {
  aspiration: string;
}

export const AspirationForm: React.FC<AspirationFormProps> = ({
  initialValue = '',
  onSave,
  onCancel,
  loading = false,
}) => {
  const {control, handleSubmit, formState: {errors}} = useForm<FormData>({
    defaultValues: {aspiration: initialValue},
  });

  const onSubmit = (data: FormData) => onSave(data.aspiration.trim());

  return (
    <>
      <Controller
        control={control}
        name="aspiration"
        rules={validationRules.nonEmptyString('Aspiration')}
        render={({field: {onChange, onBlur, value}}) => (
          <AppInput
            label="Career Aspiration"
            required
            value={value}
            onChangeText={onChange}
            onBlur={onBlur}
            error={errors.aspiration?.message}
            placeholder="e.g. Software Engineer"
          />
        )}
      />
      <AppButton title="Save" onPress={handleSubmit(onSubmit)} loading={loading} style={styles.saveBtn} />
      <AppButton title="Cancel" variant="link" onPress={onCancel} />
    </>
  );
};

const styles = StyleSheet.create({
  saveBtn: {marginBottom: Spacing.sm},
});
