from dataclasses import dataclass

from photometric_viewer.photometry.ies02.validation_issues import (
    Ies02BallastLampPhotometricFactorDeprecated,
    Ies02HAnglesTypeAFirstValueInvalid,
    Ies02HAnglesTypeALastValueInvalid,
    Ies02HAnglesTypeBFirstValueInvalid,
    Ies02HAnglesTypeBLastValueInvalid,
    Ies02HAnglesTypeCFirstValueInvalid,
    Ies02HAnglesTypeCLastValueInvalid,
    Ies02HAnglesValueNotNumber,
    Ies02HAnglesValueOutOfOrder,
    Ies02HeaderInvalid,
    Ies02HeaderNotFound,
    Ies02IntensityValueNegative,
    Ies02IntensityValueNotNumber,
    Ies02LampPositionNotNumbers,
    Ies02LampPositionHorizontalOutOfRange,
    Ies02LampPositionVerticalOutOfRange,
    Ies02LampPositionTwoValuesExpected,
    Ies02LuminousOpeningGeometryInvalid,
    Ies02MetadataFlashareaNotNumber,
    Ies02MetadataFlashareaNotPositive,
    Ies02MetadataFlashareaUnusualSize,
    Ies02MetadataKeyDeprecated,
    Ies02MetadataKeyDuplicate,
    Ies02MetadataKeyInvalidCharacters,
    Ies02MetadataKeyLeadingTrailingWhitespace,
    Ies02MetadataKeyMissing,
    Ies02MetadataKeyMissingRequired,
    Ies02MetadataKeyMissingSuggested,
    Ies02MetadataKeyNotUppercase,
    Ies02MetadataKeyTooLong,
    Ies02MetadataMaintcatInvalidValue,
    Ies02MetadataNearfieldInvalidValue,
    Ies02MetadataUserKeyWithoutUnderscore,
    Ies02MetadataValueMissing,
    Ies02NumberOfIntensitiesInvalid,
    Ies02VAnglesTypeAFirstValueInvalid,
    Ies02VAnglesTypeALastValueInvalid,
    Ies02VAnglesTypeBFirstValueInvalid,
    Ies02VAnglesTypeBLastValueInvalid,
    Ies02VAnglesTypeCFirstValueInvalid,
    Ies02VAnglesTypeCLastValueInvalid,
    Ies02VAnglesValueNotNumber,
    Ies02VAnglesValueOutOfOrder,
)
from photometric_viewer.photometry.ies91.validation_issues import (
    Ies91HAnglesTypeAFirstValueInvalid,
    Ies91HAnglesTypeALastValueInvalid,
    Ies91HAnglesTypeBFirstValueInvalid,
    Ies91HAnglesTypeBLastValueInvalid,
    Ies91HAnglesTypeCFirstValueInvalid,
    Ies91HAnglesTypeCLastValueInvalid,
    Ies91HeaderInvalid,
    Ies91LuminousOpeningGeometryInvalid,
    Ies91MetadataKeyMissingRequired,
)
from photometric_viewer.photometry.ies95.validation_issues import (
    Ies95BallastLampPhotometricFactorDeprecated,
    Ies95HAnglesTypeAFirstValueInvalid,
    Ies95HAnglesTypeALastValueInvalid,
    Ies95HAnglesTypeBFirstValueInvalid,
    Ies95HAnglesTypeBLastValueInvalid,
    Ies95HAnglesTypeCFirstValueInvalid,
    Ies95HAnglesTypeCLastValueInvalid,
    Ies95HeaderInvalid,
    Ies95LuminousOpeningGeometryInvalid,
    Ies95MetadataKeyMissingRecommended,
)
from photometric_viewer.photometry.iesna_common.validation_issues import (
    IesHAnglesTypeAFirstValueInvalid,
    IesHAnglesTypeALastValueInvalid,
    IesHAnglesTypeBFirstValueInvalid,
    IesHAnglesTypeBLastValueInvalid,
    IesHAnglesTypeCFirstValueInvalid,
    IesHAnglesTypeCLastValueInvalid,
    IesHAnglesValueNotNumber,
    IesHAnglesValueOutOfOrder,
    IesIntensityValueNegative,
    IesIntensityValueNotNumber,
    IesLampPositionNotNumbers,
    IesLampPositionOutOfRange,
    IesLampPositionTwoValuesExpected,
    IesLuminousOpeningGeometryInvalid,
    IesMetadataFlashareaNotNumber,
    IesMetadataFlashareaNotPositive,
    IesMetadataFlashareaUnusualSize,
    IesMetadataKeyDeprecated,
    IesMetadataKeyDuplicate,
    IesMetadataKeyInvalidCharacters,
    IesMetadataKeyLeadingTrailingWhitespace,
    IesMetadataKeyMissing,
    IesMetadataKeyMissingRequired,
    IesMetadataKeyNotUppercase,
    IesMetadataKeyTooLong,
    IesMetadataUserKeyWithoutUnderscore,
    IesMetadataMaintcatInvalidValue,
    IesMetadataNearfieldInvalidValue,
    IesMetadataValueMissing,
    IesNumberOfIntensitiesInvalid,
    IesVAnglesTypeAFirstValueInvalid,
    IesVAnglesTypeALastValueInvalid,
    IesVAnglesTypeBFirstValueInvalid,
    IesVAnglesTypeBLastValueInvalid,
    IesVAnglesTypeCFirstValueInvalid,
    IesVAnglesTypeCLastValueInvalid,
    IesVAnglesValueNotNumber,
    IesVAnglesValueOutOfOrder,
)
from photometric_viewer.photometry.ldt.validation_issues import (
    LdtLampSetAttributeInvalidValue,
    LdtLampSetAttributeMissingValue,
    LdtLampSetAttributeTooLong,
    LdtLampSetNumericAttributeOutOfRange,
)
from photometric_viewer.photometry.validation import (
    AttributeInvalidValue,
    AttributeMissingValue,
    AttributeTooLong,
    NumericAttributeOutOfRange,
    ValidationIssueBase,
)

