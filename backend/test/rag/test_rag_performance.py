import unittest
import pandas as pd

class TestApp(unittest.TestCase):
    def setUp(self):
        file_path = "home_loan_trending_faq.csv"
        self.eval_df = pd.read_csv(file_path)

    def test_faithfulness_evaluation(self):
        faithful_score = 0
        for val in self.eval_df['Faithfulness_Evaluation_Result'].values:
            faithful_score += 1 if val == "Pass" else 0
        total_score = faithful_score * 100 / self.eval_df.shape[0]
        self.assertGreaterEqual(total_score, 85)
    
    def test_relevancy_evaluation(self):
        relevancy_score = 0
        for val in self.eval_df['Relevancy_Evaluation_Result'].values:
            relevancy_score += 1 if val == "Pass" else 0
        total_score = relevancy_score * 100 / self.eval_df.shape[0]
        self.assertGreaterEqual(total_score, 85)