from pydantic import BaseModel, EmailStr, constr, conint, Field

class User(BaseModel):
    # Number of steps to produce regex:
    # 1. go to docs.pydantic.dev/latest/concepts/fields/#string-constraints. Look for pattern example
    # 2. Test regex here: https://regex101.com/
    # 3. Google 'regex  matches a specific letter' & 'regex matches specific number of digits'
    student_id: str = Field(pattern=r'^[S]\d{7}$') # Student ID must start with 'S', followed by exactly 7 digits
    user_id: int
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    age: conint(gt=18)