"""
Quality Assessment Utility for API Response Validation

Implements scoring logic for HTTP 402 API responses based on:
- Completeness (40% weight)
- Freshness (30% weight)
- Schema compliance (30% weight)
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dateutil import parser as date_parser
import logging

logger = logging.getLogger(__name__)


class QualityAssessment:
    """Assess quality of API response data"""

    def __init__(self):
        self.weights = {
            "completeness": 0.40,
            "freshness": 0.30,
            "schema_compliance": 0.30
        }

    def assess(
        self,
        data: Any,
        expected_criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess data quality based on criteria

        Args:
            data: API response data
            expected_criteria: Quality requirements
                - min_records: Minimum number of records expected
                - required_fields: List of required field names
                - max_age_days: Maximum age of data in days
                - schema: Expected JSON schema
                - custom_validation: Natural language rules

        Returns:
            {
                "quality_score": 0-100,
                "issues_found": [list of issues],
                "refund_percentage": 0-100,
                "assessment_details": {
                    "completeness": 0-100,
                    "freshness": 0-100,
                    "schema_compliance": 0-100
                }
            }
        """
        scores = {}
        issues = []

        # Assess completeness
        if "min_records" in expected_criteria or "required_fields" in expected_criteria:
            completeness, completeness_issues = self._assess_completeness(
                data, expected_criteria
            )
            scores["completeness"] = completeness
            issues.extend(completeness_issues)
        else:
            scores["completeness"] = 100  # Default if not assessed

        # Assess freshness
        if "max_age_days" in expected_criteria:
            freshness, freshness_issues = self._assess_freshness(
                data, expected_criteria["max_age_days"]
            )
            scores["freshness"] = freshness
            issues.extend(freshness_issues)
        else:
            scores["freshness"] = 100  # Default if not assessed

        # Assess schema compliance
        if "required_fields" in expected_criteria or "schema" in expected_criteria:
            compliance, compliance_issues = self._assess_schema_compliance(
                data, expected_criteria
            )
            scores["schema_compliance"] = compliance
            issues.extend(compliance_issues)
        else:
            scores["schema_compliance"] = 100  # Default if not assessed

        # Calculate weighted quality score
        quality_score = self._calculate_weighted_score(scores)

        # Calculate refund percentage
        refund_percentage = self._calculate_refund(quality_score)

        return {
            "quality_score": round(quality_score, 2),
            "issues_found": issues,
            "refund_percentage": refund_percentage,
            "assessment_details": {
                "completeness": round(scores["completeness"], 2),
                "freshness": round(scores["freshness"], 2),
                "schema_compliance": round(scores["schema_compliance"], 2)
            }
        }

    def _assess_completeness(
        self,
        data: Any,
        criteria: Dict[str, Any]
    ) -> tuple[float, List[str]]:
        """Assess data completeness (40% weight)"""
        score = 0
        issues = []

        # Check minimum number of records
        if "min_records" in criteria:
            min_records = criteria["min_records"]

            # Handle different data structures
            if isinstance(data, list):
                actual_records = len(data)
            elif isinstance(data, dict) and "data" in data:
                actual_records = len(data["data"]) if isinstance(data["data"], list) else 1
            elif isinstance(data, dict) and "results" in data:
                actual_records = len(data["results"]) if isinstance(data["results"], list) else 1
            else:
                actual_records = 1

            if actual_records < min_records:
                issues.append(
                    f"Incomplete data: Expected {min_records} records, got {actual_records}"
                )
                score = (actual_records / min_records) * 100
            else:
                score = 100

        # Check required fields presence
        if "required_fields" in criteria and isinstance(data, (dict, list)):
            required_fields = criteria["required_fields"]

            # For lists, check first item
            check_data = data[0] if isinstance(data, list) and len(data) > 0 else data

            if isinstance(check_data, dict):
                missing_fields = [
                    field for field in required_fields
                    if field not in check_data or check_data[field] is None
                ]

                if missing_fields:
                    issues.append(
                        f"Missing required fields: {', '.join(missing_fields)}"
                    )
                    field_score = ((len(required_fields) - len(missing_fields)) / len(required_fields)) * 100
                    score = max(score, field_score) if "min_records" in criteria else field_score
                else:
                    score = 100

        return max(score, 0), issues

    def _assess_freshness(
        self,
        data: Any,
        max_age_days: int
    ) -> tuple[float, List[str]]:
        """Assess data freshness (30% weight)"""
        score = 100
        issues = []

        try:
            # Try to find timestamp in data
            timestamp = self._extract_timestamp(data)

            if timestamp:
                # Parse timestamp
                if isinstance(timestamp, str):
                    data_time = date_parser.parse(timestamp)
                elif isinstance(timestamp, (int, float)):
                    # Assume Unix timestamp
                    data_time = datetime.fromtimestamp(timestamp)
                else:
                    data_time = timestamp

                # Calculate age
                age = datetime.now() - data_time.replace(tzinfo=None)
                age_days = age.days + (age.seconds / 86400)

                if age_days > max_age_days:
                    issues.append(
                        f"Stale data: {age_days:.1f} days old (max {max_age_days} days)"
                    )
                    # Exponential decay score
                    score = max(0, 100 * (1 - (age_days / (max_age_days * 2))))
                else:
                    # Linear score within acceptable range
                    score = 100 * (1 - (age_days / max_age_days))

            else:
                # No timestamp found - assume acceptable
                logger.warning("No timestamp found in data for freshness assessment")
                score = 50  # Neutral score
                issues.append("No timestamp found for freshness validation")

        except Exception as e:
            logger.error(f"Error assessing freshness: {e}")
            score = 50
            issues.append(f"Could not assess freshness: {str(e)}")

        return max(score, 0), issues

    def _assess_schema_compliance(
        self,
        data: Any,
        criteria: Dict[str, Any]
    ) -> tuple[float, List[str]]:
        """Assess schema compliance (30% weight)"""
        score = 100
        issues = []

        # Check required fields (if not already checked in completeness)
        if "required_fields" in criteria and isinstance(data, (dict, list)):
            required_fields = criteria["required_fields"]
            check_data = data[0] if isinstance(data, list) and len(data) > 0 else data

            if isinstance(check_data, dict):
                # Check field types and values
                for field in required_fields:
                    if field in check_data:
                        value = check_data[field]
                        # Check for null/empty values
                        if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
                            issues.append(f"Field '{field}' is null or empty")
                            score -= (100 / len(required_fields))

        # Check schema structure (basic validation)
        if "schema" in criteria:
            schema = criteria["schema"]
            schema_score, schema_issues = self._validate_schema(data, schema)
            score = min(score, schema_score)
            issues.extend(schema_issues)

        return max(score, 0), issues

    def _validate_schema(
        self,
        data: Any,
        schema: Dict[str, Any]
    ) -> tuple[float, List[str]]:
        """Basic JSON schema validation"""
        score = 100
        issues = []

        try:
            # Check type
            expected_type = schema.get("type")
            actual_type = type(data).__name__

            type_map = {
                "object": "dict",
                "array": "list",
                "string": "str",
                "number": "float",
                "integer": "int",
                "boolean": "bool"
            }

            if expected_type and type_map.get(expected_type) != actual_type:
                issues.append(
                    f"Type mismatch: Expected {expected_type}, got {actual_type}"
                )
                score -= 50

            # Check properties (for objects)
            if expected_type == "object" and isinstance(data, dict):
                properties = schema.get("properties", {})
                for prop, prop_schema in properties.items():
                    if prop not in data:
                        issues.append(f"Missing property: {prop}")
                        score -= (50 / len(properties))

        except Exception as e:
            logger.error(f"Schema validation error: {e}")
            issues.append(f"Schema validation failed: {str(e)}")
            score = 50

        return max(score, 0), issues

    def _extract_timestamp(self, data: Any) -> Optional[Any]:
        """Extract timestamp from data"""
        timestamp_fields = [
            "timestamp", "created_at", "updated_at", "date", "time",
            "createdAt", "updatedAt", "datetime", "last_updated"
        ]

        if isinstance(data, dict):
            for field in timestamp_fields:
                if field in data:
                    return data[field]
            # Check nested data
            if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                return self._extract_timestamp(data["data"][0])

        elif isinstance(data, list) and len(data) > 0:
            return self._extract_timestamp(data[0])

        return None

    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted average score"""
        total_score = 0
        for category, score in scores.items():
            weight = self.weights.get(category, 0)
            total_score += score * weight
        return min(max(total_score, 0), 100)

    def _calculate_refund(self, quality_score: float) -> int:
        """
        Calculate refund percentage based on quality score

        Refund logic:
        - Quality >= 80: 0% refund (good delivery)
        - Quality 50-79: Sliding scale (partial refund)
        - Quality < 50: 100% refund (failed delivery)
        """
        if quality_score >= 80:
            return 0
        elif quality_score >= 50:
            # Sliding scale: 0% at 80, 100% at 50
            return int((80 - quality_score) / 30 * 100)
        else:
            # Full refund for quality < 50
            return 100


# Singleton instance
_quality_assessor = None


def get_quality_assessor() -> QualityAssessment:
    """Get singleton quality assessor instance"""
    global _quality_assessor
    if _quality_assessor is None:
        _quality_assessor = QualityAssessment()
    return _quality_assessor
