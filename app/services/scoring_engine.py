# FILE: app/services/scoring_engine.py

class ScoringEngine:
    def __init__(self):
        """
        Weighted scoring:
        - Semantic Similarity: 60%
        - Skill Match Score: 40%
        (ATS-style scoring system)
        """
        self.semantic_weight = 0.60
        self.skill_weight = 0.40

    # ----------------------------------------------------------
    # Skill overlap score (JD skills vs Resume skills)
    # ----------------------------------------------------------
    def skill_match_score(self, resume_skills, jd_skills):
        """
        resume_skills = list of detected resume skills
        jd_skills = list of required skills from JD
        """

        if not jd_skills:
            return 0.0
        
        if not resume_skills:
            return 0.0

        # lower-case for matching
        resume_set = set([s.lower() for s in resume_skills])
        jd_set = set([s.lower() for s in jd_skills])

        # intersection = matched skills
        matched = resume_set.intersection(jd_set)

        skill_score = len(matched) / len(jd_set)
        skill_score = round(skill_score, 4)

        return skill_score

    # ----------------------------------------------------------
    # Final combined scoring (semantic + skills)
    # ----------------------------------------------------------
    def calculate_final_score(self, semantic_value, resume_skills, jd_skills):
        """
        Returns final weighted ATS score (0–100).
        """
        # Clamp similarity between 0–1
        semantic_value = max(0.0, min(1.0, semantic_value))

        # Skill score (0–1)
        skill_score = self.skill_match_score(resume_skills, jd_skills)

        # Weighted scoring formula
        final_score = (
            (semantic_value * self.semantic_weight) +
            (skill_score * self.skill_weight)
        )

        final_percentage = round(final_score * 100, 2)
        return final_percentage
