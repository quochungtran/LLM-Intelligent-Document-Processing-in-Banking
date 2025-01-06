from src.rag.rag_flow import bot_rag_answer_message
import pandas as pd
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import FaithfulnessEvaluator
from llama_index.core.evaluation import RelevancyEvaluator

data = {
    "collections": [
        {
            "category": "market_trends",
            "questions": [
                "What were the key mortgage market trends in 2024?",
                "How did mortgage interest rates fluctuate throughout 2024?",
                "What factors influenced the rise in mortgage rates during 2024?",
                "How did the Federal Reserve's policies impact mortgage rates in 2024?",
                "What was the average 30-year fixed mortgage rate at the end of 2024?",
                "How did high mortgage rates affect homebuyer affordability in 2024?",
                "What regions experienced the most significant changes in home prices in 2024?",
                "How did the housing inventory levels change over the course of 2024?",
                "What was the impact of rising home prices on first-time buyers in 2024?",
                "How did the 'rate-lock effect' influence housing inventory in 2024?",
                "What predictions were made for the housing market in 2025?",
                "How did the increase in stamp duty affect the housing market in 2024?",
                "What was the impact of high mortgage rates on home sales volume in 2024?",
                "How did the labor market's performance relate to the housing market in 2024?",
                "What role did inflation play in shaping the mortgage market in 2024?",
                "How did the construction of new homes trend during 2024?",
                "What were the main challenges faced by homebuyers in 2024?",
                "How did the rental market perform in comparison to the housing market in 2024?",
                "What was the effect of economic uncertainties on the housing market in 2024?",
                "How did government policies influence the mortgage market in 2024?",
                "What strategies did sellers adopt in response to market conditions in 2024?",
                "How did the demand for refinancing change throughout 2024?",
                "What was the impact of high mortgage rates on housing affordability in 2024?",
                "How did the 'rate-lock effect' contribute to reduced housing inventory in 2024?",
                "What were the regional disparities in housing market performance in 2024?",
                "How did first-time buyers navigate the housing market challenges in 2024?",
                "What were the implications of increased stamp duty on landlords in 2024?",
                "How did the anticipated stamp duty deadline in April 2025 influence market activity in 2024?",
                "What advice was given to sellers regarding pricing strategies in 2024?",
                "How did the Federal Reserve's interest rate cuts in 2024 affect mortgage rates?",
                "What was the relationship between U.S. Treasury yields and mortgage rates in 2024?",
                "How did the strong U.S. economy contribute to rising mortgage rates in 2024?",
                "What was the impact of high mortgage rates on housing market activity in 2024?",
                "How did the combination of high mortgage rates and rising home prices affect buyers in 2024?",
                "What were the predictions for mortgage rates in 2025?",
                "How did the Federal Reserve's monetary policies aim to control inflation in 2024?",
                "What was the effect of high shelter costs on the Consumer Price Index in 2024?",
                "How did the Federal Reserve's rate cuts in 2024 influence the housing market?",
                "What were the challenges faced by winter home buyers due to spiking mortgage rates in 2024?",
                "How did the housing market gridlock caused by low-rate mortgages impact buyers in 2024?",
                "What was the median loan amount for FHA and VA loans in 2023?",
                "How did the reporting volume threshold affect HMDA data in 2023?",
                "How did rising interest rates influence home loan denial rates in 2023?",
                "What were the major factors leading to the decline in refinance applications in 2023?",
                "How did the number of HELOC originations and applications change in 2023?",
                "What proportion of loans in 2023 involved paying discount points?",
                "How did refinance loans differ between conventional and jumbo loans in 2023?",
                "What was the share of refinance loans for Black borrowers in 2023?",
                "What were the major differences in home loan costs for properties in high-income neighborhoods?"
            ]
        },
        {
            "category": "eligibility",
            "questions": [
                "What are the minimum mortgage requirements for 2025?",
                "What is the minimum credit score needed for an FHA loan?",
                "How much down payment is required for a conventional loan?",
                "What are the debt-to-income (DTI) ratio requirements for different loan types?",
                "Are there specific income requirements to qualify for a mortgage?",
                "How do employment history and stability affect mortgage eligibility?",
                "What types of documentation are required during the mortgage application process?",
                "How does one's credit history impact mortgage approval chances?",
                "What are the property requirements for FHA loans?",
                "Are there any specific requirements for self-employed individuals seeking a mortgage?",
                "What steps can I take to improve my chances of qualifying for a home loan?",
                "Is a 20 percentages down payment mandatory to qualify for a mortgage?",
                "How does getting pre-approved for a loan benefit the home-buying process?",
                "What role do assets and savings play in mortgage qualification?",
                "Can I qualify for a home loan with existing debt?",
                "How do lenders assess my repayment capacity?",
                "What is the significance of the loan-to-value (LTV) ratio in mortgage approval?",
                "How does my current rent payment history influence mortgage eligibility?",
                "What impact do recent large deposits have on my mortgage application?",
                "Are there special loan programs available for first-time homebuyers?",
                "What factors determine my home loan eligibility?",
                "How does my age affect my eligibility for a home loan?",
                "Can adding a co-applicant enhance my loan eligibility?",
                "What is the role of a credit score in determining home loan eligibility?",
                "How do fixed monthly financial obligations impact my loan eligibility?",
                "What is a home loan eligibility calculator, and how can it help me?",
                "How does the tenure of the loan affect my eligibility and EMI amounts?",
                "What are the benefits of having a steady income flow and regular savings when applying for a home loan?",
                "How do lenders evaluate my financial position during the loan application process?",
                "What steps can I take if my home loan application is rejected due to eligibility issues?"
            ]
        },
        {
            "category": "financial_choice",
            "questions": [
                "What factors should I consider when making a major financial decision like buying a home?",
                "How do I evaluate whether renting or buying a home is the better financial option for me?",
                "What are the key differences between short-term and long-term financial decisions?",
                "How does my credit score impact major financial choices like home loans or renting?",
                "What is the role of interest rates in making financial decisions?",
                "How can I balance immediate financial needs with long-term financial goals?",
                "What are the risks of taking on too much debt for financial choices like home loans?",
                "How can I determine the affordability of a financial decision, such as buying a property?",
                "What strategies can I use to save for a major financial milestone, like purchasing a home?",
                "What are the benefits and drawbacks of refinancing or transferring a loan?",
                "How do economic trends influence individual financial decisions?",
                "What is the significance of tax benefits when considering financial options like home loans?",
                "What role does inflation play in evaluating financial choices like renting vs. owning?",
                "How can I compare the total cost of ownership for a home versus the cost of renting?",
                "What tools or calculators can help me assess the financial implications of a decision?",
                "How do I account for future financial uncertainties when making large commitments?",
                "What are the most common mistakes people make when choosing between renting and buying?",
                "How does having dependents or a family impact financial choices like homeownership?",
                "What are the pros and cons of diversifying my financial investments instead of buying property?",
                "How do lifestyle preferences factor into major financial choices, such as owning or renting a home",   
                "What is a home loan balance transfer?",
                "What is a top-up loan on an existing home loan?",
                "How can a home loan balance transfer benefit me financially?",
                "What are the advantages of opting for a top-up loan?",
                "Which option is better for accessing additional funds: balance transfer or top-up loan?",
                "Are there any processing fees associated with home loan balance transfers?",
                "Can I consolidate multiple loans through a home loan balance transfer?",
                "What factors should I consider when choosing between a balance transfer and a top-up loan?",
                "How does my credit profile affect eligibility for balance transfers and top-up loans?",
                "Is it possible to reduce interest costs with a home loan balance transfer?",
                "What are the benefits of taking a home loan for an under-construction property?",
                "How do under-construction property prices compare to ready-to-move-in homes?",
                "What tax benefits are available for home loans on under-construction properties?",
                "Can I claim tax deductions on interest paid during the construction period?",
                "What is the potential for property value appreciation in under-construction projects?",
                "How do flexible payment schedules work for under-construction property loans?",
                "Are there higher resale values associated with newly constructed properties?",
                "What options do buyers have when selecting units in under-construction projects?",
                "How does investing in an under-construction property impact long-term financial gains?",
                "What considerations should be made before purchasing an under-construction property?",
                "What are the financial advantages of buying a home over renting?",
                "How does renting compare to homeownership in terms of monthly expenses?",
                "What long-term benefits does homeownership offer compared to renting?",
                "How does the stability of monthly payments differ between renting and owning a home?"
            ]
        },
        {
            "category": "refinancing",
            "questions": [
                # Requirements for Home Loan Refinancing
                "What is home loan refinancing, and how does it work?",
                "What documents are typically required to refinance a home loan?",
                "How does my credit history affect my eligibility for refinancing?",
                "Can I refinance my mortgage if I have a fixed-rate loan?",
                "What are the eligibility criteria for home loan refinancing?",
                "How does my current debt-to-income ratio impact my chances of refinancing?",
                "Can I refinance if my property is located in a high-demand area?",
                "What role do my assets and liabilities play in the refinancing process?",
                "Why should I review my existing credit card limits before applying for refinancing?",
                "How can practicing good financial management improve my chances of refinancing approval?",
                "What is the maximum loan-to-value (LTV) ratio commonly accepted for refinancing?",
                "Are there additional costs associated with refinancing, and how can I calculate them?",
                "Can I refinance my home loan if I’m self-employed or have a variable income?",
                # When to Refinance Your Mortgage
                "What are the key benefits of refinancing a mortgage?",
                "How can I determine if refinancing will save me money?",
                "When is the best time to refinance my mortgage?",
                "What are the potential downsides of refinancing my mortgage?",
                "How much does refinancing typically cost, and how can I calculate break-even points?",
                "What are the most common reasons homeowners refinance their mortgages?",
                "When is refinancing not a good option?",
                "How do market conditions, such as interest rates, affect refinancing decisions?",
                "Can I refinance to switch from an adjustable-rate mortgage (ARM) to a fixed-rate mortgage?",
                "How does my loan term impact my refinancing options?",
                "Is it worth refinancing if I plan to sell my property soon?",
                "How does refinancing affect my monthly payments and overall loan duration?"
            ]
        }
    ]
}

