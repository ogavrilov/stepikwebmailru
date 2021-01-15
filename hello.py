def app(env, start_response):
    query_string = env.get("QUERY_STRING")
    data = list()
    if query_string:
        data.append(bytes(str(query_string).replace("&", "\n"), 'ascii'))
    #
    headers = list()
    headers.append(("Content-Type", "text/plain"))
    start_response("200 OK", headers)
    return iter([data])
