from storage_systems import FileBasedStorage, DatabaseStorage


file_based = FileBasedStorage()
db = DatabaseStorage()

print("File Based System.")
file_based.load()
file_based.save()
file_based.store()
file_based.delete()
print("\n")

print("Database Storage System.")
db.load()
db.save()
db.store()
db.delete()