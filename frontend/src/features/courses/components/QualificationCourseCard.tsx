import React, {useState} from 'react';
import {StyleSheet, TouchableOpacity, View} from 'react-native';
import {AppCard} from '../../../components/AppCard';
import {AppText} from '../../../components/AppText';
import {Colors} from '../../../common/theme/colors';
import {Spacing} from '../../../common/theme/spacing';
import {ExtendedCourse, SchoolSubject} from '../../../api/types';

interface QualificationCourseCardProps {
  course: ExtendedCourse;
  learnerSubjects: SchoolSubject[];
  learnerAPS: number;
}

export const QualificationCourseCard: React.FC<QualificationCourseCardProps> = ({
  course,
  learnerSubjects,
  learnerAPS,
}) => {
  const [expanded, setExpanded] = useState(false);

  const findLearnerMark = (subjectName: string): number | null => {
    const match = learnerSubjects.find(
      s => s.name.toLowerCase() === subjectName.toLowerCase(),
    );
    return match ? match.percentage : null;
  };

  return (
    <AppCard style={styles.card}>
      <TouchableOpacity
        onPress={() => setExpanded(!expanded)}
        accessibilityRole="button"
        accessibilityLabel={`${course.courseName}, tap to ${expanded ? 'collapse' : 'expand'} details`}
        activeOpacity={0.7}>
        <AppText variant="subheading">{course.courseName}</AppText>
        <AppText
          variant="body"
          color={Colors.textSecondary}
          style={styles.institution}>
          {course.institution}
        </AppText>
        <AppText variant="label" color={Colors.primary} style={styles.aps}>
          Minimum APS: {course.minimumAPS}
        </AppText>

        {course.subjectRequirements.map((req, index) => (
          <AppText
            key={index}
            variant="caption"
            color={Colors.textSecondary}
            style={styles.requirement}>
            {req.subjectName}: {req.minimumPercentage}%
          </AppText>
        ))}

        <AppText variant="caption" color={Colors.primary} style={styles.toggle}>
          {expanded ? 'Hide details ▲' : 'View details ▼'}
        </AppText>
      </TouchableOpacity>

      {expanded && (
        <View style={styles.detailsSection}>
          <View style={styles.divider} />
          <AppText variant="label" style={styles.comparisonTitle}>
            Your Marks vs Requirements
          </AppText>
          <View style={styles.headerRow}>
            <AppText variant="caption" bold style={styles.subjectCol}>
              Subject
            </AppText>
            <AppText variant="caption" bold style={styles.markCol}>
              Required
            </AppText>
            <AppText variant="caption" bold style={styles.markCol}>
              Yours
            </AppText>
          </View>
          {course.subjectRequirements.map((req, index) => {
            const learnerMark = findLearnerMark(req.subjectName);
            const meetsRequirement =
              learnerMark !== null && learnerMark >= req.minimumPercentage;

            return (
              <View key={index} style={styles.comparisonRow}>
                <AppText variant="caption" style={styles.subjectCol}>
                  {req.subjectName}
                </AppText>
                <AppText variant="caption" style={styles.markCol}>
                  {req.minimumPercentage}%
                </AppText>
                <AppText
                  variant="caption"
                  color={
                    learnerMark === null
                      ? Colors.error
                      : meetsRequirement
                        ? Colors.success
                        : Colors.error
                  }
                  style={styles.markCol}>
                  {learnerMark !== null ? `${learnerMark}%` : 'N/A'}
                </AppText>
              </View>
            );
          })}
          <View style={styles.apsComparisonRow}>
            <AppText variant="caption" bold style={styles.subjectCol}>
              APS
            </AppText>
            <AppText variant="caption" bold style={styles.markCol}>
              {course.minimumAPS}
            </AppText>
            <AppText
              variant="caption"
              bold
              color={
                learnerAPS >= course.minimumAPS ? Colors.success : Colors.error
              }
              style={styles.markCol}>
              {learnerAPS}
            </AppText>
          </View>
        </View>
      )}
    </AppCard>
  );
};


const styles = StyleSheet.create({
  card: {
    marginBottom: Spacing.md,
  },
  institution: {
    marginTop: Spacing.xxs,
  },
  aps: {
    marginTop: Spacing.sm,
  },
  requirement: {
    marginTop: Spacing.xs,
  },
  toggle: {
    marginTop: Spacing.sm,
  },
  detailsSection: {
    marginTop: Spacing.sm,
  },
  divider: {
    height: 1,
    backgroundColor: Colors.divider,
    marginBottom: Spacing.sm,
  },
  comparisonTitle: {
    marginBottom: Spacing.sm,
  },
  headerRow: {
    flexDirection: 'row',
    marginBottom: Spacing.xs,
  },
  comparisonRow: {
    flexDirection: 'row',
    paddingVertical: Spacing.xs,
    borderBottomWidth: 1,
    borderBottomColor: Colors.divider,
  },
  apsComparisonRow: {
    flexDirection: 'row',
    paddingVertical: Spacing.sm,
    marginTop: Spacing.xs,
  },
  subjectCol: {
    flex: 2,
  },
  markCol: {
    flex: 1,
    textAlign: 'right',
  },
});