@dataclass
class IssueTranslation:
    translation: str
    details: str | None


def get_translations(issue: ValidationIssueBase) -> IssueTranslation:
    ATTRIBUTE_NAMES = {
        'future_use': _('future use'),
        'ballast_lamp_photometric_factor': _('ballast-lamp photometric factor'),
        'lumens_per_lamp': _('lumens per lamp'),
        'multiplying_factor': _('multiplying factor'),
        'n_v_angles': _('number of vertical angles'),
        'n_h_angles': _('number of horizontal angles'),
        'photometry_type': _('photometry type'),
        'luminous_opening_units': _('luminous opening units'),
        'luminous_opening_width': _('luminous opening width'),
        'luminous_opening_length': _('luminous opening length'),
        'luminous_opening_height': _('luminous opening height'),
        'ballast_factor': _('ballast factor'),
        'input_watts': _('input watts'),
        'symmetry_indicator': _('symmetry indicator'),
        'distance_between_c_planes': _('distance between C planes'),
        'number_of_intensities': _('number of intensities'),
        'distance_between_intensities': _('distance between intensities'),
        'measurement_report': _('measurement report'),
        'luminaire_name': _('luminaire name'),
        'luminaire_number': _('luminaire number'),
        'file_name': _('file name'),
        'date_and_user': _('date and user'),
        'manufacturer': _('manufacturer'),
        'length_of_luminaire': _('length of luminaire'),
        'width_of_luminaire': _('width of luminaire'),
        'height_of_luminaire': _('height of luminaire'),
        'length_of_luminous_area': _('length of luminous area'),
        'width_of_luminous_area': _('width of luminous area'),
        'height_of_luminous_area_c0': _('height of luminous area C0'),
        'height_of_luminous_area_c90': _('height of luminous area C90'),
        'height_of_luminous_area_c180': _('height of luminous area C180'),
        'height_of_luminous_area_c270': _('height of luminous area C270'),
        'dff_percent': _('DFF percent'),
        'lor_percent': _('LOR percent'),
        'conversion_factor': _('conversion factor'),
        'tilt': _('tilt'),
        'number_of_lamp_sets': _('number of lamp sets'),
        'lamp_sets': _('lamp sets'),
        'direct_ratios_for_room_indices': _('direct ratios for room indices'),
        'number_of_c_planes': _('number of C planes'),
        'c_angles': _('C angles'),
        'gamma_angles': _('gamma angles'),
        'intensities': _('intensities'),
        'intensity': _('intensity'),
        'number_of_lamps': _('number of lamps'),
        'type_of_lamp': _('type of lamp'),
        'total_lumens': _('total lumens'),
        'light_color': _('light color'),
        'cri': _('CRI'),
        'wattage': _('wattage'),
        'type_indicator': _('type indicator'),
        "direct_ratio_1": _("direct ratio for room index k = 0.60"),
        "direct_ratio_2": _("direct ratio for room index k = 0.80"),
        "direct_ratio_3": _("direct ratio for room index k = 1.00"),
        "direct_ratio_4": _("direct ratio for room index k = 1.25"),
        "direct_ratio_5": _("direct ratio for room index k = 1.50"),
        "direct_ratio_6": _("direct ratio for room index k = 2.00"),
        "direct_ratio_7": _("direct ratio for room index k = 2.50"),
        "direct_ratio_8": _("direct ratio for room index k = 3.00"),
        "direct_ratio_9": _("direct ratio for room index k = 4.00"),
        "direct_ratio_10": _("direct ratio for room index k = 5.00"),
    }

    def _attr(attribute: str):
        return ATTRIBUTE_NAMES.get(attribute, attribute)

    match issue:
        case AttributeMissingValue():
            return IssueTranslation(
                _('Missing required value'),
                _('Value for {attribute} is empty').format_map({"attribute": _attr(issue.attribute)}),
            )
        case AttributeInvalidValue():
            return IssueTranslation(
                _('Attribute has invalid value'),
                _('Value {value} is not valid for attribute {attribute}').format_map(
                    {"attribute": _attr(issue.attribute), "value": issue.value}
                ),
            )
        case AttributeTooLong():
            return IssueTranslation(
                _('Value exceeds maximum length'),
                _('Value for {attribute} exceeds {max_length} characters').format_map(
                    {"attribute": _attr(issue.attribute), "max_length": issue.max_length}
                ),
            )
        case NumericAttributeOutOfRange():
            return IssueTranslation(
                _('Value is out of range'),
                _('{attribute} is outside the expected range: {value}').format_map(
                    {"attribute": _attr(issue.attribute), "value": issue.value}
                ),
            )
        case LdtLampSetAttributeMissingValue():
            return IssueTranslation(
                _('Missing lamp set value'),
                _('Value for {attribute} is empty in lamp set {lamp_set_number}').format_map(
                    {"attribute": _attr(issue.attribute), "lamp_set_number": issue.lamp_set_number}
                ),
            )
        case LdtLampSetAttributeInvalidValue():
            return IssueTranslation(
                _('Lamp set value is invalid'),
                _('Value {value} is not valid for {attribute} in lamp set {lamp_set_number}').format_map(
                    {
                        "attribute": _attr(issue.attribute),
                        "value": issue.value,
                        "lamp_set_number": issue.lamp_set_number,
                    }
                ),
            )
        case LdtLampSetAttributeTooLong():
            return IssueTranslation(
                _('Lamp set value exceeds maximum length'),
                _('Value for {attribute} exceeds {max_length} characters in lamp set {lamp_set_number}').format_map(
                    {
                        "attribute": _attr(issue.attribute),
                        "max_length": issue.max_length,
                        "lamp_set_number": issue.lamp_set_number,
                    }
                ),
            )
        case LdtLampSetNumericAttributeOutOfRange():
            return IssueTranslation(
                _('Lamp set value is out of range'),
                _('Value {value} for {attribute} in lamp set {lamp_set_number} is outside the expected range').format_map(
                    {
                        "attribute": _attr(issue.attribute),
                        "value": issue.value,
                        "lamp_set_number": issue.lamp_set_number,
                    }
                ),
            )
        case IesMetadataKeyMissing():
            return IssueTranslation(
                _('Metadata key missing'),
                _('Metadata key {key} is missing').format_map({"key": issue.metadata.key}),
            )
        case IesMetadataKeyLeadingTrailingWhitespace():
            return IssueTranslation(
                _('Metadata key has whitespace'),
                _('Metadata key {key} has leading or trailing whitespace').format_map({"key": issue.metadata.key}),
            )
        case IesMetadataValueMissing():
            return IssueTranslation(
                _('Metadata value missing'),
                _('Metadata value for {key} is empty').format_map({"key": issue.metadata.key}),
            )
        case IesMetadataKeyMissingRequired():
            return IssueTranslation(
                _('Required metadata missing'),
                _('Required metadata key {key} is missing').format_map({"key": issue.missing_key}),
            )
        case IesMetadataKeyDeprecated():
            return IssueTranslation(
                _('Deprecated metadata key'),
                _('Metadata key {key} is deprecated').format_map({"key": issue.key}),
            )
        case IesMetadataKeyInvalidCharacters():
            return IssueTranslation(
                _('Metadata key contains invalid characters'),
                _('Metadata key {key} contains invalid characters').format_map({"key": issue.metadata.key}),
            )
        case IesMetadataKeyNotUppercase():
            return IssueTranslation(
                _('Metadata key should be uppercase'),
                _('Metadata key {key} should use uppercase letters only').format_map({"key": issue.metadata.key}),
            )
        case IesMetadataKeyDuplicate():
            return IssueTranslation(
                _('Duplicate metadata key'),
                _('Metadata key {key} is duplicated').format_map({"key": issue.metadata.key}),
            )
        case IesMetadataKeyTooLong():
            return IssueTranslation(
                _('Metadata key is too long'),
                _('Metadata key {key} exceeds the maximum length of 20 characters').format_map({"key": issue.metadata.key}),
            )
        case IesMetadataUserKeyWithoutUnderscore():
            return IssueTranslation(
                _('Metadata key format is invalid'),
                _('User metadata key {key} should start with an underscore').format_map({"key": issue.metadata.key}),
            )
        case IesMetadataNearfieldInvalidValue():
            return IssueTranslation(
                _('Invalid NEARFIELD value'),
                _('NEARFIELD metadata value {value} is invalid').format_map({"value": issue.metadata.value}),
            )
        case IesMetadataMaintcatInvalidValue():
            return IssueTranslation(
                _('Invalid MAINTCAT value'),
                _('MAINTCAT metadata value {value} is invalid').format_map({"value": issue.metadata.value}),
            )
        case IesMetadataFlashareaNotNumber():
            return IssueTranslation(
                _('FLASHAREA is not numeric'),
                _('FLASHAREA metadata value {value} is not a number').format_map({"value": issue.metadata.value}),
            )
        case IesMetadataFlashareaNotPositive():
            return IssueTranslation(
                _('FLASHAREA must be positive'),
                _('FLASHAREA metadata value {value} must be positive').format_map({"value": issue.metadata.value}),
            )
        case IesMetadataFlashareaUnusualSize():
            return IssueTranslation(
                _('Unusual FLASHAREA value'),
                _('FLASHAREA metadata value {value} is unusually large or small').format_map({"value": issue.metadata.value}),
            )
        case IesLampPositionTwoValuesExpected():
            return IssueTranslation(
                _('LAMPPOSITION has invalid number of values'),
                _('LAMPPOSITION metadata value {value} does not contain two values').format_map({"value": issue.metadata.value}),
            )
        case IesLampPositionNotNumbers():
            return IssueTranslation(
                _('LAMPPOSITION must contain numbers'),
                _('LAMPPOSITION metadata value {value} does not contain valid numbers').format_map({"value": issue.metadata.value}),
            )
        case IesLampPositionOutOfRange():
            return IssueTranslation(
                _('LAMPPOSITION is out of range'),
                _('Given value {value} is out of range. First angle must be between 0.00 to 359.99 degrees. Second angle must be between 0.00 to 180.00 degrees.').format_map({"value": issue.metadata.value}),
            )
        case IesIntensityValueNotNumber():
            return IssueTranslation(
                _('Intensity value is not numeric'),
                _('Intensity value {value} is not a number').format_map({"value": issue.value}),
            )
        case IesIntensityValueNegative():
            return IssueTranslation(
                _('Intensity value is negative'),
                _('Intensity value {value} is negative').format_map({"value": issue.value}),
            )
        case IesVAnglesValueNotNumber():
            return IssueTranslation(
                _('Vertical angle value is invalid'),
                _('Vertical angle value {value} is not a number').format_map({"value": issue.value}),
            )
        case IesVAnglesValueOutOfOrder():
            return IssueTranslation(
                _('Vertical angles are out of order'),
                _('Value {value} is not in ascending order').format_map({"value": issue.value}),
            )
        case IesVAnglesTypeCFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first vertical angle'),
                _('Type C photometry first vertical angle is invalid: {value}. Expected 0 or 90.').format_map({"value": issue.value}),
            )
        case IesVAnglesTypeCLastValueInvalid():
            return IssueTranslation(
                _('Invalid last vertical angle'),
                _('Type C photometry last vertical angle is invalid: {value}. Expected 90 or 180.').format_map({"value": issue.value}),
            )
        case IesVAnglesTypeBFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first vertical angle'),
                _('Type B photometry first vertical angle is invalid: {value}. Expected -90 or 0.').format_map({"value": issue.value}),
            )
        case IesVAnglesTypeBLastValueInvalid():
            return IssueTranslation(
                _('Invalid last vertical angle'),
                _('Type B photometry last vertical angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case IesVAnglesTypeAFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first vertical angle'),
                _('Type A photometry first vertical angle is invalid: {value}. Expected -90 or 0.').format_map({"value": issue.value}),
            )
        case IesVAnglesTypeALastValueInvalid():
            return IssueTranslation(
                _('Invalid last vertical angle'),
                _('Type A photometry last vertical angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case IesHAnglesValueNotNumber():
            return IssueTranslation(
                _('Horizontal angle value is invalid'),
                _('Horizontal angle value {value} is not a number').format_map({"value": issue.value}),
            )
        case IesHAnglesValueOutOfOrder():
            return IssueTranslation(
                _('Horizontal angles are out of order'),
                _('Horizontal angles are not in ascending order: {value}').format_map({"value": issue.value}),
            )
        case IesHAnglesTypeCFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type C photometry first horizontal angle is invalid: {value}. Expected 0.').format_map({"value": issue.value}),
            )
        case IesHAnglesTypeCLastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type C photometry last horizontal angle is invalid: {value}. Expected 0, 90, 180, or 360.').format_map({"value": issue.value}),
            )
        case IesHAnglesTypeBFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type B photometry first horizontal angle is invalid: {value}. Expected 0 or -90.').format_map({"value": issue.value}),
            )
        case IesHAnglesTypeBLastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type B photometry last horizontal angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case IesHAnglesTypeAFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type A photometry first horizontal angle is invalid: {value}. Expected 0 or -90.').format_map({"value": issue.value}),
            )
        case IesHAnglesTypeALastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type A photometry last horizontal angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case IesLuminousOpeningGeometryInvalid():
            return IssueTranslation(
                _('Invalid luminous opening geometry'),
                _('Luminous opening geometry is invalid: width={width}, length={length}, height={height}').format_map(
                    {"width": issue.width, "length": issue.length, "height": issue.height}
                ),
            )
        case IesNumberOfIntensitiesInvalid():
            return IssueTranslation(
                _('Invalid number of intensities'),
                _('Expected {expected} intensity values, got {number}').format_map(
                    {"expected": issue.expected, "number": issue.number}
                ),
            )
        case Ies02HeaderNotFound():
            return IssueTranslation(
                _('Header not found'),
                _('IESNA:LM-63-2002 header was not found in the file'),
            )
        case Ies02HeaderInvalid():
            return IssueTranslation(
                _('Invalid header'),
                _('IESNA:LM-63-2002 header is invalid: {header}').format_map({"header": issue.header}),
            )
        case Ies02MetadataKeyMissing():
            return IssueTranslation(
                _('Metadata key missing'),
                _('Metadata key {key} is missing').format_map({"key": issue.metadata.key}),
            )
        case Ies02MetadataKeyLeadingTrailingWhitespace():
            return IssueTranslation(
                _('Metadata key has whitespace'),
                _('Metadata key {key} has leading or trailing whitespace').format_map({"key": issue.metadata.key}),
            )
        case Ies02MetadataValueMissing():
            return IssueTranslation(
                _('Metadata value missing'),
                _('Metadata value for {key} is empty').format_map({"key": issue.metadata.key}),
            )
        case Ies02MetadataKeyMissingRequired():
            return IssueTranslation(
                _('Required metadata missing'),
                _('Required metadata key {key} is missing').format_map({"key": issue.missing_key}),
            )
        case Ies02MetadataKeyMissingSuggested():
            return IssueTranslation(
                _('Suggested metadata missing'),
                _('Suggested metadata key {key} is missing').format_map({"key": issue.missing_key}),
            )
        case Ies02MetadataKeyDeprecated():
            return IssueTranslation(
                _('Deprecated metadata key'),
                _('Metadata key {key} is deprecated').format_map({"key": issue.key}),
            )
        case Ies02MetadataKeyInvalidCharacters():
            return IssueTranslation(
                _('Metadata key contains invalid characters'),
                _('Metadata key {key} contains invalid characters').format_map({"key": issue.metadata.key}),
            )
        case Ies02MetadataKeyNotUppercase():
            return IssueTranslation(
                _('Metadata key should be uppercase'),
                _('Metadata key {key} should use uppercase letters only').format_map({"key": issue.metadata.key}),
            )
        case Ies02MetadataKeyDuplicate():
            return IssueTranslation(
                _('Duplicate metadata key'),
                _('Metadata key {key} is duplicated').format_map({"key": issue.metadata.key}),
            )
        case Ies02MetadataKeyTooLong():
            return IssueTranslation(
                _('Metadata key is too long'),
                _('Metadata key {key} exceeds the maximum length').format_map({"key": issue.metadata.key}),
            )
        case Ies02MetadataUserKeyWithoutUnderscore():
            return IssueTranslation(
                _('Metadata key format is invalid'),
                _('User metadata key {key} should start with an underscore').format_map({"key": issue.metadata.key}),
            )
        case Ies02MetadataNearfieldInvalidValue():
            return IssueTranslation(
                _('Invalid NEARFIELD value'),
                _('NEARFIELD metadata value {value} is invalid').format_map({"value": issue.metadata.value}),
            )
        case Ies02MetadataMaintcatInvalidValue():
            return IssueTranslation(
                _('Invalid MAINTCAT value'),
                _('MAINTCAT metadata value {value} is invalid').format_map({"value": issue.metadata.value}),
            )
        case Ies02MetadataFlashareaNotNumber():
            return IssueTranslation(
                _('FLASHAREA is not numeric'),
                _('FLASHAREA metadata value {value} is not a number').format_map({"value": issue.metadata.value}),
            )
        case Ies02MetadataFlashareaNotPositive():
            return IssueTranslation(
                _('FLASHAREA must be positive'),
                _('FLASHAREA metadata value {value} must be positive').format_map({"value": issue.metadata.value}),
            )
        case Ies02MetadataFlashareaUnusualSize():
            return IssueTranslation(
                _('Unusual FLASHAREA value'),
                _('FLASHAREA metadata value {value} is unusually large or small').format_map({"value": issue.metadata.value}),
            )
        case Ies02LampPositionTwoValuesExpected():
            return IssueTranslation(
                _('LAMPPOSITION has invalid number of values'),
                _('LAMPPOSITION metadata value {value} does not contain two values').format_map({"value": issue.metadata.value}),
            )
        case Ies02LampPositionNotNumbers():
            return IssueTranslation(
                _('LAMPPOSITION must contain numbers'),
                _('LAMPPOSITION metadata value {value} does not contain valid numbers').format_map({"value": issue.metadata.value}),
            )
        case Ies02LampPositionHorizontalOutOfRange():
            return IssueTranslation(
                _('LAMPPOSITION is out of range'),
                _('Horizontal (first) value of LAMPPOSITION must be between 0.00 and 359.99 degrees. Given: {value}').format_map({"value": issue.value}),
            )
        case Ies02LampPositionVerticalOutOfRange():
            return IssueTranslation(
                _('LAMPPOSITION is out of range'),
                _('Vertical (second) value of LAMPPOSITION must be between 0.00 and 180.00 degrees. Given: {value}').format_map({"value": issue.value}),
            )
        case Ies02IntensityValueNotNumber():
            return IssueTranslation(
                _('Intensity value is not numeric'),
                _('Intensity value {value} is not a number').format_map({"value": issue.value}),
            )
        case Ies02IntensityValueNegative():
            return IssueTranslation(
                _('Intensity value is negative'),
                _('Intensity value {value} is negative').format_map({"value": issue.value}),
            )
        case Ies02VAnglesValueNotNumber():
            return IssueTranslation(
                _('Vertical angle value is invalid'),
                _('Vertical angle value {value} is not a number').format_map({"value": issue.value}),
            )
        case Ies02VAnglesValueOutOfOrder():
            return IssueTranslation(
                _('Vertical angles are out of order'),
                _('Vertical angles are not in ascending order: {value}').format_map({"value": issue.value}),
            )
        case Ies02VAnglesTypeCFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first vertical angle'),
                _('Type C photometry first vertical angle is invalid: {value}. Expected 0 or 90.').format_map({"value": issue.value}),
            )
        case Ies02VAnglesTypeCLastValueInvalid():
            return IssueTranslation(
                _('Invalid last vertical angle'),
                _('Type C photometry last vertical angle is invalid: {value}. Expected 90 or 180.').format_map({"value": issue.value}),
            )
        case Ies02VAnglesTypeBFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first vertical angle'),
                _('Type B photometry first vertical angle is invalid: {value}. Expected -90 or 0.').format_map({"value": issue.value}),
            )
        case Ies02VAnglesTypeBLastValueInvalid():
            return IssueTranslation(
                _('Invalid last vertical angle'),
                _('Type B photometry last vertical angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case Ies02VAnglesTypeAFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first vertical angle'),
                _('Type A photometry first vertical angle is invalid: {value}. Expected -90 or 0.').format_map({"value": issue.value}),
            )
        case Ies02VAnglesTypeALastValueInvalid():
            return IssueTranslation(
                _('Invalid last vertical angle'),
                _('Type A photometry last vertical angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case Ies02HAnglesValueNotNumber():
            return IssueTranslation(
                _('Horizontal angle value is invalid'),
                _('Horizontal angle value {value} is not a number').format_map({"value": issue.value}),
            )
        case Ies02HAnglesValueOutOfOrder():
            return IssueTranslation(
                _('Horizontal angles are out of order'),
                _('Horizontal angles are not in ascending order: {value}').format_map({"value": issue.value}),
            )
        case Ies02HAnglesTypeCFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type C photometry first horizontal angle is invalid: {value}. Expected 0.').format_map({"value": issue.value}),
            )
        case Ies02HAnglesTypeCLastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type C photometry last horizontal angle is invalid: {value}. Expected 0, 90, 180, or 360.').format_map({"value": issue.value}),
            )
        case Ies02HAnglesTypeBFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type B photometry first horizontal angle is invalid: {value}. Expected 0 or -90.').format_map({"value": issue.value}),
            )
        case Ies02HAnglesTypeBLastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type B photometry last horizontal angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case Ies02HAnglesTypeAFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type A photometry first horizontal angle is invalid: {value}. Expected 0 or -90.').format_map({"value": issue.value}),
            )
        case Ies02HAnglesTypeALastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type A photometry last horizontal angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case Ies02LuminousOpeningGeometryInvalid():
            return IssueTranslation(
                _('Invalid luminous opening geometry'),
                _('Luminous opening geometry is invalid: width={width}, length={length}, height={height}').format_map(
                    {"width": issue.width, "length": issue.length, "height": issue.height}
                ),
            )
        case Ies02NumberOfIntensitiesInvalid():
            return IssueTranslation(
                _('Invalid number of intensities'),
                _('Expected {expected} intensity values, got {number}').format_map(
                    {"expected": issue.expected, "number": issue.number}
                ),
            )
        case Ies02BallastLampPhotometricFactorDeprecated():
            return IssueTranslation(
                _('Deprecated ballast-lamp photometric factor'),
                _('Ballast-lamp photometric factor is deprecated. Use a value of 1.0 instead (given: {value})').format_map(
                    {"value": issue.value}
                ),
            )
        case Ies91HeaderInvalid():
            return IssueTranslation(
                _('Invalid header'),
                _('IESNA:LM-63-1991 header is invalid: {header}').format_map({"header": issue.header}),
            )
        case Ies91MetadataKeyMissingRequired():
            return IssueTranslation(
                _('Required metadata missing'),
                _('Required metadata key {key} is missing').format_map({"key": issue.key}),
            )
        case Ies91LuminousOpeningGeometryInvalid():
            return IssueTranslation(
                _('Invalid luminous opening geometry'),
                _('Luminous opening geometry is invalid: width={width}, length={length}, height={height}').format_map(
                    {"width": issue.width, "length": issue.length, "height": issue.height}
                ),
            )
        case Ies91HAnglesTypeCFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type C photometry first horizontal angle is invalid: {value}. Expected 0.').format_map({"value": issue.value}),
            )
        case Ies91HAnglesTypeCLastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type C photometry last horizontal angle is invalid: {value}. Expected {expected}').format_map(
                    {"value": issue.last_value, "expected": "90, 180, or 360." if issue.first_value == 0 else "270."}
                ),
            )
        case Ies91HAnglesTypeBFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type B photometry first horizontal angle is invalid: {value}. Expected 0 or -90.').format_map({"value": issue.value}),
            )
        case Ies91HAnglesTypeBLastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type B photometry last horizontal angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case Ies91HAnglesTypeAFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type A photometry first horizontal angle is invalid: {value}. Expected 0 or -90.').format_map({"value": issue.value}),
            )
        case Ies91HAnglesTypeALastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type A photometry last horizontal angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case Ies95HeaderInvalid():
            return IssueTranslation(
                _('Invalid header'),
                _('IESNA:LM-63-1995 header is invalid: {header}').format_map({"header": issue.header}),
            )
        case Ies95MetadataKeyMissingRecommended():
            return IssueTranslation(
                _('Suggested metadata missing'),
                _('Recommended metadata key {key} is missing').format_map({"key": issue.key}),
            )
        case Ies95LuminousOpeningGeometryInvalid():
            return IssueTranslation(
                _('Invalid luminous opening geometry'),
                _('Luminous opening geometry is invalid: width={width}, length={length}, height={height}').format_map(
                    {"width": issue.width, "length": issue.length, "height": issue.height}
                ),
            )
        case Ies95HAnglesTypeCFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type C photometry first horizontal angle is invalid: {value}. Expected 0.').format_map({"value": issue.value}),
            )
        case Ies95HAnglesTypeCLastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type C photometry last horizontal angle is invalid: {value}. Expected {expected}').format_map(
                    {"value": issue.last_value, "expected": "90, 180, or 360." if issue.first_value == 0 else "270."}
                ),
            )
        case Ies95HAnglesTypeBFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type B photometry first horizontal angle is invalid: {value}. Expected 0 or -90.').format_map({"value": issue.value}),
            )
        case Ies95HAnglesTypeBLastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type B photometry last horizontal angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case Ies95HAnglesTypeAFirstValueInvalid():
            return IssueTranslation(
                _('Invalid first horizontal angle'),
                _('Type A photometry first horizontal angle is invalid: {value}. Expected 0 or -90.').format_map({"value": issue.value}),
            )
        case Ies95HAnglesTypeALastValueInvalid():
            return IssueTranslation(
                _('Invalid last horizontal angle'),
                _('Type A photometry last horizontal angle is invalid: {value}. Expected 90.').format_map({"value": issue.value}),
            )
        case Ies95BallastLampPhotometricFactorDeprecated():
            return IssueTranslation(
                _('Deprecated ballast-lamp photometric factor'),
                _('Ballast-lamp photometric factor is deprecated. Use a value of 1.0 instead (given: {value})').format_map(
                    {"value": issue.value}
                ),
            )
        case _:
            return IssueTranslation(str(issue), None)
