from unittest import TestCase
from src.analysis.analysis import DataAnalysis


class TestDataAnalysis(TestCase):
    data_analysis = DataAnalysis()

    def test_hub_actor_connections(self):
        self.assertEqual({'Bruce Willis': 303}, self.data_analysis.hub_actor_connections(1))
        self.assertEqual({}, self.data_analysis.hub_actor_connections(-100))
        self.assertEqual({'Brenda Vaccaro': 50, 'Paul Newman': 58, 'Faye Dunaway': 107,
                          'Jack Warden': 116, 'Bruce Willis': 303},
                         self.data_analysis.hub_actor_connections(5))

    def test_age_gross_relation(self):
        self.assertEqual(20, min(self.data_analysis.age_gross_relation()))
        self.assertEqual(94, max(self.data_analysis.age_gross_relation()))
        self.assertEqual(65, len(self.data_analysis.age_gross_relation()))
        self.assertEqual(563000000, self.data_analysis.age_gross_relation()[30])

    def test_year_gross_relation(self):
        self.assertEqual(67, len(self.data_analysis.year_gross_relation()))
        self.assertEqual(1949, min(self.data_analysis.year_gross_relation()))
        self.assertEqual(2017, max(self.data_analysis.year_gross_relation()))
        self.assertEqual(897209322, self.data_analysis.year_gross_relation()[2006])
