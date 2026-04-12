import React from 'react';
import {Alert, Linking, StyleSheet, View} from 'react-native';
import {AppCard} from '../../../components/AppCard';
import {AppText} from '../../../components/AppText';
import {AppButton} from '../../../components/AppButton';
import {StatusBadge} from './StatusBadge';
import {formatDate, formatFee, getApplicationStatus} from '../utils/formatters';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import {ApplicationEntry} from '../../../api/types';

interface ApplicationEntryCardProps {
  entry: ApplicationEntry;
  currentDate?: Date;
}

export const ApplicationEntryCard: React.FC<ApplicationEntryCardProps> = ({
  entry,
  currentDate,
}) => {
  const status = getApplicationStatus(entry.openDate, entry.closeDate, currentDate);

  const handleApply = async () => {
    try {
      await Linking.openURL(entry.portalUrl);
    } catch {
      Alert.alert('Error', 'Unable to open application portal.');
    }
  };

  return (
    <AppCard style={styles.card}>
      <View style={styles.header}>
        <AppText variant="subheading" style={styles.institutionName}>
          {entry.institutionName}
        </AppText>
        <StatusBadge status={status} />
      </View>
      <AppText variant="body" color={Colors.textSecondary} style={styles.dates}>
        Opens: {formatDate(entry.openDate)}
      </AppText>
      <AppText variant="body" color={Colors.textSecondary}>
        Closes: {formatDate(entry.closeDate)}
      </AppText>
      <AppText variant="label" color={Colors.primary} style={styles.fee}>
        Fee: {formatFee(entry.applicationFee)}
      </AppText>
      <AppButton
        title="Apply"
        variant="secondary"
        compact
        onPress={handleApply}
        style={styles.applyButton}
        accessibilityLabel={`Apply to ${entry.institutionName}`}
      />
    </AppCard>
  );
};

const styles = StyleSheet.create({
  card: {
    marginBottom: Spacing.md,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  institutionName: {
    flex: 1,
    marginRight: Spacing.sm,
  },
  dates: {
    marginTop: Spacing.sm,
  },
  fee: {
    marginTop: Spacing.sm,
  },
  applyButton: {
    marginTop: Spacing.md,
    alignSelf: 'flex-start',
  },
});
