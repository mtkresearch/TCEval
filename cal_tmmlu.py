import json
import os

import pandas as pd

categories = {
    "STEM": [
        "physics",
        "chemistry",
        "biology",
        "computer science",
        "math",
        "engineering",
    ],
    "humanities": ["history", "philosophy", "law"],
    "social sciences": [
        "politics",
        "culture",
        "economics",
        "geography",
        "psychology",
        "education",
    ],
    "other (business, health, misc.)": ["other", "business", "health"],
}

task_list = [
    "engineering_math",
    "dentistry",
    "traditional_chinese_medicine_clinical_medicine",
    "clinical_psychology",
    "technical",
    "culinary_skills",
    "mechanical",
    "logic_reasoning",
    "real_estate",
    "general_principles_of_law",
    "finance_banking",
    "anti_money_laundering",
    "ttqav2",
    "marketing_management",
    "business_management",
    "organic_chemistry",
    "advance_chemistry",
    "physics",
    "secondary_physics",
    "human_behavior",
    "national_protection",
    "jce_humanities",
    "politic_science",
    "agriculture",
    "official_document_management",
    "financial_analysis",
    "pharmacy",
    "educational_psychology",
    "statistics_and_machine_learning",
    "management_accounting",
    "introduction_to_law",
    "computer_science",
    "veterinary_pathology",
    "accounting",
    "fire_science",
    "optometry",
    "insurance_studies",
    "pharmacology",
    "taxation",
    "education_(profession_level)",
    "economics",
    "veterinary_pharmacology",
    "nautical_science",
    "occupational_therapy_for_psychological_disorders",
    "trust_practice",
    "geography_of_taiwan",
    "physical_education",
    "auditing",
    "administrative_law",
    "basic_medical_science",
    "macroeconomics",
    "trade",
    "chinese_language_and_literature",
    "tve_design",
    "junior_science_exam",
    "junior_math_exam",
    "junior_chinese_exam",
    "junior_social_studies",
    "tve_mathematics",
    "tve_chinese_language",
    "tve_natural_sciences",
    "junior_chemistry",
    "music",
    "education",
    "three_principles_of_people",
    "taiwanese_hokkien",
]
subject2name = {}
subject2category = {}

df = pd.read_csv("subject.tsv", delimiter="\t")
for _, row in df.iterrows():
    if row["subject"] in task_list:
        subject2category[row["subject"]] = row["category"]
        subject2name[row["subject"]] = row["name"]

import glob

dir_path = 'outputs_chat_tmmlu_0shot'

for path in glob.glob(dir_path + '/*'):
    path = path + '/results.json'

    try:
        data = json.load(open(path))['results']
    except:
        continue

    stat = {'STEM': [], "humanities": [], "social sciences": [], "other (business, health, misc.)": []}
    for k in data.keys():
        if not k.startswith('tmmluplus_fewshot-'):
            continue
        subcat = subject2category[k.replace('tmmluplus_fewshot-','')]
        cat = None
        for tmp_cat in categories:
            if subcat in categories[tmp_cat]:
                cat = tmp_cat
                break
        if cat is None:
            print('not found', key)
        stat[cat].append(data[k]['acc,none'])


    import numpy as np

    agg_stat = {k: np.mean(stat[k]) for k in stat}
    print(path)
    print(agg_stat)
    print(np.mean(list(agg_stat.values())))
    print('------------------------')

