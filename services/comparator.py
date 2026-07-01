def compare_assessments(results):
    if len(results) < 2:
        return {
            "reply": "Please specify two assessments to compare.",
            "recommendations": [],
            "end_of_conversation": False
        }

    a = results[0]
    b = results[1]

    comparison = f"""
Comparison

Name:
- {a['name']}
- {b['name']}

Categories:
- {", ".join(a.get("keys", []))}
- {", ".join(b.get("keys", []))}

Duration:
- {a.get("duration", "N/A")}
- {b.get("duration", "N/A")}

Job Levels:
- {", ".join(a.get("job_levels", []))}
- {", ".join(b.get("job_levels", []))}

Adaptive:
- {a.get("adaptive", "N/A")}
- {b.get("adaptive", "N/A")}

Remote:
- {a.get("remote", "N/A")}
- {b.get("remote", "N/A")}
"""

    return {
        "reply": comparison,
        "recommendations": [],
        "end_of_conversation": True
    }