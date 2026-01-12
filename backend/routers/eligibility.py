from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from resume_parse import extract_text_from_pdf

router = APIRouter(
    prefix="/eligibility",
    tags=["Eligibility Check"]
)

@router.post("/check")
async def check_eligibility(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    # 1️⃣ Validate PDF
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # 2️⃣ Extract resume text
    resume_text = extract_text_from_pdf(resume.file)

    if resume_text is None or resume_text.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Could not read resume text"
        )

    # 3️⃣ Convert to lowercase
    jd_text = job_description.lower()
    resume_text = resume_text.lower()

    # 4️⃣ Split words
    jd_words = jd_text.split()
    resume_words = resume_text.split()

    if len(jd_words) == 0:
        raise HTTPException(
            status_code=400,
            detail="Job description is empty"
        )

    # 5️⃣ Count matching words
    matched_count = 0

    for word in jd_words:
        if word in resume_words:
            matched_count += 1

    # 6️⃣ Calculate percentage
    match_percentage = round(
        (matched_count / len(jd_words)) * 100,
        2
    )

    # 7️⃣ Verdict
    if match_percentage >= 70:
        verdict = "High Match"
    elif match_percentage >= 40:
        verdict = "Medium Match"
    else:
        verdict = "Low Match"

    # 8️⃣ Return response
    return {
        "match_percentage": match_percentage,
        "matched_words": matched_count,
        "total_jd_words": len(jd_words),
        "verdict": verdict
    }
