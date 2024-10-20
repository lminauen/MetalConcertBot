import json

from datetime import datetime
from utils import write_log
from openai import OpenAI
from google_utils import query_google

from config import MODEL, LOCATION, RANGE

# Tool call handling
def process_tool_calls(completion):
    # Get tool call from response
    tool_calls = completion.choices[0].message.tool_calls
    response_messages = []

    # Process all tool calls in response
    for tool_call in tool_calls:
        # Extract arguments from generated call
        arguments = json.loads(tool_call.function.arguments)
        query = arguments.get('query')
        num_results = arguments.get('num_results')

        if not num_results or num_results < 0:
            num_results = 10

        # Call google api
        search_results = query_google(query, num_results)

        # Generate response message
        function_call_result_message = {
            "role": "tool",
            "content": json.dumps({
                "query": query,
                "num_results": num_results,
                "google_results": search_results
            }),
            "tool_call_id": tool_call.id
        }

        response_messages.append(function_call_result_message)

    return response_messages

# GPT API call
def get_response(request = ""):
    openai_client = OpenAI()
    request = request.strip()

    if not request:
        return

    write_log(request, "User")

    # Query OpenAI API
    completion = openai_client.chat.completions.create(
         model=MODEL,
         messages=[
            {"role": "system", "content": "You are a friendly and helpful assistant informing metal fans about concert announcements. " +
                                          "Events before " + str(datetime.now()) + " are of no interest. Unless stated otherwise, only consider concerts within a " + RANGE +
                                          " distance from " + LOCATION + ". Use the supplied tools to assist the user."},
            {
                "role": "user",
                "content": request
            }
        ],
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "query_google",
                    "description": "Call the Google Custom Search JSON API to look up information on the internet. Call this whenever you need online information for event dates or concert announcements.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Your google search input.",
                            },
                            "num_results": {
                                "type": "integer",
                                "description": "The number of results to be returned from Google. Defaults to ten if not provided."
                            }
                        },
                        "required": ["query"],
                        "additionalProperties": False,
                    },
                }
            }
        ]
    )


    if completion.choices[0].message.tool_calls:
        # Prepare new completion
        completion_message = {
            "model": MODEL,
            "messages": [
                {"role": "system",
                 "content": "You are a friendly and helpful assistant informing metal fans about concert announcements. " +
                                          "Parse the data you retrieved from google."},
                {"role": "user", "content": request},
                completion.choices[0].message,
                *process_tool_calls(completion)
            ]
        }

        write_log(completion_message["messages"], "System")

        completion = openai_client.chat.completions.create(
            model = MODEL,
            messages = completion_message["messages"]
        )

        write_log(completion.choices[0].message, "OpenAI")
        response = completion.choices[0].message.content
    else:
        write_log(completion.choices[0].message, "OpenAI")
        response = completion.choices[0].message.content

    return response