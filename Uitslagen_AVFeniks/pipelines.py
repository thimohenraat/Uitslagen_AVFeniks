# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import sqlite3


# class SQLlitePipeline:
#     def __init__(self):
#         self.con = sqlite3.connect("uitslagen.db")
#         self.cur = self.con.cursor()
#         self.create_table()

#     def create_table(self):
#         self.cur.execute("""DROP TABLE IF EXISTS Wedstrijd""")
#         self.cur.execute(
#             """
#             CREATE TABLE Wedstrijd(
#                 wedstrijd text, datum text, plaats text, onderdeel text
#             );
#             """
#         )
#         self.cur.execute("""DROP TABLE IF EXISTS Onderdeel""")
#         self.cur.execute(
#             """
#             CREATE TABLE Onderdeel(
#                 onderdeel text, atleet text
#             );
#             """
#         )
#         self.cur.execute("""DROP TABLE IF EXISTS Atleet""")
#         self.cur.execute(
#             """
#             CREATE TABLE Atleet(
#                 atleet text, categorie text, uitslag text
#             );
#             """
#         )
#         self.cur.execute("""DROP TABLE IF EXISTS Uitslag""")
#         self.cur.execute(
#             """
#             CREATE TABLE Uitslag(
#                 resultaat text, onderdeel text, wind text
#             );
#             """
#         )

#     def process_item(self, item, spider):
#         self.cur.execute(
#             """
#             INSERT INTO Wedstrijd VALUES(?,?,?,?)
#             """,
#             (
#                 item["wedstrijd"][0],
#                 item["datum"][0],
#                 item["plaats"][0],
#                 item["onderdeel"][0],
#             ),
#         )
#         self.cur.execute(
#             """
#             INSERT INTO Onderdeel VALUES(?,?)
#             """,
#             (item["onderdeel"][0], item["atleet"][0]),
#         )
#         self.cur.execute(
#             """
#             INSERT INTO Atleet VALUES(?,?,?)
#             """,
#             (item["atleet"][0], item["categorie"][0], item["uitslag"][0]),
#         )
#         self.cur.execute(
#             """
#             INSERT INTO Uitslag VALUES(?,?,?)
#             """,
#             (item["resultaat"][0], item["onderdeel"][0], item["wind"][0]),
#         )
#         self.con.commit()
#         return item


# class UitslagenAvfeniksPipeline:
#     def process_item(self, item, spider):
#         return item
