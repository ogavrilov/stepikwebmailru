def app(env, start_response):
    query_string = env.get("QUERY_STRING")
    data = list()
    if query_string:
        new_data = str(query_string).replace("&", "\n")
        data.append(bytes(new_data))
    #
    headers = list()
    headers.append(("Content-Type", "text/plain"))
    start_response("200 OK", headers)
    return iter([data])