class HomeloanGoldenData():

    def setUp(self, data, model="gpt-4o"):
        self.history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there! How can I help you today?"}
        ]
        self._data = data
        llm = OpenAI(model=model)
        self.faithful_evaluator  = FaithfulnessEvaluator(llm)
        self.relevancy_evaluator = RelevancyEvaluator(llm)

    def evaluate_golden_dataset(self):
        eval_data = []
        for collection in self._data['collections']:
            for question in collection['questions']:
                print(f"question : {question}")
                rag_response, source_docs = bot_rag_answer_message(self.history, question)    
                faithful_eval_res = self.faithful_evaluator.evaluate(
                    response=rag_response,
                    contexts=[source_docs]
                )
            
                relevancy_eval_res = self.relevancy_evaluator.evaluate(
                    query=question,
                    response=rag_response,
                    contexts=[source_docs]
                )

                eval_data.append({"category": collection['category'], 
                     "question": question, 
                     "rag_response":rag_response,
                     "source": source_docs[:1500],
                     "Faithfulness_Evaluation_Result": "Pass" if faithful_eval_res.passing else "Fail",
                     "Relevancy_Evaluation_Result": "Pass" if relevancy_eval_res.passing else "Fail",
                    }
                )
        return pd.DataFrame(eval_data)

    def rag_performance(self):
        eval_df = self.evaluate_golden_dataset()
        faithfull_score = 0
        relevancy_score = 0
        for val in eval_df['Faithfulness_Evaluation_Result'].values:
            faithfull_score += 1 if val == "Pass" else 0
        for val in eval_df['Relevancy_Evaluation_Result'].values:
            relevancy_score += 1 if val == "Pass" else 0

        print(f"""Faithfulness score {faithfull_score * 100 / eval_df.shape[0]}""")
        print(f"""Relevancy    score {relevancy_score * 100 / eval_df.shape[0]}""")
    
    def to_csv(self, df):
        file_path = "home_loan_trending_faq.csv"
        df.to_csv(file_path, index=False)

golder_data = HomeloanGoldenData()
golder_data.setUp(data)
df_eval     = golder_data.evaluate_golden_dataset()
golder_data.to_csv(df_eval)
