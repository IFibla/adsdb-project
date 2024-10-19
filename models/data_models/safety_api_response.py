from pydantic import BaseModel, HttpUrl


class SafetyApiResult(BaseModel):
    vehicle_picture: HttpUrl | None
    overall_rating: str | None
    overall_front_crash_rating: str | None
    front_crash_driverside_rating: str | None
    front_crash_passengerside_rating: str | None
    front_crash_picture: HttpUrl | None
    front_crash_video: HttpUrl | None
    overall_side_crash_rating: str | None
    side_crash_driverside_rating: str | None
    side_crash_passengerside_rating: str | None
    combined_side_barrier_and_pole_rating_front: str | None
    combined_side_barrier_and_pole_rating_rear: str | None
    side_barrier_rating_overall: str | None
    rollover_rating: str | None
    rollover_rating2: str | None
    rollover_possibility: float | None
    rollover_possibility2: float | None
    dynamic_tip_result: str | None
    side_pole_crash_rating: str | None
    side_pole_picture: HttpUrl | None
    side_pole_video: HttpUrl | None
    nhsta_electronic_stability_control: str | None
    nhsta_forward_collision_warning: str | None
    nhsta_lane_departure_warning: str | None
    complaints_count: int | None
    recalls_count: int | None
    investigation_count: int | None
    model_year: int | None
    make: str | None
    model: str | None
    vehicle_description: str | None
    vehicle_id: int


class SafetyApiResponse(BaseModel):
    count: int
    message: str
    results: list[SafetyApiResult]
