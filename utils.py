def getString(value):
  if isinstance(value, bytes):
    return value.decode()
  else:
    return value
