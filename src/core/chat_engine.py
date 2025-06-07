def get_ai_response(messages, llm):
    response = llm.invoke(messages)
    # Handle response structure
    if hasattr(response, "content"):
        return response.content
    else:
        return str(response)