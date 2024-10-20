from pydantic import BaseModel, HttpUrl, Field


class SafetyApiResult(BaseModel):
    vehicle_picture: HttpUrl | None = Field(alias="VehiclePicture")
    overall_rating: str | None = Field(alias="OverallRating")
    overall_front_crash_rating: str | None = Field(alias="OverallFrontCrashRating")
    front_crash_driverside_rating: str | None = Field(
        alias="FrontCrashDriversideRating"
    )
    front_crash_passengerside_rating: str | None = Field(
        alias="FrontCrashPassengersideRating"
    )
    overall_side_crash_rating: str | None = Field(alias="OverallSideCrashRating")
    side_crash_driverside_rating: str | None = Field(alias="SideCrashDriversideRating")
    side_crash_passengerside_rating: str | None = Field(
        alias="SideCrashPassengersideRating"
    )
    combined_side_barrier_and_pole_rating_front: str | None = Field(
        alias="combinedSideBarrierAndPoleRating-Front"
    )
    combined_side_barrier_and_pole_rating_rear: str | None = Field(
        alias="combinedSideBarrierAndPoleRating-Rear"
    )
    side_barrier_rating_overall: str | None = Field(alias="sideBarrierRating-Overall")
    rollover_rating: str | None = Field(alias="RolloverRating")
    rollover_rating2: str | None = Field(alias="RolloverRating2")
    rollover_possibility: float | None = Field(alias="RolloverPossibility")
    rollover_possibility2: float | None = Field(alias="RolloverPossibility2")
    dynamic_tip_result: str | None = Field(alias="dynamicTipResult")
    side_pole_crash_rating: str | None = Field(alias="SidePoleCrashRating")
    nhsta_electronic_stability_control: str | None = Field(
        alias="NHTSAElectronicStabilityControl"
    )
    nhsta_forward_collision_warning: str | None = Field(
        alias="NHTSAForwardCollisionWarning"
    )
    nhsta_lane_departure_warning: str | None = Field(alias="NHTSALaneDepartureWarning")
    complaints_count: int | None = Field(alias="ComplaintsCount")
    recalls_count: int | None = Field(alias="RecallsCount")
    investigation_count: int | None = Field(alias="InvestigationCount")
    model_year: int | None = Field(alias="ModelYear")
    make: str | None = Field(alias="Make")
    model: str | None = Field(alias="Model")
    vehicle_description: str | None = Field(alias="VehicleDescription")
    vehicle_id: int = Field(alias="VehicleId")

    class Config:
        protected_namespaces = ()


class SafetyApiResponse(BaseModel):
    count: int = Field(alias="Count")
    message: str = Field(alias="Message")
    results: list[SafetyApiResult] = Field(alias="Results")

    class Config:
        populate_by_name = True
