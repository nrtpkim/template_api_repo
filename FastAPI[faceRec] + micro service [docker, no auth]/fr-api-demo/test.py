from src.provider.ElasticsearchService import ElasticsearchService

ES = ElasticsearchService()

# print(ES.create_index('test1234'))
print(ES.query_index())
# print("xxx")