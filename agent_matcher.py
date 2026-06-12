import streamlit as st
import os
import re
from pypdf import PdfReader

# ==========================================
# 1. GLOBAL STREAMLIT UI CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Offline Skill Matcher Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Offline Skill-Matching AI Agent")
st.caption("Enterprise-Grade Local Resume Ranking & Skill Validation System (100% Offline & Private)")
st.write("---")


# ==========================================
# 2. CORE PATTERN MATCHING BACKEND LOGIC
# ==========================================
def extract_text_from_uploaded_pdf(uploaded_file):
    """
    Reads an uploaded stream buffer PDF asset and extracts plaintext layers cleanly.
    """
    text_content = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content += extracted + "\n"
    except Exception as e:
        st.error(f"Error reading file {uploaded_file.name}: {str(e)}")
    return text_content


def parse_skills_from_text(raw_jd_text):
    """
    Extracts individual potential skill tokens from the raw Job Description text.
    Filters out common english grammar stop words automatically.
    """
    words = re.findall(r'\b[a-zA-Z0-9+#\.]+\b', raw_jd_text)
    
    stop_words = {
        'required', 'skills', 'developer', 'and', 'the', 'for', 'with', 
        'job', 'in', 'to', 'of', 'looking', 'experience', 'knowledge', 'years'
    }
    extracted_skills = list(set([w for w in words if w.lower() not in stop_words and len(w) > 1]))
    return extracted_skills


# ==========================================
# 3. INTERACTIVE DASHBOARD GRAPHICAL LAYOUT
# ==========================================
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📋 Job Description Source Context")
    st.write("Upload a target requirements `.txt` file or paste your criteria directly below:")
    
    jd_file_upload = st.file_uploader("Optional: Load JD from (.txt) File", type=["txt"])
    
    default_jd_placeholder = "Looking for an Android Developer proficient in Kotlin, Android Studio, MVVM, Java, Git, and Jetpack Compose."
    
    if jd_file_upload is not None:
        try:
            jd_text_value = jd_file_upload.read().decode("utf-8", errors="ignore")
        except Exception as e:
            st.error(f"Error reading JD file: {str(e)}")
            jd_text_value = default_jd_placeholder
    else:
        jd_text_value = default_jd_placeholder

    job_description_input = st.text_area(
        label="Target Core Skill Criteria Profile:",
        value=jd_text_value,
        height=200
    )

