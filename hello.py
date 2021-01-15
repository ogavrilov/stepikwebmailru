def app(env, start_response):
    query_string = env.get("QUERY_STRING")
    data = ''
    if query_string:
        data += str(query_string).replace("&", "\n")
    #
    headers = list()
    headers.append(("Content-Type", "text/plain"))
    start_response("200 OK", headers)
    return [bytes(data)]