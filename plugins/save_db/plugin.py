class SaveDBPlugin:

    name = "save_db"

    def execute(self, data):
        print("Saving data:", data)
        return {"status": "saved"}