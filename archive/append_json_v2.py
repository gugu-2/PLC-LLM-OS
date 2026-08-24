import json

with open("st_code.txt", "r") as f:
    st_content = f.read()

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Lead Medical Robotics Engineer. Evolve a basic servo block into a Robotic Surgery Console Controller. Technical Specs: 1. Haptic feedback scaling to translate microscopic surgical resistance back to the surgeon's fingers. 2. Inverse kinematics for 7-DOF surgical arms. 3. Micro-tremor cancellation algorithms. Ensure production-grade safety, error handling, and hard real-time compliance."
        },
        {
            "role": "assistant",
            "content": st_content
        }
    ]
}

with open("data/synthetic_generation_v3_enterprise.jsonl", "a") as f:
    f.write(json.dumps(data) + "\n")
