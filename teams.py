import sqlite3
import os
from enum import IntEnum
from collections import namedtuple
from members import Members

TeamMember = namedtuple('TeamMember', ['name', 'barcode', 'type'])


class Status(IntEnum):
    inactive = 0
    active = 1


class TeamMemberType(IntEnum):
    student = 0
    mentor = 1
    coach = 2


class Teams(object):
    def __init__(self):
        pass

    def createTable(self, dbConnection):
        self.migrate(dbConnection, 0)

    def migrate(self, dbConnection, db_schema_version):
        if db_schema_version < 5:
            dbConnection.execute('''CREATE TABLE teams
                                 (team_id INTEGER PRIMARY KEY,
                                 name TEXT UNIQUE,
                                  active INTEGER default 1)''')
            dbConnection.execute('''CREATE TABLE team_members
                                 (team_id TEXT, barcode TEXT, type INTEGER default 1)''')

    def create_team(self, dbConnection, name):
        try:
            dbConnection.execute(
                "INSERT INTO teams VALUES (NULL,?,1)", (name, ))
            return ""
        except sqlite3.IntegrityError:
            return "Team name already exists"

    def get_team_list(self, dbConnection):
        team_list = []
        for row in dbConnection.execute('''SELECT team_id, name
                                FROM teams
                                WHERE (active = ?)
                                ORDER BY name''', (Status.active,)):
            team_list.append((row[0], row[1]))
        return team_list

    def team_id_from_name(self, dbConnection, name):
        data = dbConnection.execute(
            "SELECT * FROM teams WHERE (name=?)", (name, )).fetchone()
        if data:
            return data[0]
        return ''

    def team_name_from_id(self, dbConnection, team_id):
        data = dbConnection.execute(
            "SELECT * FROM teams WHERE (team_id=?)", (team_id, )).fetchone()
        if data:
            return data[1]
        return ''

    def add_team_members(self, dbConnection, team_id, listStudents, listMentors, listCoaches):
        fullList = []

        for student in listStudents:
            fullList.append((student, TeamMemberType.student))
        for mentor in listMentors:
            fullList.append((mentor, TeamMemberType.mentor))
        for coach in listCoaches:
            fullList.append((coach, TeamMemberType.coach))

        # Should it check to make sure team_id is valid?
            for member in fullList:
                dbConnection.execute("INSERT INTO team_members VALUES (?, ?, ?)",
                                     (team_id, member[0], member[1]))

    def get_team_members(self, dbConnection, team_id):
        listMembers = []
        for row in dbConnection.execute('''SELECT displayName,type,team_members.barcode
                            FROM team_members
                            INNER JOIN members ON members.barcode = team_members.barcode
                            WHERE (team_id == ?)
                            ORDER BY type, displayName''', (team_id,)):
            listMembers.append(TeamMember(row[0], row[2], row[1]))
        return listMembers


class TestFile():
    def __init__(self, filename):
        self.file = open(filename, "rb")
        self.filename = filename


        # unit test
if __name__ == "__main__":  # pragma no cover
    DB_STRING = 'data/test.db'
    try:
        os.remove(DB_STRING)   # Start with a new one
    except IOError:
        pass  # Don't care if it didn't exist
    teams = Teams()
    members = Members()
    dbConnection = sqlite3.connect(
        DB_STRING, detect_types=sqlite3.PARSE_DECLTYPES)
    members.create_table(dbConnection)
    teams.createTable(dbConnection)
    tf = TestFile("data/members.csv")
    members.bulkAdd(dbConnection, tf)

    error = teams.create_team(dbConnection, 'test')
    assert not error
    error = teams.create_team(dbConnection, 'test')  # should fail...
    assert error
    if error:
        print("Error adding: ", error)
    tid = teams.team_id_from_name(dbConnection, 'test')
    print("Team ID: ", tid)

    teams.add_team_members(dbConnection, tid, ["100090"], [], ["100091"])
    print("Members: ", teams.get_team_members(dbConnection, tid))
