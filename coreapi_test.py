import coreapi


doc = coreapi.get('http://monitor.crest.iu.edu:9000/links')
print(doc)

# coreapi.action(doc, ['description'], params={'description': 'Test description'})

# print("After change")
# print(doc['description'])