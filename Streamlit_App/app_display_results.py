import streamlit as st
import markdown
from resume_analyzer import get_section_scores


def custom_markdown(
    text,
    html_tag="p",
    bg_color="white",
    color="black",
    font_size=None,
    text_align="left",
):
    """Customise markdown by specifying custom background colour, text colour, font size, and text alignment.."""

    style = f'style="background-color:{bg_color};color:{color};font-size:{font_size}px; \
text-align: {text_align};padding: 25px 25px 25px 25px;border-radius:2%;"'

    body = f"<{html_tag} {style}> {text}</{html_tag}>"

    st.markdown(body, unsafe_allow_html=True)
    st.write("")


def set_background_color(score):
    """Set background color based on score."""
    if score >= 80:
        bg_color = "#D4F1F4"
    elif score >= 60:
        bg_color = "#ededed"
    else:
        bg_color = "#fbcccd"
    return bg_color


def format_object_to_string(object, separator="\n- "):
    """Convert object (e.g. list) to string."""
    if not isinstance(object, str):
        return separator + separator.join(object)
    else:
        return object


def markdown_to_html(md_text):
    """Convert Markdown to html."""
    html_txt = (
        markdown.markdown(md_text.replace("\\n", "\n").replace("- ", "\n- "))
        .replace("\n", "")
        .replace('\\"', '"')
    )
    return html_txt


def display_scores_in_columns(section_names: list, scores: list, column_width: list):
    """Display the scores of the sections in side-by-side columns.
    The column_width variable sets the width of the columns."""
    columns = st.columns(column_width)
    for i, column in enumerate(columns):
        with column:
            custom_markdown(
                text=f"<b>{section_names[i]} <br><br> {scores[i]}</b>",
                bg_color=set_background_color(scores[i]),
                text_align="center",
            )


def display_section_results(
    expander_label: str,
    expander_header_fields: list,
    expander_header_links: list,
    score: int,
    section_original_text_header: str,
    section_original_text: list,
    original_text_bullet_points: bool,
    section_assessment,
    section_improved_text,
):
    if score > -1:
        expander_label += f"- 🎯 **{score}**/100"
    with st.expander(expander_label):
        st.write("")

        # 1. Display the header fields (for example, the company and dates of the work experience)
        if expander_header_fields is not None:
            for field in expander_header_fields:
                if not isinstance(field, list):
                    st.markdown(field)
                else:
                    # display fields in side-by-side columns.
                    columns = st.columns(len(field))
                    for i, column in enumerate(columns):
                        with column:
                            st.markdown(field[i])

        # 2. View the links (examle social media blogs and web sites)
        if expander_header_links is not None:
            if not isinstance(expander_header_links, list):
                link = expander_header_links.strip().replace('"', "")
                if not link.startswith("http"):
                    link = "https://" + link
                st.markdown(
                    f"""🌐 <a href="{link}" target="_blank">{link}""",
                    unsafe_allow_html=True,
                )
            else:
                for link in expander_header_links:
                    if not link.startswith("http"):
                        link = "https://" + link
                    st.markdown(
                        f"""🌐 <a href="{link}" target="_blank">{link}""",
                        unsafe_allow_html=True,
                    )

        # 3. View the original text
        if section_original_text_header is not None:
            st.write("")
            st.markdown(section_original_text_header)
        if section_original_text is not None:
            for text in section_original_text:
                if original_text_bullet_points:
                    st.markdown(f"- {text}")
                else:
                    st.markdown(text)

        # 4. Display of section score
        st.divider()
        custom_markdown(
            html_tag="h4",
            text=f"<b>🎯 Score: {score}</b>/<small>100</small>",
        )

        # 5. Display the assessmnet
        bg_color = set_background_color(score)
        assessment = markdown_to_html(format_object_to_string(section_assessment))
        custom_markdown(
            text=f"<b>🔎 Assessment:</b> <br><br> {assessment}",
            html_tag="div",
            bg_color=bg_color,
        )

        # 6. View the improved text
        if section_improved_text is not None:
            improved_text = markdown_to_html(
                format_object_to_string(section_improved_text)
            )
            custom_markdown(
                text=f"<b>🚀 Improvement:</b> <br><br> {improved_text}",
                html_tag="div",
                bg_color="#ededed",
            )
        st.write("")


def display_assessment(score, section_assessment):
    """Display the section score and the assessment."""
    # 1. View section score
    custom_markdown(
        html_tag="h4",
        text=f"<b>🎯 Score: {score}</b>/<small>100</small>",
    )
    # 2. Display the assessmnet
    bg_color = set_background_color(score)
    assessment = markdown_to_html(format_object_to_string(section_assessment))
    custom_markdown(
        text=f"<b>🔎 Assessment:</b> <br><br> {assessment}",
        html_tag="div",
        bg_color=bg_color,
    )
    st.write("")


