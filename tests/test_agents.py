import pytest
from Utils.Agents import Agent, Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam

def test_agent_initialization():
    """Test that agents can be initialized with a medical report."""
    report = "Patient has chest pain."
    cardiologist = Cardiologist(report)
    assert cardiologist.role == "Cardiologist"
    assert cardiologist.medical_report == report

def test_multidisciplinary_team_initialization():
    """Test that the team agent is initialized correctly."""
    team = MultidisciplinaryTeam("Cardio Report", "Psych Report", "Pulmo Report")
    assert team.role == "MultidisciplinaryTeam"
    assert team.extra_info['cardiologist_report'] == "Cardio Report"

def test_prompt_template_creation():
    """Test that prompt templates are created."""
    report = "Test Report"
    agent = Cardiologist(report)
    assert agent.prompt_template is not None
