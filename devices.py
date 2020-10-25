
class Device(object):
    def __init__(self, name, mac, barcode):
        self.name = name
        self.mac = mac
        self.barcode = barcode


class Devices(object):
    def __init__(self):
        pass

    def migrate(self, dbConnection, db_schema_version):  # pragma: no cover
        if db_schema_version < 11:
            dbConnection.execute('''CREATE TABLE devices
                                 (mac TEXT PRIMARY KEY,
                                  barcode TEXT,
                                  name TEXT)''')

    def add(self, dbConnection, mac, name, barcode):
        dbConnection.execute(
            "INSERT INTO devices(barcode, mac, name) VALUES(?,?,?)", (barcode, mac, name))

    def delete(self, dbConnection, mac, barcode):
        dbConnection.execute(
            "DELETE from devices WHERE (mac=?) AND (barcode=?)", (mac, barcode))

    def getList(self, dbConnection, barcode):
        listDevices = []
        print(f'BARCODE: {barcode}')
        for row in dbConnection.execute('''SELECT name, mac, barcode
            FROM devices
            WHERE barcode = ?
            ORDER BY name''', (barcode,)):
            listDevices.append(Device(name=row[0], mac=row[1], barcode=row[2]))
        return listDevices
