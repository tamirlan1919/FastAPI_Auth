LINK_TTL = 600 #10 minutes

def link_key(code: str) -> str:
    return f'tg:link:{code}'