import boto3
import requests


def get_top_song(top_n):
    """Returns the top n popular songs for the request.
    Args:
        top_n (number): desired number of top songs.
    Returns:
        response (json): The top n popular songs and artists.
    """

    params = {
        "offset": 0,
        "limit": top_n,
    }

    headers = {
        "x-app-id": "soundcharts",
        "x-api-key": "soundcharts",
    }

    url = "https://customer.api.soundcharts.com/api/v2.14/chart/song/global-28/ranking/latest"

    try:
        response = requests.get(url, headers=headers, params=params)
        return_songs = []
        for item in response.json()["items"]:
            return_songs.append(
                {
                    "json": {
                        "song name": item["song"]["name"],
                        "credit": item["song"]["creditName"],
                    }
                }
            )
        return return_songs

    except requests.exceptions.HTTPError as err:
        raise "HTTP error occurred: %s" % err


def generate_text(bedrock_client, model_id, tool_config, input_text):
    """Generates text using the supplied Amazon Bedrock model. If necessary,
    the function handles tool use requests and sends the result to the model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The Amazon Bedrock model ID.
        tool_config (dict): The tool configuration.
        input_text (str): The input text.
    Returns:
        Nothing.
    """

    # Create the initial message from the user input.
    messages = [{"role": "user", "content": [{"text": input_text}]}]

    response = bedrock_client.converse(
        modelId=model_id, messages=messages, toolConfig=tool_config
    )

    output_message = response["output"]["message"]
    messages.append(output_message)
    stop_reason = response["stopReason"]

    if stop_reason == "tool_use":
        # Tool use requested. Call the tool and send the result to the model.
        tool_requests = response["output"]["message"]["content"]
        for tool_request in tool_requests:
            if "toolUse" in tool_request:
                tool = tool_request["toolUse"]
                print(f"Requesting tool {tool['name']}. Input: {tool['input']}")

                if tool["name"] == "top_song":
                    tool_result = {}
                    try:
                        response = get_top_song(tool["input"]["top_n"])
                        tool_result = {
                            "toolUseId": tool["toolUseId"],
                            "content": response,
                        }
                    except Exception as err:
                        tool_result = {
                            "toolUseId": tool["toolUseId"],
                            "content": [{"text": err.args[0]}],
                            "status": "error",
                        }
                        print(f"Error: {err.args[0]}")

                    tool_result_message = {
                        "role": "user",
                        "content": [{"toolResult": tool_result}],
                    }
                    messages.append(tool_result_message)

                    # Send the tool result to the model.
                    response = bedrock_client.converse(
                        modelId=model_id, messages=messages, toolConfig=tool_config
                    )
                    output_message = response["output"]["message"]

    # print the final response from the model.
    for content in output_message["content"]:
        print(content["text"])


def main(input_text):
    """
    Entrypoint for tool use example.
    """
    model_id = "cohere.command-r-v1:0"

    tool_config = {
        "tools": [
            {
                "toolSpec": {
                    "name": "top_song",
                    "description": "Get the top n popular song played on the leaderboard.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "top_n": {
                                    "type": "number",
                                    "description": "The number of top songs to return. Must be an integer.",
                                }
                            },
                            "required": ["top_n"],
                        }
                    },
                }
            }
        ]
    }
    bedrock_client = boto3.client(service_name="bedrock-runtime")

    try:
        print(f"Question: {input_text}")
        generate_text(bedrock_client, model_id, tool_config, input_text)

    except Exception as err:
        message = err.response["Error"]["Message"]
        print(f"A client error occured: {message}")


if __name__ == "__main__":
    main("給我前三名的歌曲，用繁體中文回答。")
    # main("1+1=?")
