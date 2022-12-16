"""
Low level object models that are to be serialized as JSON.
NOT PUBLIC API, these are not intended to be used by client code
unless explicitly exported as public in __init__.py

Developer notes:
A field can either have metadata.spec_field set or field.SPEC_OBJECT set, not both.
If SPEC_OBJECT is set, this field is an union type and serialization should take the
value in `SPEC_OBJECT` as the serialized field name. Otherwise, the metadata.spec_field
says what the serializer should use for field name.
In general, metadata.spec_field should only be present for primitive types.
"""
from enum import Enum
import dataclasses as dc
import typing as ty

from .formatter import format_enum, format_timestamp

# TODO: waiting on spec md PR to add all docstrings for objects and fields.


class ArtifactType(ty.Protocol):
    """
    Protocol type to describe all low level serializable objects in this file.
    """

    __dataclass_fields__: ty.ClassVar[dict]


class OCPVersion(Enum):
    VERSION_2_0 = (2, 0)


@dc.dataclass
class SchemaVersion:
    SPEC_OBJECT: ty.ClassVar[str] = "schemaVersion"

    major: int = dc.field(
        default=OCPVersion.VERSION_2_0.value[0],
        metadata={"spec_field": "major"},
    )

    minor: int = dc.field(
        default=OCPVersion.VERSION_2_0.value[1],
        metadata={"spec_field": "minor"},
    )


class LogSeverity(Enum):
    INFO = 1
    DEBUG = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5


@dc.dataclass
class Log:
    SPEC_OBJECT: ty.ClassVar[str] = "log"

    severity: LogSeverity = dc.field(
        metadata={
            "spec_field": "severity",
            "formatter": format_enum,
        },
    )

    message: str = dc.field(
        metadata={"spec_field": "message"},
    )


@dc.dataclass
class Error:
    SPEC_OBJECT: ty.ClassVar[str] = "error"

    symptom: str = dc.field(
        metadata={"spec_field": "symptom"},
    )

    message: ty.Optional[str] = dc.field(
        metadata={"spec_field": "message"},
    )

    software_info_ids: list[str] = dc.field(
        metadata={"spec_field": "softwareInfoIds"},
    )


class DiagnosisType(Enum):
    PASS = 1
    FAIL = 2
    UNKNOWN = 3


@dc.dataclass
class Diagnosis:
    SPEC_OBJECT: ty.ClassVar[str] = "diagnosis"

    verdict: str = dc.field(
        metadata={"spec_field": "verdict"},
    )

    type: DiagnosisType = dc.field(
        metadata={
            "spec_field": "type",
            "formatter": format_enum,
        },
    )

    message: ty.Optional[str] = dc.field(
        metadata={"spec_field": "message"},
    )

    # TODO: hardwareInfoId
    # TODO: subcomponent


@dc.dataclass
class DutInfo:
    pass


@dc.dataclass
class RunStart:
    SPEC_OBJECT: ty.ClassVar[str] = "testRunStart"

    name: str = dc.field(
        metadata={"spec_field": "name"},
    )

    version: str = dc.field(
        metadata={"spec_field": "version"},
    )

    command_line: str = dc.field(
        default="",
        metadata={"spec_field": "commandLine"},
    )

    parameters: dict[str, ty.Any] = dc.field(
        default_factory=dict,
        metadata={"spec_field": "parameters"},
    )

    # TODO: is still a list?
    dut_info: list[DutInfo] = dc.field(
        default_factory=list,
        metadata={"spec_field": "dutInfo"},
    )


class TestStatus(Enum):
    COMPLETE = 1
    ERROR = 2
    SKIP = 3


class TestResult(Enum):
    PASS = 1
    FAIL = 2
    NOT_APPLICABLE = 3


@dc.dataclass
class RunEnd:
    SPEC_OBJECT: ty.ClassVar[str] = "testRunEnd"

    status: TestStatus = dc.field(
        metadata={
            "spec_field": "status",
            "formatter": format_enum,
        },
    )

    result: TestResult = dc.field(
        metadata={
            "spec_field": "result",
            "formatter": format_enum,
        },
    )


@dc.dataclass
class RunArtifact:
    SPEC_OBJECT: ty.ClassVar[str] = "testRunArtifact"

    impl: RunStart | RunEnd | Log | Error


@dc.dataclass
class StepStart:
    SPEC_OBJECT: ty.ClassVar[str] = "testStepStart"

    name: str = dc.field(
        metadata={"spec_field": "name"},
    )


@dc.dataclass
class StepEnd:
    SPEC_OBJECT: ty.ClassVar[str] = "testStepEnd"

    status: TestStatus = dc.field(
        metadata={
            "spec_field": "status",
            "formatter": format_enum,
        },
    )


@dc.dataclass
class StepArtifact:
    SPEC_OBJECT: ty.ClassVar[str] = "testStepArtifact"

    id: str = dc.field(
        metadata={"spec_field": "testStepId"},
    )

    # TODO: measurement
    # TODO: measurementSeriesStart
    # TODO: measurementSeriesEnd
    # TODO: measurementSeriesElement
    # TODO: error
    # TODO: file
    # TODO: extension
    impl: StepStart | StepEnd | Diagnosis | Log | Error


RootArtifactType = SchemaVersion | RunArtifact | StepArtifact


@dc.dataclass
class Root:
    impl: RootArtifactType

    sequence_number: int = dc.field(
        metadata={"spec_field": "sequenceNumber"},
    )

    timestamp: float = dc.field(
        metadata={
            "spec_field": "timestamp",
            "formatter": format_timestamp,
        },
    )
