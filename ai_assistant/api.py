from fastapi import FastAPI, Depends, Query
from llama_index.core.agent import ReActAgent
from ai_assistant.agent import TravelAgent
from ai_assistant.models import AgentAPIResponse,TripReservation,HotelReservation,RestaurantReservation
from ai_assistant.tools import reserve_flight, reserve_bus, reserve_hotel, reserve_restaurant
import os, json
from ai_assistant.config import get_agent_settings

SETTINGS = get_agent_settings()

def get_agent() -> ReActAgent:
    return TravelAgent().get_agent()


app = FastAPI(title="AI Agent")


@app.get("/recommendations/cities")
def recommend_cities(
    notes: list[str] = Query(...), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"recommend cities in bolivia with the following notes: {notes}"
    print(str(agent.chat(prompt)))
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))

@app.get("/recommendations/hotels")
def recommend_hotels(
    notes: list[str] = Query(...), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"recommend hotels in the cities previously mentioned, or to be mentioned from bolivia with the following notes: {notes}"
    print(str(agent.chat(prompt)))
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))

@app.get("/recommendations/activities")
def recommend_hotels(
    notes: list[str] = Query(...), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"recommend activities in the cities previously mentioned, or to be mentioned from bolivia with the following notes: {notes}"
    print(str(agent.chat(prompt)))
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))

@app.get("/reservation/flights")
def reservation_flights(
    date_str:str,
    departure:str,
    destination:str
)->TripReservation:
    return reserve_flight(date_str,departure,destination)

@app.get("/reservation/bus")
def reservation_bus(
    date_str:str,
    departure:str,
    destination:str
)->TripReservation:
    return reserve_bus(date_str,departure,destination)

@app.get("/reservation/hotel")
def reservation_hotel(
    start_date: str,
    end_date:str, 
    hotel: str, 
    city: str
)->HotelReservation:
    return reserve_hotel(start_date,end_date,hotel,city)

@app.get("/reservation/restaurant")
def reservation_restaurant(
    date: str,
    time:str, 
    restaurant: str, 
    city: str,
    dish:str
)-> RestaurantReservation:
    return reserve_restaurant(date,time,restaurant,city,dish)
    
@app.get("/summary")
def summary(
    agent: ReActAgent = Depends(get_agent)
):
    if os.path.exists(SETTINGS.log_file) and os.path.getsize(SETTINGS.log_file) > 0:
        with open(SETTINGS.log_file, "r") as file:
            try:
                reservations = json.load(file)
            except json.JSONDecodeError:
                print(json.JSONDecodeError)
    prompt = f"""make a brief summary of all the items in the following list: {reservations}, all clasified as bullet points, organize its content by "place" as a header and "date" as a subtitle, with the description of each activity as a bullet point also sum all items called "cost" to return a total, in adition to brief comments about the places and activities to do."""
    #print(str(agent.chat(prompt)))
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))