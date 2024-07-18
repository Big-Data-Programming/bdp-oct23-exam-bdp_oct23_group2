# hushHush Recruiter Project

# AutomateHire

AutomateHire is a collaborative project developed by our team. Built in Python, the project utilizes popular libraries such as sklearn, pandas, numpy, django, and asyncio to automate the candidate selection process for potential roles at Doodle, a renowned software company.

## Project Overview

Doodle sought to automate its recruitment process while ensuring secrecy and avoiding deterministic algorithms to prevent social media discussions and replication of selection patterns. AutomateHire was developed to address this need, providing an interface for candidates to submit code solutions to coding questions provided by Doodle. The system also enables hiring managers to evaluate these solutions and initiate the interview process based on the assessment.

## Features

- **User Clustering and Selection**: Leveraging KMeans and Logistic Regression algorithms for user clustering and selection.
- **Code Evaluation**: Implementing tests for evaluating user-submitted code to ensure quality and correctness.
- **Asynchronous Data Retrieval**: Fetching data from GitHub and Stack Overflow asynchronously to streamline the process.
- **Triggers for User Code Submission**: Utilizing triggers to initiate actions when user code is submitted, enhancing automation.
- **Future Work**: Planning to implement reinforcement learning for further enhancements to the candidate selection process.

## Selection Criteria

AutomateHire employs a comprehensive set of selection criteria, including coding activity, project contributions, skills proficiency, collaboration and teamwork, problem-solving skills, community involvement, and more. These criteria ensure a holistic evaluation of candidates' capabilities and suitability for roles at Doodle.

## User Stories

### Recruiter:

- **Configure Candidate Selection Criteria**: Enabling recruiters to define selection criteria and specify the desired number of candidates for selection.

### Hiring Manager:

- **Evaluate Code Challenges and Schedule Interviews**: Empowering hiring managers to assess code challenges submitted by candidates and schedule interviews with top candidates based on the assessment.

### Candidate:

- **Engage with Code Challenges and Track Application Process**: Providing candidates with the ability to submit code challenges, receive feedback, and track their application process through the platform.

## Installation

To run AutomateHire locally, follow these steps:

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Configure the system according to your preferences.
4. Run the application using `python manage.py runserver`.

## Contributions

AutomateHire was developed collaboratively by our team as part of our class project. Contributions from team members were instrumental in building and enhancing the functionality of the system.

---

AutomateHire represents the collective effort of our team to develop an innovative solution for automating the candidate selection process, contributing to the advancement of talent acquisition practices in the software industry.
