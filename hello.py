def app(env, start_response):
    query_string = env.get("QUERY_STRING")
    data = ''
    if query_string:
        data += str(query_string).replace("&", "\n")
    try:
        data_bytes = bytes(data)
    except:
        data_bytes = bytes(data, 'utf-8')
    #
    headers = list()
    headers.append(("Content-Type", "text/plain"))
    start_response("200 OK", headers)
    return [data_bytes]
