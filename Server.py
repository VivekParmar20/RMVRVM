from fastapi import FastAPI
import asyncio
import concurrent.futures
import math
import os
import time
import httpx

cpu_rapl_path = '/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj'
start_time = 0
initial_value = 0

app = FastAPI()

@app.get("/")
def greetings():
    global start_time, initial_value
    
    start_time = time.time()

    with open(cpu_rapl_path, 'r') as file:
        initial_value = int(file.read().strip())
    return {"Measuring Started From Home Page"}

def perform_math_calculation(number):
    t = number
    art = math.tan(t)
    atan_art = math.atan(art)
    atan2_t_art = math.atan2(t, art)
    atan2_art_t = math.atan2(art, t)

    return {
        "art": art,
        "atan_art": atan_art,
        "atan2_t_art": atan2_t_art,
        "atan2_art_t": atan2_art_t
    }

@app.get("/calculate/{number}")
async def calculate(number: int):
    loop = asyncio.get_event_loop()

    # Execute the math calculation asynchronously using a thread pool executor
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, perform_math_calculation, number)

    with open(cpu_rapl_path, 'r') as file:
        final_value = int(file.read().strip())

    end_time = time.time()

    energy_consumption = final_value - initial_value
    execution_time = end_time - start_time

    return {
        "result": result,
        "Energy consumption (microjoules (uJ))": energy_consumption,
        "Execution time (seconds)": execution_time
    }

async def simulate_users(num_users, number):
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(num_users):
            task = client.get(f"http://localhost:8000/calculate/{number}")
            tasks.append(task)
        responses = await asyncio.gather(*tasks)

    return responses

@app.get("/load_test/{number}")
async def load_test(number: int):
    global start_time, initial_value

    user_counts = [1, 10, 20, 50, 100, 200]
    load_test_results = {}

    for user_count in user_counts:
        start_time = time.time()

        with open(cpu_rapl_path, 'r') as file:
            initial_value = int(file.read().strip())

        responses = await simulate_users(user_count, number)

        with open(cpu_rapl_path, 'r') as file:
            final_value = int(file.read().strip())

        end_time = time.time()

        energy_consumption = final_value - initial_value
        execution_time = end_time - start_time

        load_test_results[user_count] = {
            "Energy consumption (microjoules (uJ))": energy_consumption,
            "Execution time (seconds)": execution_time,
            "Responses": [response.json() for response in responses]
        }

    return load_test_results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

