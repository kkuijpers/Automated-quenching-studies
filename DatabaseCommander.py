import os
import sqlite3 as lite
from tkinter import messagebox
import logging

class DatabaseHandler():
    def __init__(self, database, workingDir=os.getcwd()):
        # initiation that is needed for every device
        self.logger = logging.getLogger('AutosamplerLog')
        self.logger.info('Serial is initiated')

        self.databaseDir = workingDir
        self.databaseName = database
        self.databaseLocation = os.path.join(self.databaseDir, self.databaseName)

        self.connection = self.CreateConnection()
        if self.connection is None:
            print('Database does not exists')

    def CreateConnection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            connection = lite.connect(self.databaseLocation)
            return connection
        except Exception as e:
            print(e)

        return None

    def CreateSolvent(self, solvent):
        """
        Creates a new entery in the table solvent
        :param connection:
        :param solvent:
        :return: solvent id
        """
        sqlInsert = '''INSERT INTO solvents (solvent)
                    VALUES(?)'''

        sqlGetCat = '''SELECT * FROM catalysts'''

        sqlInsLifetime = '''INSERT INTO Lifetime_couples(
                            ID_cat, ID_sol)
                            VALUES(?,?)'''

        cursor = self.connection.cursor()
        try:
            with self.connection:
                cursor = self.connection.cursor()

                cursor.execute(sqlInsert, solvent)
                idSol = cursor.lastrowid

                cursor.execute(sqlGetCat)
                allData = cursor.fetchall()

                for row in range(0, len(allData)):
                    idCat = allData[row][0]
                    insertLifetime = (idCat, idSol)
                    cursor.execute(sqlInsLifetime, insertLifetime)

            return cursor.lastrowid

        except lite.IntegrityError:
            messagebox.showerror("Integrity Error", 'Solvent already exists in the database.\n'
                                                    'Cannot create this entry.')
            return False
        except Exception as e:
            messagebox.showerror('Unknown error occurred',
                                 "A unknown error occurred named : \n{}".format(e))

    def CreateSingleSolvent(self, solvent):
        """
        creates a single solvent entry
        :param connection:
        :param solvent:
        :return:
        """

        sqlInsert = '''INSERT INTO solvents (solvent)
                        VALUES(?)'''

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(sqlInsert, solvent)

            return cursor.lastrowid
        except lite.IntegrityError:
            messagebox.showerror("Integrity Error", 'Solvent already exists in the database.\n'
                                                    'Cannot create this entry.')
            return False
        except Exception as e:
            messagebox.showerror('Unknown error occurred',
                                 "A unknown error occurred named : \n{}".format(e))

    def GetAllSolvents(self):
        '''
        returns al solvents in the solvent table
        :return:
        '''

        sql = '''SELECT solvent FROM Solvents'''

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            solvents = cursor.fetchall()
        return solvents

    def CreateCatalyst(self, catalyst):
        """
        Creates a new entery in the catalyst table
        :param connection:
        :param catalyst:
        :return: catalyst id
        """
        sqlInsert = '''INSERT INTO catalysts (catalyst)
                       VALUES(?)'''

        sqlGetSol = '''SELECT * FROM solvents'''

        sqlInsLifetime = '''INSERT INTO Lifetime_couples(
                                ID_cat, ID_sol)
                                VALUES(?,?)'''

        try:
            with self.connection:
                cursor = self.connection.cursor()

                cursor.execute(sqlInsert, catalyst)
                idCat = cursor.lastrowid

                cursor.execute(sqlGetSol)
                allData = cursor.fetchall()

                for row in range(0, len(allData)):
                    idSol = allData[row][0]
                    insertLifetime = (idCat, idSol)
                    cursor.execute(sqlInsLifetime, insertLifetime)

            return cursor.lastrowid

        except lite.IntegrityError:
            messagebox.showerror("Integrity Error", 'Catalyst already exists in the database.\n'
                                                    'Cannot create this entry.')
            return False
        except Exception as e:
            messagebox.showerror('Unknown error occurred',
                                 "A unknown error occurred named : \n{}".format(e))

    def CreateSingleCatalyst(self, catalyst):
        """
           Creates a new entery in the catalyst table
           :param connection:
           :param catalyst:
           :return: catalyst id
           """

        sqlInsert = '''INSERT INTO catalysts (catalyst)
                           VALUES(?)'''

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(sqlInsert, catalyst)
                return cursor.lastrowid
        except lite.IntegrityError:
            messagebox.showerror("Integrity Error", 'Catalyst already exists in the database.\n'
                                                    'Cannot create this entry.')
            return False
        except Exception as e:
            messagebox.showerror('Unknown error occurred',
                                 "A unknown error occurred named : \n{}".format(e))

    def GetAllCatalysts(self):
        """
        return all catalysts in a list
        :return:
        """
        sql = 'SELECT catalyst FROM Catalysts'

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            catalysts = cursor.fetchall()
        return catalysts

    def InsertAutomationExperiment(self, data):
        """
        inserts a new experiment into the database
        :param connection:
        :param data:
        :return:
        """

        sql = ''' INSERT INTO Automation_experiments(
        Date, Name, ID_Cat, Number_experiments, I0, t0,
        Position, Name_sample, Quenching_code, Peak_data)
        VALUES(?,?,
        (SELECT ID FROM Catalysts Where Catalyst = ?) ,
        ?,?,?,?,?,?,?)'''

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)

        return cursor.lastrowid

    def InsertSVExperiment(self, data):
        """
        Inserts a new SV experiment into the database
        :param connection:
        :param data:
        :return:
        """

        sql = ''' INSERT INTO SV_experiments(
                Date, Name, ID_Cat, ID_sol, Quencher,
                Num_points, Slope, R2, Kq, Data)
                VALUES(?,?,
                (SELECT ID FROM Catalysts Where Catalyst = (?) ),
                (SELECT ID FROM Solvents  WHERE Solvent = (?)),
                ?,?,?,?,?,?)'''

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)

        return cursor.lastrowid

    def AskForLifetime(self, data):
        """
        returns the lifetime from the database
        :param data:
        :return:life time of solvent/ catalyst couple
                or None if error or no value found
        """

        sql = '''SELECT Lifetime FROM Lifetime_couples WHERE
         id_cat = (select id from catalysts where catalyst = ?) AND
         id_sol = (select id from solvents where solvent = ?)'''

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(sql, data)
                answer = cursor.fetchone()[0]
                return answer
        except lite.IntegrityError:
            messagebox.showerror("Integrity Error", 'Catalyst already exists in the database.\n'
                                                    'Cannot create this entry.')
            return None
        except Exception as e:
            messagebox.showerror('Unknown error occurred',
                                 "A unknown error occurred named : \n{}".format(e))
            return None
        pass

    def InsertLifetime(self, data):
        lifetime = data[0] / 1e9
        catalyst = data[1]
        solvent = data[2]

        sqlinsert = '''UPDATE lifetime_couples
                      SET lifetime = ? WHERE
                      id_cat = (SELECT id FROM Catalysts WHERE catalyst = ?) AND
                      id_sol = (SELECT id FROM solvents WHERE solvent = ?) '''

        sqlask = ''' SELECT ID, Slope
                FROM SV_Experiments WHERE
                ID_cat = (SELECT id FROM Catalysts WHERE catalyst = ?) AND
                ID_sol = (SELECT id FROM solvents WHERE solvent = ?)
                '''

        sqlupdate = '''UPDATE SV_Experiments
                SET Kq = ?
                WHERE ID = ?'''

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sqlinsert, (lifetime, catalyst, solvent))
            cursor.execute(sqlask, (catalyst, solvent))
            rows = cursor.fetchall()

            update = [0.0] * len(rows)

            for i in range(len(rows)):
                idl = rows[i][0]
                kq = rows[i][1] / lifetime
                update[i] = (kq, idl)

            cursor.executemany(sqlupdate, update)

        pass

    def RecreateOriginalTables(self):

        sqlCreateCatalysts = '''CREATE TABLE `Catalysts` (
        `ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `Catalyst`	TEXT NOT NULL UNIQUE);'''

        sqlCreateSolvents = ''' CREATE TABLE `Solvents` (
        `ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `Solvent`	TEXT NOT NULL UNIQUE);'''

        sqlCreateLifetime = '''CREATE TABLE `Lifetime_couples` (
            `ID_cat`	INTEGER NOT NULL,
            `ID_sol`	INTEGER NOT NULL,
            `Lifetime`	NUMERIC DEFAULT NULL,
            FOREIGN KEY(`ID_cat`) REFERENCES `Catalysts`(`ID`),
            FOREIGN KEY(`ID_sol`) REFERENCES `Solvents`(`ID`));'''

        sqlCreateAutomation = '''CREATE TABLE `Automation_experiments` (
        `ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `Date`	TEXT NOT NULL,
        `Name`	TEXT NOT NULL,
        `ID_Cat`	INTEGER NOT NULL,
        `Number_experiments`	INTEGER NOT NULL,
        `I0`	NUMERIC NOT NULL,
        `t0`	NUMERIC NOT NULL,
        `Position`	TEXT NOT NULL,
        `Name_sample`	TEXT,
        `Quenching_code`	TEXT,
        `Peak_data`	BLOB DEFAULT NULL,
        FOREIGN KEY(`ID_Cat`) REFERENCES `Catalysts`(`ID`));'''

        sqlCreateSV = '''CREATE TABLE `SV_experiments` (
        `ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `Date`	TEXT NOT NULL,
        `Name`	TEXT NOT NULL,
        `ID_cat`	INTEGER NOT NULL,
        `ID_sol`	INTEGER NOT NULL,
        `Quencher`	TEXT NOT NULL,
        `Num_points`	INTEGER NOT NULL,
        `Slope`	NUMERIC NOT NULL,
        `R2`	NUMERIC NOT NULL,
        `Kq`	INTEGER,
        `Data`	BLOB DEFAULT NULL,
        FOREIGN KEY(`ID_cat`) REFERENCES `Catalysts`(`ID`),
        FOREIGN KEY(`ID_sol`) REFERENCES `Solvents`(`ID`));'''

        sqlInsertFirstSolvent = '''INSERT INTO Solvents(solvent)
        VALUES(?)'''

        sqlInsertFirstCatalyst = '''INSERT INTO Catalysts(catalyst)
        VALUES(?)'''

        sqlInsertFirstLifetime = '''INSERT INTO Lifetime_couples
        (ID_cat, ID_sol) VALUES (
        (SELECT ID FROM Catalysts WHERE catalyst = ?),
        (SELECT ID FROM Solvents WHERE solvent = ?))'''

        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(sqlCreateCatalysts)
                cursor.execute(sqlCreateSolvents)
                cursor.execute(sqlCreateLifetime)
                cursor.execute(sqlCreateAutomation)
                cursor.execute(sqlCreateSV)
                cursor.execute(sqlInsertFirstSolvent, ('MeCN',))
                cursor.execute(sqlInsertFirstCatalyst, ('Ru(bpy)3Cl2',))
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(sqlInsertFirstLifetime, ('Ru(bpy)3Cl2', 'MeCN'))
        except Exception as e:
            messagebox.showerror('Error',
                                 'Error occurred during Table creation:\n{}'.format(e))

        pass

    def PullAutomationData(self, catalyst):
        '''
        returns the data for the automation
        for the outputdatabase GUI
        :return:
        '''

        sql = '''select name,
                        Name_sample,
                        Quenching_code
                from Automation_experiments
                where (ID_cat =
                    (select id from Catalysts where catalyst = (?)))
                    and (Quenching_code = 'blue' or Quenching_code = 'green')'''

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql, catalyst)
            answer = cursor.fetchall()
        return answer

    def PullSVlight(self, data):
        '''
        returns the data to stern-Volmer light data pull request
        :return:
        '''

        sql = '''
        select distinct
            solvent,
            catalyst,
            quencher
        from SV_experiments

        inner join solvents
        on SV_experiments.ID_sol = solvents.id

        inner join Catalysts
        on SV_experiments.ID_cat = catalysts.id

        WHERE
            (ID_cat = (select id from Catalysts where catalyst = (?)))
        and
            (ID_sol = (select id from Solvents where solvent = (?)))
        and
            (R2 > 0.9)
        '''

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            answer = cursor.fetchall()
        return answer

    def PullSVHard(self, data):
        '''
        returns the data to stern-Volmer light data pull request
        :return:
        '''

        sql = '''
        select
            name,
            catalyst,
            solvent,
            quencher,
            round(slope, 3),
            round(KQ, 2),
            round(R2, 4) as r2
        from SV_experiments

        inner join solvents
        on SV_experiments.ID_sol = solvents.id

        inner join Catalysts
        on SV_experiments.ID_cat = catalysts.id

        WHERE
            (ID_cat = (select id from Catalysts where catalyst = (?)))
        and
            (ID_sol = (select id from Solvents where solvent = (?)))
        and
            (R2 > 0.95)
        '''

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            answer = cursor.fetchall()
        return answer

if __name__ == '__main__':

    database = 'Database_Automation2.db'
    databaseCommander = DatabaseHandler(database)

    rows = databaseCommander.PullSVlight(('RA-48', 'DMF'))

    for row in rows:
        print(row)
    print('end')