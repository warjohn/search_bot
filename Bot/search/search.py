from Bot.search.SSMU_search_tool import SSMU

def search(input_query):
    engine = SSMU()
    result = engine.search(input_query)
    return result

