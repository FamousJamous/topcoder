import re

def create_header_name(class_name):
 temp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
 return "{}.h".format(re.sub('([a-z0-9])([A-Z])', r'\1_\2', temp).lower())
