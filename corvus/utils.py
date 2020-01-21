def proccess_headers(headers):

    return {
        header[0].decode(): header[1].decode() for header in headers
    }
