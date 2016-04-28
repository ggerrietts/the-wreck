from unittest import TestCase
import models as m


class Test_Subject(TestCase):

    def test_work_count_null(self):
        res = m.Subject.parse({'id': 15, 'name': "gaudy beads"}, 123)
        self.assertEqual(res, [
            m.Insert('tw_subject', (15,), "INSERT INTO tw_subject (id, name, work_count) VALUES (15, 'gaudy beads', NULL);\n"),
            m.Insert('tw_subject_tree', (123, 15), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (123, 15, NULL);\n")
        ])

    def test_single(self):
        res = m.Subject.parse({'id': 15, 'name': "gaudy beads", 'workCount': 5}, 123)
        self.assertEqual(res, [
            m.Insert('tw_subject', (15,), "INSERT INTO tw_subject (id, name, work_count) VALUES (15, 'gaudy beads', 5);\n"),
            m.Insert('tw_subject_tree', (123, 15), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (123, 15, NULL);\n")
        ])

    def test_nested(self):
        res = m.Subject.parse({
            'id': 15,
            'name': "gaudy beads",
            'workCount': 5,
            'children': [{
                'id': 17,
                'name': "blue beads"
            }, {
                'id': 14,
                'name': 'glass beads',
                'workCount': 3
        }]}, 123)
        self.assertEqual(res, [
            m.Insert('tw_subject', (15,), "INSERT INTO tw_subject (id, name, work_count) VALUES (15, 'gaudy beads', 5);\n"),
            m.Insert('tw_subject_tree', (123, 15), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (123, 15, NULL);\n"),
            m.Insert('tw_subject', (17,), "INSERT INTO tw_subject (id, name, work_count) VALUES (17, 'blue beads', NULL);\n"),
            m.Insert('tw_subject_tree', (123, 17), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (123, 17, 15);\n"),
            m.Insert('tw_subject', (14,), "INSERT INTO tw_subject (id, name, work_count) VALUES (14, 'glass beads', 3);\n"),
            m.Insert('tw_subject_tree', (123, 14), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (123, 14, 15);\n"),
        ])

    def test_apostrophes(self):
        res = m.Subject.parse({'id': 15, 'name': "glazier's tongs", 'workCount': 5}, work_id=123)
        self.assertEqual(res, [
            m.Insert('tw_subject', (15,), "INSERT INTO tw_subject (id, name, work_count) VALUES (15, 'glazier''s tongs', 5);\n"),
            m.Insert('tw_subject_tree', (123, 15), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (123, 15, NULL);\n")
        ])


class Test_Movement(TestCase):

    def test_with_era_no_wc(self):
        res = m.Movement.parse({'id': 12, 'name': "surrealism", 'era': {"name": "modernity"}})
        self.assertEqual(res, [
            m.Insert('tw_movement', (12,), "INSERT INTO tw_movement (id, name, era, work_count) VALUES (12, 'surrealism', 'modernity', NULL);\n")
        ])

    def test_with_era_and_wc(self):
        res = m.Movement.parse({'id': 12, 'name': "surrealism", 'workCount': 3, 'era': {"name": "modernity"}})
        self.assertEqual(res, [
            m.Insert('tw_movement', (12,), "INSERT INTO tw_movement (id, name, era, work_count) VALUES (12, 'surrealism', 'modernity', 3);\n")
        ])

    def test_with_no_era_no_wc(self):
        res = m.Movement.parse({'id': 12, 'name': "surrealism"})
        self.assertEqual(res, [
            m.Insert('tw_movement', (12,), "INSERT INTO tw_movement (id, name, era, work_count) VALUES (12, 'surrealism', '', NULL);\n")
        ])

    def test_with_linked_artist(self):
        res = m.Movement.parse({'id': 12, 'name': "surrealism"}, artist=123)
        self.assertEqual(res, [
            m.Insert('tw_movement', (12,), "INSERT INTO tw_movement (id, name, era, work_count) VALUES (12, 'surrealism', '', NULL);\n"),
            m.Insert('tw_artist_to_movement', (123, 12), 'INSERT INTO tw_artist_to_movement (artist_id, movement_id) VALUES (123, 12);\n')
        ])

    def test_with_linked_work(self):
        res = m.Movement.parse({'id': 12, 'name': "surrealism"}, work=123)
        self.assertEqual(res, [
            m.Insert('tw_movement', (12,), "INSERT INTO tw_movement (id, name, era, work_count) VALUES (12, 'surrealism', '', NULL);\n"),
            m.Insert('tw_work_to_movement', (123, 12), 'INSERT INTO tw_work_to_movement (work_id, movement_id) VALUES (123, 12);\n')
        ])


class Test_CatalogGroup(TestCase):
    def test_cg(self):
        res = m.CatalogGroup.parse({
            "accessionRanges": "D09058-D09206; D40818; D41541",
            "completeStatus": "COMPLETE",
            "finbergNumber": "CXXIX",
            "groupType": "Turner Sketchbook",
            "id": 65772,
            "shortTitle": "Woodcock Shooting Sketchbook"})
        self.assertEqual(res, [
            m.Insert('tw_catalog_group', (65772,),
                     "INSERT INTO tw_catalog_group (id, accession_ranges, short_title, group_type) VALUES "
                     "(65772, 'D09058-D09206; D40818; D41541', 'Woodcock Shooting Sketchbook', 'Turner Sketchbook');\n")
        ])

class Test_Artist(TestCase):

    artist = {
        "activePlaceCount": 0,
          "birth": {
            "place": {
              "name": "M\u00e1laga, Espa\u00f1a",
              "placeName": "M\u00e1laga",
              "placeType": "inhabited_place"
            },
            "time": {
              "startYear": 1881
            }
          },
          "birthYear": 1881,
          "date": "1881\u20131973",
          "death": {
            "place": {
              "name": "Mougins, France",
              "placeName": "Mougins",
              "placeType": "inhabited_place"
            },
            "time": {
              "startYear": 1973
            }
          },
          "fc": "Pablo Picasso",
          "gender": "Male",
          "id": 1767,
          "mda": "Picasso, Pablo",
          "movements": [ {
              "era": {
                "id": 8,
                "name": "20th century 1900-1945"
              },
              "id": 299,
              "name": "Cubism"
            }, {
              "era": {
                "id": 8,
                "name": "20th century 1900-1945"
              },
              "id": 1685,
              "name": "Return to Order"
          } ],
          "startLetter": "P",
          "totalWorks": 46,
          "url": "http://www.tate.org.uk/art/artists/pablo-picasso-1767"
    }

    def test_complex(self):
        res = m.Artist.parse(self.artist)
        self.assertEqual(res, [
            m.Insert('tw_artist', (1767,), "INSERT INTO tw_artist (id, name, gender, born, died, birthplace, url, total_works) VALUES (1767, 'Pablo Picasso', 'Male', '1881', '1973', 'M\u00e1laga', 'http://www.tate.org.uk/art/artists/pablo-picasso-1767', 46);\n"),
            m.Insert('tw_movement', (299,), "INSERT INTO tw_movement (id, name, era, work_count) VALUES (299, 'Cubism', '20th century 1900-1945', NULL);\n"),
            m.Insert('tw_artist_to_movement', (1767, 299), 'INSERT INTO tw_artist_to_movement (artist_id, movement_id) VALUES (1767, 299);\n'),
            m.Insert('tw_movement', (1685,), "INSERT INTO tw_movement (id, name, era, work_count) VALUES (1685, 'Return to Order', '20th century 1900-1945', NULL);\n"),
            m.Insert('tw_artist_to_movement', (1767, 1685), 'INSERT INTO tw_artist_to_movement (artist_id, movement_id) VALUES (1767, 1685);\n'),
        ])


class Test_Work(TestCase):
    picasso = {
          "acno": "N04683",
          "acquisitionYear": 1933,
          "all_artists": "Pablo Picasso",
          "catalogueGroup": {},
          "classification": "painting",
          "contributorCount": 1,
          "contributors": [
            {
              "birthYear": 1881,
              "date": "1881\u20131973",
              "displayOrder": 1,
              "fc": "Pablo Picasso",
              "gender": "Male",
              "id": 1767,
              "mda": "Picasso, Pablo",
              "role": "artist",
              "startLetter": "P"
            }
          ],
          "creditLine": "Purchased with assistance from the Contemporary Art Society 1933",
          "dateRange": {
            "endYear": 1901,
            "startYear": 1901,
            "text": "1901"
          },
          "dateText": "1901",
          "depth": "",
          "dimensions": "support: 651 x 489 mm\r\nframe: 916 x 758 x 103 mm",
          "foreignTitle": "Fleurs",
          "groupTitle": None,
          "height": "489",
          "id": 11854,
          "inscription": None,
          "medium": "Oil paint on canvas",
          "movementCount": 0,
          "subjectCount": 2,
          "subjects": {
            "children": [
              {
                "children": [
                  {
                    "children": [
                      {
                        "id": 269,
                        "name": "flower"
                      }
                    ],
                    "id": 72,
                    "name": "plants and flowers"
                  }
                ],
                "id": 60,
                "name": "nature"
              },
              {
                "children": [
                  {
                    "children": [
                      {
                        "id": 1461,
                        "name": "vase"
                      }
                    ],
                    "id": 170,
                    "name": "vessels and containers"
                  }
                ],
                "id": 78,
                "name": "objects"
              }
            ],
            "id": 1,
            "name": "subject"
          },
          "thumbnailCopyright": "\u00a9 Succession Picasso/DACS 2014",
          "thumbnailUrl": "http://www.tate.org.uk/art/images/work/N/N04/N04683_8.jpg",
          "title": "Flowers",
          "units": "mm",
          "url": "http://www.tate.org.uk/art/artworks/picasso-flowers-n04683",
          "width": "651"
        }

    turner = {
          "acno": "D41541",
          "acquisitionYear": 1856,
          "all_artists": "Joseph Mallord William Turner",
          "catTextResId": 1145746,
          "catalogueGroup": {
            "accessionRanges": "D09058-D09206; D40818; D41541",
            "completeStatus": "COMPLETE",
            "finbergNumber": "CXXIX",
            "groupType": "Turner Sketchbook",
            "id": 65772,
            "shortTitle": "Woodcock Shooting Sketchbook"
          },
          "classification": "on paper, unique",
          "contributorCount": 1,
          "contributors": [
            {
              "birthYear": 1775,
              "date": "1775\u20131851",
              "displayOrder": 1,
              "fc": "Joseph Mallord William Turner",
              "gender": "Male",
              "id": 558,
              "mda": "Turner, Joseph Mallord William",
              "role": "artist",
              "startLetter": "T"
            }
          ],
          "creditLine": "Accepted by the nation as part of the Turner Bequest 1856",
          "dateRange": {
            "endYear": 1813,
            "startYear": 1812,
            "text": "c.1812-13"
          },
          "dateText": "c.1812\u201313",
          "depth": "",
          "dimensions": "support: 110 x 178 mm",
          "finberg": "CXXIX 46",
          "foreignTitle": None,
          "groupTitle": "Woodcock Shooting Sketchbook",
          "height": "178",
          "id": 124602,
          "inscription": None,
          "medium": None,
          "movementCount": 0,
          "pageNumber": 95,
          "subjectCount": 0,
          "thumbnailCopyright": None,
          "thumbnailUrl": None,
          "title": "A Track Rising through Trees on Otley Chevin",
          "units": "mm",
          "url": "http://www.tate.org.uk/art/artworks/turner-a-track-rising-through-trees-on-otley-chevin-d41541",
          "width": "110"
        }

    def test_picasso(self):
        res = m.Work.parse(self.picasso)
        expected = [
            m.Insert('tw_work', (11854,), "INSERT INTO tw_work (id, accession_number, acquisition_year, catalog_group_id, classification, credit_line, date_text, medium, title, url) "
                     "VALUES (11854, 'N04683', '1933', NULL, 'painting', 'Purchased with assistance from the Contemporary Art Society 1933', '1901', "
                     "'Oil paint on canvas', 'Flowers', 'http://www.tate.org.uk/art/artworks/picasso-flowers-n04683');\n"),
            m.Insert('tw_work_to_artist', (11854, 1767), "INSERT INTO tw_work_to_artist (work_id, artist_id) VALUES (11854, 1767);\n"),
            m.Insert('tw_subject', (1,), "INSERT INTO tw_subject (id, name, work_count) VALUES (1, 'subject', NULL);\n"),
            m.Insert('tw_subject_tree', (11854, 1), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (11854, 1, NULL);\n"),
            m.Insert('tw_subject', (60,), "INSERT INTO tw_subject (id, name, work_count) VALUES (60, 'nature', NULL);\n"),
            m.Insert('tw_subject_tree', (11854, 60), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (11854, 60, 1);\n"),
            m.Insert('tw_subject', (72,), "INSERT INTO tw_subject (id, name, work_count) VALUES (72, 'plants and flowers', NULL);\n"),
            m.Insert('tw_subject_tree', (11854, 72), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (11854, 72, 60);\n"),
            m.Insert('tw_subject', (269,), "INSERT INTO tw_subject (id, name, work_count) VALUES (269, 'flower', NULL);\n"),
            m.Insert('tw_subject_tree', (11854, 269), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (11854, 269, 72);\n"),
            m.Insert('tw_subject', (78,), "INSERT INTO tw_subject (id, name, work_count) VALUES (78, 'objects', NULL);\n"),
            m.Insert('tw_subject_tree', (11854, 78), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (11854, 78, 1);\n"),
            m.Insert('tw_subject', (170,), "INSERT INTO tw_subject (id, name, work_count) VALUES (170, 'vessels and containers', NULL);\n"),
            m.Insert('tw_subject_tree', (11854, 170), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (11854, 170, 78);\n"),
            m.Insert('tw_subject', (1461,), "INSERT INTO tw_subject (id, name, work_count) VALUES (1461, 'vase', NULL);\n"),
            m.Insert('tw_subject_tree', (11854, 1461), "INSERT INTO tw_subject_tree (work_id, subject_id, parent_id) VALUES (11854, 1461, 170);\n"),
        ]
        self.assertEqual(res, expected)

    def test_turner(self):
        res = m.Work.parse(self.turner)
        expected = [
            m.Insert('tw_catalog_group', (65772,),
                     "INSERT INTO tw_catalog_group (id, accession_ranges, short_title, group_type) VALUES "
                     "(65772, 'D09058-D09206; D40818; D41541', 'Woodcock Shooting Sketchbook', 'Turner Sketchbook');\n"),
            m.Insert('tw_work', (124602,),
                     "INSERT INTO tw_work (id, accession_number, acquisition_year, catalog_group_id, classification, credit_line, date_text, medium, title, url) "
                     "VALUES (124602, 'D41541', '1856', 65772, 'on paper, unique', 'Accepted by the nation as part of the Turner Bequest 1856', 'c.1812\u201313', "
                     "'', 'A Track Rising through Trees on Otley Chevin', 'http://www.tate.org.uk/art/artworks/turner-a-track-rising-through-trees-on-otley-chevin-d41541');\n"),
            m.Insert('tw_work_to_artist', (124602, 558), "INSERT INTO tw_work_to_artist (work_id, artist_id) VALUES (124602, 558);\n"),
        ]
        self.assertEqual(res, expected)
