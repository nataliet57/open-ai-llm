import csv
import time
from openai import OpenAI
import pandas as pd

data = pd.read_excel('chat_prompts.xlsx')
data = data.fillna('')

tests = [
    "usmle_1_q",
    "usmle_2_q"
]

test_answers = [
    "usmle_1_a",
    "usmle_2_a"
]


client = OpenAI(
  api_key='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',
)

for item, test in enumerate(tests):
    for idx, row in enumerate(data.itertuples()):
        if idx >= 20:
            break
        with open("results.csv", mode='a', encoding='UTF8') as file:
            writer = csv.writer(file)
            csv_out = []
            csv_out.append(idx)

            prompt = getattr(row, test)
            print(prompt)
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                  messages=[
                    {"role": "system", "content": f"Including an explanation, answer the following question: {prompt}"},
                  ]
            )

            gpt_ans = completion.choices[0].message
            # gpt_ans = "To determine the range within which the true... test"
            # gpt_ans = " ".join(gpt_ans.splitlines())
            # data.at[idx, str(test_answers[item])] = gpt_ans
            csv_out.append(gpt_ans)

            writer.writerow(csv_out)
            print(f"Finished question GPT-3.5's answer: {gpt_ans}")
            print(f"Finished question {idx} for {test}")
            time.sleep(4)

    data.to_excel(f"output_results_{test}.xlsx") 