from schema import factory
from schema import Job

j1 = Job(job_title="Student", min_salary=5000000, max_salary=9000000)
j2 = Job(job_title="Teacher", min_salary=2500, max_salary=8000)
j3 = Job(job_title="Scientist", min_salary=60000, max_salary=150000)
j4 = Job(job_title="Electrician", min_salary=100, max_salary=500)

session = factory()
session.add_all([j1, j2, j3, j4])
session.commit()