with col2:
    st.header("📂 Candidate Resume Hub")
    st.write("Select and upload your real multi-page candidate PDF resumes directly into memory:")
    
    uploaded_resumes = st.file_uploader(
        label="Drop Candidate Resume PDFs Here:",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_resumes:
        st.success(f"Staged **{len(uploaded_resumes)} resume files** securely inside workspace queue.")


# ==========================================
# 4. RUNTIME RUN PROCESSING ENGINE
# ==========================================
st.write("---")
execute_agent = st.button("🚀 Execute Offline Skill Matching Agent", type="primary")

if execute_agent:
    if not job_description_input.strip():
        st.warning("Execution Halted: Please ensure the Job Description target field is not empty.")
    elif not uploaded_resumes:
        st.warning("Execution Halted: Please upload at least one candidate PDF resume file to verify.")
    else:
        with st.spinner("Agent running text extraction and regex validation over binary data layers..."):
            
            target_skills = parse_skills_from_text(job_description_input)
            
            if not target_skills:
                st.error("Error: Could not extract any valid core skills from the provided Job Description text.")
            else:
                st.info(f"🎯 Target Checklist Parsed from JD: `{', '.join(target_skills)}`")
                
                computed_rankings = []
                report_lines = []
                
                # Setup base title text arrays for local output text backup file
                report_lines.append("====================================================")
                report_lines.append("     OFFLINE AGENT SKILL-MATCHING MATRIX REPORT     ")
                report_lines.append("====================================================\n")
                
                # Step B: Loop through raw uploaded stream memory objects
                for resume_file in uploaded_resumes:
                    raw_resume_text = extract_text_from_uploaded_pdf(resume_file)
                    
                    matched_skills = []
                    not_matched_skills = []
                    
                    # Pattern check loops
                    for skill in target_skills:
                        pattern = r'\b' + re.escape(skill) + r'\b'
                        if re.search(pattern, raw_resume_text, re.IGNORECASE):
                            matched_skills.append(skill)
                        else:
                            not_matched_skills.append(skill)
                            
                    # Calculate percentage metrics
                    total_count = len(target_skills)
                    match_score = round((len(matched_skills) / total_count) * 100, 2) if total_count > 0 else 0
                    
                    # Store data row for dynamic sorting UI leaderboard
                    computed_rankings.append({
                        "filename": resume_file.name,
                        "score": match_score,
                        "matched": matched_skills,
                        "unmatched": not_matched_skills,
                        "raw_text": raw_resume_text
                    })
                    
                    # Append rows directly to background text logging compiler
                    report_lines.append(f"📄 CANDIDATE FILE: {resume_file.name}")
                    report_lines.append(f"📊 MATCH COVERAGE SCORE: {match_score}%")
                    report_lines.append(f"✅ MATCHED SKILLS ({len(matched_skills)}): {', '.join(matched_skills) if matched_skills else 'None'}")
                    report_lines.append(f"❌ NOT MATCHED SKILLS ({len(not_matched_skills)}): {', '.join(not_matched_skills) if not_matched_skills else 'None'}")
                    report_lines.append("-" * 52 + "\n")
                
                # Step C: Write back compiled lines natively to target local storage file path
                output_log_filename = "result.txt"
                try:
                    # File direct disk sync pipeline
                    with open(output_log_filename, "w", encoding="utf-8") as f_out:
                        f_out.write("\n".join(report_lines))
                    st.success(f"💾 Background Synchronization Complete! Data successfully written to `{output_log_filename}`")
                except Exception as ex:
                    st.error(f"Could not update local storage file data log logs: {str(ex)}")
                
                # ==========================================
                # 5. RENDER DYNAMIC UI VISUAL LEADERBOARD
                # ==========================================
                st.write("---")
                st.subheader("📊 Candidate Compatibility Leaderboard")
                
                sorted_leaderboard = sorted(computed_rankings, key=lambda x: x["score"], reverse=True)
                
                for rank, candidate in enumerate(sorted_leaderboard, start=1):
                    with st.container():
                        card_col1, card_col2 = st.columns([1, 5])
                        
                        with card_col1:
                            if rank == 1:
                                st.markdown(f"### 🏆 Rank {rank}")
                            else:
                                st.markdown(f"### Rank {rank}")
                                
                        with card_col2:
                            st.markdown(f"**Resume Profile:** `{candidate['filename']}`")
                            
                            normalized_progress_bar = float(candidate["score"] / 100.0)
                            st.progress(max(0.0, min(1.0, normalized_progress_bar)))
                            st.markdown(f"🎯 Evaluated Match Coverage Accuracy: **{candidate['score']}%**")
                            
                            sub_col1, sub_col2 = st.columns(2)
                            with sub_col1:
                                st.markdown("##### ✅ Matched Skillsets Detected:")
                                if candidate["matched"]:
                                    st.info(", ".join(candidate["matched"]))
                                else:
                                    st.caption("None tracked.")
                            with sub_col2:
                                f"##### ❌ Missing Requirements:"
                                if candidate["unmatched"]:
                                    st.error(", ".join(candidate["unmatched"]))
                                else:
                                    st.success("All targets matched perfectly!")
                                    
                            with st.expander("Review Parsed Extracted Plaintext Document Stream Logs"):
                                st.text_area(
                                    label="Extracted Context:", 
                                    value=candidate["raw_text"], 
                                    height=120, 
                                    key=f"text_area_{rank}_{candidate['filename']}",
                                    disabled=True
                                )
                        st.markdown("---")