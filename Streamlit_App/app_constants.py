from pathlib import Path
import os

# 1. Constants

list_LLM_providers = [":rainbow[**OpenAI**]", "**Google Generative AI**"]

list_Assistant_Languages = [
    "english",
    "french",
    "spanish",
    "german",
    "russian",
    "chinese",
    "arabic",
    "portuguese",
    "italian",
    "Japanese",
]

TMP_DIR = Path(__file__).resolve().parent.joinpath("data", "tmp")


#  2. PROMPT TEMPLATES

templates = {}

# 2.1 Contact information Section
templates[
    "Contact__information"
] = """Extract and evaluate the contact information. \
Output a dictionary with the following keys:
- candidate__name 
- candidate__title
- candidate__location
- candidate__email
- candidate__phone
- candidate__social_media: Extract a list of all social media profiles, blogs or websites.
- evaluation__ContactInfo: Evaluate in {language} the contact information.
- score__ContactInfo: Rate the contact information by giving a score (integer) from 0 to 100.
"""

# 2.2. Summary Section
templates[
    "CV__summary"
] = """Extract the summary and/or objective section. This is a separate section of the resume. \
If the resume doed not contain a summary and/or objective section, then simply write "unknown"."""

# 2.3. WORK Experience Section

templates[
    "Work__experience"
] = """Extract all work experiences. For each work experience: 
1. Extract the job title.
2. Extract the company.  
3. Extract the start date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
4. Extract the end date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
5. Create a dictionary with the following keys: job__title, job__company, job__start_date, job__end_date.

Format your response as a list of dictionaries.
"""

# 2.4. Projects Section
templates[
    "CV__Projects"
] = """Include any side projects outside the work experience. 
For each project:
1. Extract the title of the project. 
2. Extract the start date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
3. Extract the end date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
4. Create a dictionary with the following keys: project__title, project__start_date, project__end_date.

Format your response as a list of dictionaries.
"""

# 2.5. Education Section
templates[
    "CV__Education"
] = """Extract all educational background and academic achievements.
For each education achievement:
1. Extract the name of the college or the high school. 
2. Extract the earned degree. Honors and achievements are included.
3. Extract the start date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
4. Extract the end date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
5. Create a dictionary with the following keys: edu__college, edu__degree, edu__start_date, edu__end_date.

Format your response as a list of dictionaries.
"""

templates[
    "Education__evaluation"
] = """Your task is to perform the following actions:  
1. Rate the quality of the Education section by giving an integer score from 0 to 100. 
2. Evaluate (in three sentences and in {language}) the quality of the Education section.
3. Format your response as a dictionary with the following keys: score__edu, evaluation__edu.
"""

# 2.6. Skills
templates[
    "candidate__skills"
] = """Extract the list of soft and hard skills from the skill section. Output a list.
The skill section is a separate section.
"""

templates[
    "Skills__evaluation"
] = """Your task is to perform the following actions: 
1. Rate the quality of the Skills section by giving an integer score from 0 to 100.
2. Evaluate (in three sentences and in {language}) the quality of the Skills section.
3. Format your response as a dictionary with the following keys: score__skills, evaluation__skills.
"""

# 2.7. Languages
templates[
    "CV__Languages"
] = """Extract all the languages that the candidate can speak. For each language:
1. Extract the language.
2. Extract the fluency. If the fluency is not available, then simply write "unknown".
3. Create a dictionary with the following keys: spoken__language, language__fluency.

Format your response as a list of dictionaries.
"""

templates[
    "Languages__evaluation"
] = """ Your task is to perform the following actions: 
1. Rate the quality of the language section by giving an integer score from 0 to 100.
2. Evaluate (in three sentences and in {language}) the quality of the language section.
3. Format your response as a dictionary with the following keys: score__language,evaluation__language.
"""

# 2.8. Certifications
templates[
    "CV__Certifications"
] = """Extraction of all certificates other than education background and academic achievements. \
For each certificate: 
1. Extract the title of the certification. 
2. Extract the name of the organization or institution that issues the certification.
3. Extract the date of certification and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
4. Extract the certification expiry date and output it in the following format: \
YYYY/MM/DD or YYYY/MM or YYYY (depending on the availability of the day and month).
5. Extract any other information listed about the certification. if not found, then simply write "unknown".
6. Create a dictionary with the following keys: certif__title, certif__organization, certif__date, certif__expiry_date, certif__details.

Format your response as a list of dictionaries.
"""

templates[
    "Certif__evaluation"
] = """Your task is to perform the following actions: 
1. Rate the certifications by giving an integer score from 0 to 100.
2. Evaluate (in three sentences and in {language}) the certifications and the quality of the text.
3. Format your response as a dictionary with the following keys: score__certif,evaluation__certif.
"""


# 3. PROMPTS

PROMPT_IMPROVE_SUMMARY = """Your are given a resume (delimited by <resume></resume>) \
and a summary (delimited by <summary></summary>).
1. In {language}, evaluate the summary (format and content) .
2. Rate the summary by giving an integer score from 0 to 100. \
If the summary is "unknown", the score is 0.
3. In {language}, strengthen the summary. The summary should not exceed 5 sentences. \
If the summary is "unknown", generate a strong summary in {language} with no more than 5 sentences. \
Please include: years of experience, top skills and experiences, some of the biggest achievements, and finally an attractive objective.
4. Format your response as a dictionary with the following keys: evaluation__summary, score__summary, CV__summary_enhanced.

<summary>
{summary}
</summary>
------
<resume>
{resume}
</resume>
"""

PROMPT_IMPROVE_WORK_EXPERIENCE = """you are given a work experience text delimited by triple backticks.
1. Rate the quality of the work experience text by giving an integer score from 0 to 100. 
2. Suggest in {language} how to make the work experience text better and stronger.
3. Strengthen the work experience text to make it more appealing to a recruiter in {language}. \
Provide additional details on responsibilities and quantify results for each bullet point. \
Format your text as a string in {language}.
4. Format your response as a dictionary with the following keys: "Score__WorkExperience", "Comments__WorkExperience" and "Improvement__WorkExperience".

Work experience text: ```{text}```
"""

PROMPT_IMPROVE_PROJECT = """you are given a project text delimited by triple backticks.
1. Rate the quality of the project text by giving an integer score from 0 to 100. 
2. Suggest in {language} how to make the project text better and stronger.
3. Strengthen the project text to make it more appealing to a recruiter in {language}, \
including the problem, the approach taken, the tools used and quantifiable results. \
Format your text as a string in {language}.
4. Format your response as a dictionary with the following keys: Score__project, Comments__project, Improvement__project.

project text: ```{text}```
"""

PROMPT_EVALUATE_RESUME = """You are given a resume delimited by triple backticks. 
1. Provide an overview of the resume in {language}.
2. Provide a comprehensive analysis of the three main strengths of the resume in {language}. \
Format the top 3 strengths as string containg three bullet points.
3. Provide a comprehensive analysis of the three main weaknesses of the resume in {language}. \
Format the top 3 weaknesses as string containg three bullet points.
4. Format your response as a dictionary with the following keys: resume_cv_overview, top_3_strengths, top_3_weaknesses.

The strengths and weaknesses lie in the format, style and content of the resume.

Resume: ```{text}```
"""
