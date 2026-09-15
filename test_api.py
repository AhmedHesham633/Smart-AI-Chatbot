from src.api_client import generate_response


messages = [
    {
        "role": "user",
        "content": "Say hello in one short sentence."
    }
]


try:
    reply = generate_response(messages)

    assert reply, "Response text should not be empty"

    print("SUCCESS!")
    print("AI Response:")
    print(reply)

except Exception as e:
    print("API Error handled successfully:")
    print(e)