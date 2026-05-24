from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Tuple
from routing_algorithm import calculate_optimal_route

app = FastAPI()

# Injecting the CORS middleware to allow the local HTML file to communicate with the server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoutingRequest(BaseModel):
    graph: Dict[str, List[Tuple[str, float]]]
    start_node: str
    destinations: List[str]
    demand_factors: Dict[str, float]

@app.post("/optimize")
def optimize_delivery_route(request: RoutingRequest):
    result = calculate_optimal_route(
        graph=request.graph,
        start_node=request.start_node,
        destinations=request.destinations,
        demand_factors=request.demand_factors
    )
    return result