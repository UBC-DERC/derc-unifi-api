""" UBC DERC Camera API Class List
A set of classes to be used for consistency across API calls and services. These classes focus mostly on camera services.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Annotated, Self

from pydantic import BaseModel, Field, model_validator
from uiprotect.data import DeviceState

CameraId = Annotated[
  str,
  Field(description="The camera's colloquial name in the system (e.g., 'cam04'). This field is not guaranteed to be unique. Only the private attribute `mac_address` is unique.",
        examples=["cam04", "cam01", "bullet01"])
]

class CameraConnection(str, Enum):
  """How is the camera connected to the network? An enumerated set of values:

  ["wired", "wireless" or "unknown"]

  """
  wired = 'wired'
  wireless = 'wireless'
  unknown = 'unknown'


class CameraMetadataPublic(BaseModel):
  """Public camera metadata

  This metadata comes from a publically accessible CSV file (manually recorded). This files
  should be checked continuously, and updated following installation of new cameras. The metadata
  is all data that can be used to assess readiness for research purposes, video coverage of the farm
  and past availability.
  """
  camera_id: CameraId
  label: str = Field(description="The camera's descriptive name, provided by the DERC team.",
                     examples=["Calf barn pen 4 back", "Milking Robot 3 Front"])
  console_id: str = Field(description="The console (NVR, or server) to which the camera is connected.")
  location: str = Field(description="Description of the camera's physical location on the farm.")
  model: str = Field(description="Supplier model of the camera.")
  connection_type: CameraConnection = Field(default=CameraConnection.unknown, description="Connection type, either wired, wireless, or unknown. Cameras defined as unknown should be checked and updated.")
  resolution: str = Field(description="Camera resolution, currently stored as a text string.")


class CameraMetadataFull(CameraMetadataPublic):
  """An extension of the CameraMetadataPublic class to include the MAC address when a user has been authenticated.

  A MAC address is universally unique and may identify an instrument, and can possibly be used, in part, to access devices.
  """
  mac_address: str = Field(description="Valid and unique MAC address for the camera.",
                           pattern='^(?:(?:[0-9A-Fa-f]{2}(?=([-:]))(?:\1[0-9A-Fa-f]{2}){5}))$')

class CameraStatus(BaseModel):
  """Current status of the camera at the timestamp identified by the `statustimestamp` as reported by the Unifi API.
  """
  camera_id: CameraId
  is_connected: bool = Field(description="Is the camera currently connected to a console?",
                             examples=[True, False])
  is_recording: bool = Field(description="Is the camera currently recording?",
                             examples = [True, False])
  uptime_seconds: int | None = Field(default=None, description="How long has the camera been connected and recording (in seconds)?",
                                     examples=[36000, 10, None, 0])
  last_seen: datetime | None = Field(default = None, description="When was the camera last detected by the console to which it was connected?")
  state: DeviceState = Field(description="Camera API device state (Unifi fixed Enum)")
  console_reachable: bool = Field(description="Can the camera's gateway (console) be reached?")
  statustimestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC), description="Reported time of the status check.")

class Camera(BaseModel):
  """Full data model for camera description, including all metadata and current status.
  """
  metadata: CameraMetadataPublic | CameraMetadataFull = Field(description="Camera device metadata.")
  status: CameraStatus | None  = Field(default = None, description="Current camera status, including uptime, recording status and connection status.")

class Clip(BaseModel):
  """Class for a single clip from a camera.
  """
  camera_id: CameraId
  start: datetime = Field(description="Camera clip recording start time (UTC).")
  end: datetime = Field(description="Camera clip recording end time (UTC).")
  duration_seconds: float = Field(description="Clip duration in seconds.")
  download_url: str = Field(description="URL endpoint for the camera clip once prepared.")

  @model_validator(mode="after")
  def time_to_utc(self) -> Self:
    """Make sure that all timestamps use a consistent (UTC) timezone. We're using UTC for portability.

    Returns:
        Self: A Clip object.
    """
    self.start = self.start.astimezone(tz=UTC)
    self.end = self.end.astimezone(tz=UTC)
    return self

  @model_validator(mode="after")
  def check_duration(self) -> Self:
    """Make sure that the duration and the start and end times for the clip are similar (within 0.5 sec).

    Raises:
        ValueError: The clip length is not the same as that delta between the start and end times.

    Returns:
        Self: A Clip object.
    """
    if abs((self.end - self.start).total_seconds() - self.duration_seconds) < 0.5:
      return self
    else:
      raise ValueError("The described clip duration is different than the difference between the clip start and end time.")

class FieldDrift(BaseModel):
  """Internal flag if there are differences in field values between CSV files or
  Unifi API values reported from the Unifi servers.
  """
  camera_id: CameraId
  field: str = Field(description="Which field in the data CSV has drifted from accepted values as reported by the server/console?")
  csv_value: str = Field(description="Truth as reported in the CSV.")
  live_value: str = Field(description="Truth as reported from the console/server.")

class SyncCheckResult(BaseModel):
  """The full set of results from a single sync check event.
  """
  checked_at: datetime = Field(description="When was the check performed?")
  consoles_checked: list[str] = Field(description="Which consoles were checked?")
  consoles_unreachable: list[str] = Field(description="Consoles that were not reachable.")
  cameras_in_csv_only: list[str] = Field(description="List of cameras found in the CSV file, but not returned from the Protect API.")
  cameras_in_protect_only: list[str] = Field(description="List of cameras found in the Protect API, but not found in the CSV.")
  field_drift: list[FieldDrift] = Field(description="List of fields that diverge between the CSV and live (server) values.")
