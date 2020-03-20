import operator
import re
from functools import reduce

import scriptures
from django.db.models import Q

from churchcal.management.commands.import_base import ImportCommemorationsBaseCommand
from churchcal.models import MassReading, Proper, Commemoration


class Command(ImportCommemorationsBaseCommand):
    help = "Imports Mass Readings"

    RANGE_NAME = "Mass Readings!A1:G1034"

    def format_reading(self, book, passage):
        passage = "{} {}".format(book, passage)
        try:
            reference = scriptures.extract(passage)[0]
            # print(reference)
        except IndexError:
            return passage
        passage = scriptures.reference_to_string(*reference)
        return passage

    def get_reading_type(self, book, passage):
        if book == "Canticle":
            return "psalm"
        passage = "{} {}".format(book, passage)
        try:
            reference = scriptures.extract(passage)[0]
            book = reference[0]
            testament = reference[5]
            if book in ("Matthew", "Mark", "Luke", "John"):
                return "gospel"
            if book == "Psalms":
                return "psalm"
            if testament == "NT":
                return "epistle"
            return "prophecy"
        except IndexError:
            return "unknown"

    def handle_odd_commeoration(self, code):

        codes = {
            "AllSaints": "All Saints’ Day",
            "AllSaintsSunday": "All Saints' Sunday",
            "Andrew": "Andrew the Apostle",
            "Ascension": "Ascension Day",
            "CanadaDay": "Canada Day (Canada)",
            "Christmas": "The Nativity of our Lord Jesus Christ: Christmas Day",
            "Easter": "Easter Day",
            "EasterEve": "Easter Day",
            "EasterVII": "The Sunday after the Ascension",
            "Ecumenist": "",
            "Ember": "",
            "Epiphany": "The Epiphany: The Manifestation of Christ to the Gentiles",
            "EpiphanyPaenultima": "The Second to Last Sunday of Epiphany: World Mission Sunday, or Sexagesima",
            "EpiphanyUltima": "The Last Sunday of Epiphany: Transfiguration, or Quinquagesima",
            "James": "James the Elder, Apostle",
            "John": "John, Apostle and Evangelist",
            "JohnTheBaptist": "The Beheading of John the Baptist",
            "Joseph": "Joseph, Husband of the Virgin Mary and Guardian of Jesus",
            "Mark": "Mark the Evangelist",
            "Martyr": "",
            "Mary": "The Virgin Mary, Mother of our Lord Jesus Christ",
            "Michael": "Holy Michael and All Angels",
            "MemorialDay": "Memorial Day (United States)",
            "RemembranceDay": "Remembrance Day (Canada)",
            "MissionaryEvangelist": "",
            "Monastic": "",
            "Paul": "Peter and Paul, Apostles",
            "Pentecost": "The Day of Pentecost",
            "Peter": "Confession of Peter the Apostle",
            "ReformerOfTheChurch": "",
            "RenewerOfSociety": "",
            "Rogation": "",
            "TeacherOfTheFaith": "",
            "ThanksgivingUS": "Thanksgiving Day (United States)",
            "ThanksgivingCanada": "Thanksgiving Day (Canada)",
            "Thomas": "Thomas the Apostle",
            "Transfiguration": "The Transfiguration of Our Lord Jesus Christ",
            "TrinitySunday": "Trinity Sunday",
        }

        try:
            name = codes[code]
        except AttributeError:
            return None

        if name:
            try:
                return Commemoration.objects.filter(calendar=self.calendar).get(name=name)
            except Commemoration.DoesNotExist:
                print(name)
                return None

    def get_proper(self, code):
        if "Proper" in code:
            number = code.replace("Proper", "")
            return Proper.objects.filter(calendar=self.calendar).get(number=number)
        return None

    def decode_roman_numeral(self, roman):
        """Calculate the numeric value of a Roman numeral (in capital letters)"""
        try:
            trans = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
            values = [trans[r] for r in roman]
            return sum(val if val >= next_val else -val for val, next_val in zip(values[:-1], values[1:])) + values[-1]
        except (KeyError, IndexError):
            return None

    def number_to_ordinal(self, number):
        ordinals = {
            1: "First",
            2: "Second",
            3: "Third",
            4: "Fourth",
            5: "Fifth",
            6: "Sixth",
            7: "Seventh",
            8: "Eighth",
            9: "Ninth",
            10: "Tenth",
        }

        try:
            return ordinals[number]
        except KeyError:
            return None

    def get_numbered_commemoration(self, code, season):
        if season not in code:
            return None
        code = code.replace(season, "")
        if code:
            number = self.decode_roman_numeral(code)
            if number:
                ordinal = self.number_to_ordinal(number)
                if ordinal:
                    commemoration = (
                        Commemoration.objects.filter(calendar=self.calendar, name__icontains=ordinal)
                        .filter(name__icontains=season)
                        .first()
                    )
                    if commemoration:
                        return commemoration
        return None

    def get_commemoration(self, code):
        original_code = code
        proper = self.get_proper(code)
        if proper:
            return None
        for season in ["Advent", "Easter", "Christmas", "Epiphany", "Lent", "Easter"]:
            numbered_commemoration = self.get_numbered_commemoration(code, season)
            if numbered_commemoration:
                return numbered_commemoration

        ordinals = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth")
        code = re.sub("([A-Z])", " \g<0>", code).strip().split(" ")
        try:
            res = (
                Commemoration.objects.filter(calendar=self.calendar)
                .filter(reduce(operator.and_, (Q(name__icontains=x) for x in code)))
                .exclude(reduce(operator.and_, (Q(name__icontains=x) for x in ordinals)))
                .get()
            )
            if res:
                return res
        except (Commemoration.MultipleObjectsReturned, Commemoration.DoesNotExist):
            pass

        res = self.handle_odd_commeoration(original_code)
        if res:
            return res
        return None

    def import_dates(self):

        MassReading.objects.filter(calendar=self.calendar).delete()
        self.values.pop(0)
        self.values.pop(0)
        for i, row in enumerate(self.values):
            reading = MassReading()
            reading.calendar = self.calendar
            reading.long_citation = self.format_reading(row[4], row[5])
            if len(row) > 6:
                reading.short_citation = self.format_reading(row[4], row[6])
            reading.service = row[1]
            reading.years = row[3].replace(",", "")
            reading.reading_type = self.get_reading_type(row[4], row[5])
            reading.proper = self.get_proper(row[0])
            reading.commemoration = self.get_commemoration(row[0])
            reading.abbreviation = row[0]
            reading.save()
            # print(row[0])