def display_resume_analysis(SCANNED_RESUME):
    """Display the resume analysis."""
    try:
        ###############################################################
        #        Overview, Top 3 strengths and Top 3 weaknesses
        ###############################################################
        st.divider()
        st.header("🎯 Overview and scores")

        list_task = ["Overview", "Top 3 strengths", "Top 3 weaknesses"]
        list_content = [
            SCANNED_RESUME["resume_cv_overview"],
            SCANNED_RESUME["top_3_strengths"],
            SCANNED_RESUME["top_3_weaknesses"],
        ]
        list_colors = ["#ededed", "#D4F1F4", "#fbcccd"]

        for i in range(3):
            st.write("")
            st.subheader(list_task[i])
            custom_markdown(
                html_tag="div",
                text=markdown_to_html(format_object_to_string(list_content[i])),
                bg_color=list_colors[i],
            )

        ###############################################################
        #                      Display scores
        ###############################################################
        st.write("")
        st.subheader("Scores over 100")
        st.write("")

        dict_scores = get_section_scores(SCANNED_RESUME)

        display_scores_in_columns(
            section_names=[
                "👤 Contact",
                "📋 Summary",
                "📋 Work Experience",
                "💪 Skills",
            ],
            scores=[
                dict_scores.get(key)
                for key in ["ContactInfo", "summary", "work_experience", "skills"]
            ],
            column_width=[2.25, 2.25, 2.75, 2.25],
        )

        display_scores_in_columns(
            section_names=[
                "🎓 Education",
                "🗣 Language",
                "📋 Projects",
                "🏅 Certifications",
            ],
            scores=[
                dict_scores.get(key)
                for key in ["education", "language", "projects", "certfication"]
            ],
            column_width=[2.5, 2.5, 2.5, 2.75],
        )

        ##################################################################################
        #                          Detailed analysis
        ##################################################################################
        st.divider()
        st.header("🔎 Detailed Analysis")

        # 1. Contact Information

        st.write("")
        st.subheader(f"Contact Information - 🎯 **{dict_scores['ContactInfo']}**/100")
        display_section_results(
            expander_label="🛈 Contact Information",
            expander_header_fields=[
                f"**👤 {SCANNED_RESUME['Contact__information']['candidate__name']}**",
                f"{SCANNED_RESUME['Contact__information']['candidate__title']}",
                "",
                [
                    f"**📌 Location:** {SCANNED_RESUME['Contact__information']['candidate__location']}",
                    f"**:telephone_receiver::** {SCANNED_RESUME['Contact__information']['candidate__phone']}",
                ],
                "",
                "**Email and Social media:**",
                f"**:e-mail:** {SCANNED_RESUME['Contact__information']['candidate__email']}",
            ],
            expander_header_links=SCANNED_RESUME["Contact__information"][
                "candidate__social_media"
            ],
            score=dict_scores["ContactInfo"],
            section_original_text_header=None,
            section_original_text=None,
            original_text_bullet_points=False,
            section_assessment=SCANNED_RESUME["Contact__information"][
                "evaluation__ContactInfo"
            ],
            section_improved_text=None,
        )

        # 2. Summary

        st.write("")
        st.write("")
        st.subheader(f"Summary - 🎯 **{dict_scores['summary']}**/100")
        display_section_results(
            expander_label="Summary",
            expander_header_fields=[],
            expander_header_links=None,
            score=dict_scores["summary"],
            section_original_text_header="**📋 Summary:**",
            section_original_text=[SCANNED_RESUME["CV__summary"]],
            original_text_bullet_points=False,
            section_assessment=SCANNED_RESUME["Summary__evaluation"][
                "evaluation__summary"
            ],
            section_improved_text=SCANNED_RESUME["Summary__evaluation"][
                "CV__summary_enhanced"
            ],
        )

        #  3. Work Experience

        st.write("")
        st.write("")
        st.subheader(f"work experience - 🎯 **{dict_scores['work_experience']}**/100")

        if len(SCANNED_RESUME["Work__experience"]) == 0:
            st.info("No work experience results.")
        else:
            for work_experience in SCANNED_RESUME["Work__experience"]:
                display_section_results(
                    expander_label=f"{work_experience['job__title']}",
                    expander_header_fields=[
                        [
                            f"**Company:**\n {work_experience['job__company']}",
                            f"**📅**\n {work_experience['job__start_date']} - {work_experience['job__end_date']}",
                        ]
                    ],
                    expander_header_links=None,
                    score=work_experience["Score__WorkExperience"],
                    section_original_text_header="**📋 Responsibilities:**",
                    section_original_text=list(
                        work_experience["work__duties"].values()
                    ),
                    original_text_bullet_points=True,
                    section_assessment=work_experience["Comments__WorkExperience"],
                    section_improved_text=work_experience[
                        "Improvement__WorkExperience"
                    ],
                )

        # 4. Skills

        st.write("")
        st.write("")
        st.subheader(f"Skills - 🎯 **{dict_scores['skills']}**/100")
        display_section_results(
            expander_label="💪 Skills",
            expander_header_fields=None,
            expander_header_links=None,
            score=dict_scores["skills"],
            section_original_text_header=None,
            section_original_text=[SCANNED_RESUME["candidate__skills"]],
            original_text_bullet_points=True,
            section_assessment=SCANNED_RESUME["Skills__evaluation"][
                "evaluation__skills"
            ],
            section_improved_text=None,
        )

        # 5. Education

        st.write("")
        st.write("")
        st.subheader(f"Education - 🎯 **{dict_scores['education']}**/100")
        with st.expander(f"🎓 Educational background and academic achievements."):
            st.write("")
            list_education = SCANNED_RESUME["CV__Education"]
            if not isinstance(list_education, list):
                st.markdown(f"- {list_education}")
            else:
                for edu in list_education:
                    col1, col2 = st.columns([6, 4])
                    with col1:
                        st.markdown(f"**🎓 Degree:** {edu['edu__degree']}")
                    with col2:
                        st.markdown(
                            f"**📅** {edu['edu__start_date']} - {edu['edu__end_date']}"
                        )
                    st.markdown(f"**🏛️** {edu['edu__college']}")
                    st.divider()

            display_assessment(
                score=dict_scores["education"],
                section_assessment=SCANNED_RESUME["Education__evaluation"][
                    "evaluation__edu"
                ],
            )

        # 6. Language (Optional section)

        st.divider()
        st.subheader(f"Language - 🎯 **{dict_scores['language']}**/100")
        languages = []
        for language in SCANNED_RESUME["CV__Languages"]:
            languages.append(
                f"**🗣 {language['spoken__language']}** : {language['language__fluency']}"
            )
        display_section_results(
            expander_label="🗣 Language",
            expander_header_fields=None,
            expander_header_links=None,
            score=dict_scores["language"],
            section_original_text_header=None,
            section_original_text=languages,
            original_text_bullet_points=False,
            section_assessment=SCANNED_RESUME["Languages__evaluation"][
                "evaluation__language"
            ],
            section_improved_text=None,
        )

        # 7. CERTIFICATIONS (optional section)

        st.write("")
        st.write("")
        st.subheader(f"Certifications - 🎯 **{dict_scores['certfication']}**/100")
        with st.expander("🏅 Certifications"):
            st.write("")
            list_certifs = SCANNED_RESUME["CV__Certifications"]
            if not isinstance(list_certifs, list):
                st.markdown(f"- {list_certifs}")
            else:
                for certif in list_certifs:
                    col1, col2 = st.columns([6, 4])
                    with col1:
                        st.markdown(f"**🏅 Title:** {certif['certif__title']}")
                    with col2:
                        st.markdown(f"**📅** {certif['certif__date']} ")
                    st.markdown(f"**🏛️** {certif['certif__organization']}")

                    if certif["certif__expiry_date"].lower() != "unknown":
                        st.markdown(
                            f"**📅 Expiry date:** {certif['certif__expiry_date']}"
                        )
                    if certif["certif__details"].lower() != "unknown":
                        st.write("")
                        st.markdown(f"{certif['certif__details']}")
                    st.divider()

                display_assessment(
                    score=dict_scores["certfication"],
                    section_assessment=SCANNED_RESUME["Certif__evaluation"][
                        "evaluation__certif"
                    ],
                )

        # 8. Projects (Optional section)

        st.write("")
        st.write("")
        st.subheader(f"Projects - 🎯 **{dict_scores['projects']}**/100")
        if len(SCANNED_RESUME["CV__Projects"]) == 0:
            st.info("No projects found.")
        else:
            for project in SCANNED_RESUME["CV__Projects"]:
                display_section_results(
                    expander_label=f"{project['project__title']}",
                    expander_header_fields=[
                        f"**📅**\n {project['project__start_date']} - {project['project__end_date']}"
                    ],
                    expander_header_links=None,
                    score=project["Score__project"],
                    section_original_text_header="**📋 Project details:**",
                    section_original_text=[project["project__description"]],
                    original_text_bullet_points=True,
                    section_assessment=project["Comments__project"],
                    section_improved_text=project["Improvement__project"],
                )

    except Exception as exception:
        print(exception)
