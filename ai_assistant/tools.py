from random import randint
from datetime import date, datetime, time
from llama_index.core.tools import QueryEngineTool, FunctionTool, ToolMetadata
from ai_assistant.rags import TravelGuideRAG
from ai_assistant.prompts import travel_guide_qa_tpl, travel_guide_description
from ai_assistant.config import get_agent_settings
from ai_assistant.models import (
    TripReservation,
    TripType,
    HotelReservation,
    RestaurantReservation,
)
from ai_assistant.utils import save_reservation

SETTINGS = get_agent_settings()

travel_guide_tool = QueryEngineTool(
    query_engine=TravelGuideRAG(
        store_path=SETTINGS.travel_guide_store_path,
        data_dir=SETTINGS.travel_guide_data_path,
        qa_prompt_tpl=travel_guide_qa_tpl,
    ).get_query_engine(),
    metadata=ToolMetadata(
        name="travel_guide", description=travel_guide_description, return_direct=False
    ),
)


# Tool functions
#flight:
def reserve_flight(date_str: str, departure: str, destination: str) -> TripReservation:

    print(
        f"Making flight reservation from {departure} to {destination} on date: {date}"
    )
    reservation = TripReservation(
        trip_type=TripType.flight,
        departure=departure,
        destination=destination,
        date=date.fromisoformat(date_str),
        cost=randint(200, 700),
    )

    save_reservation(reservation)
    return reservation


flight_tool = FunctionTool.from_defaults(fn=reserve_flight, return_direct=False)

#bus:
def reserve_bus(date_str: str, departure: str, destination: str) -> TripReservation:

    print(
        f"Making bus reservation from {departure} to {destination} on date: {date}"
    )
    reservation = TripReservation(
        trip_type=TripType.bus,
        departure=departure,
        destination=destination,
        date=date.fromisoformat(date_str),
        cost=randint(200, 700),
    )

    save_reservation(reservation)
    return reservation


bus_tool = FunctionTool.from_defaults(fn=reserve_bus, return_direct=False)

#hotel
def reserve_hotel(start_date: str,end_date:str, hotel: str, city: str) -> HotelReservation:

    print(
        f"Making hotel reservation on {hotel} hotel, located in {city} on dates: {start_date} to {end_date}"
    )
    reservation = HotelReservation(
        checkin_date=date.fromisoformat(start_date),
        checkout_date=date.fromisoformat(end_date),
        hotel_name=hotel,
        city=city,
        cost=randint(100,1000)
    )
    save_reservation(reservation)
    return reservation


hotel_tool = FunctionTool.from_defaults(fn=reserve_hotel, return_direct=False)

#restaurant:
def reserve_restaurant(date: str,time:str, restaurant: str, city: str,dish:str) -> RestaurantReservation:

    print(
        f"Making restaurant reservation on {restaurant} restaurant, located in {city} on date: {date} at {time}, you ordered: {dish}"
    )
    reservation_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    reservation = RestaurantReservation(
        reservation_time=reservation_datetime,
        restaurant=restaurant,
        city=city,
        dish=dish,
        cost=randint(10,1000)

    )
    save_reservation(reservation)
    return reservation


restaurant_tool = FunctionTool.from_defaults(fn=reserve_restaurant, return_direct=False)