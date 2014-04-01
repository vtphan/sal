# Todos:
# 3-valued logic enforced.  Do not raise exceptions on invalidated fields

from tex import *
import datetime
import time

# String
name = Field( String(5,10), Ne('Cat Smith') )
name.value = 'Cat Smith'

# Int
age = Field( Int(), Gt(38) )
age.value = 20

# Float
salary = Field( Float(), Gt(20000), value=50000 )

# Date
today = datetime.date.today()
dob = Field( Date(), Le(today) )
dob.value = datetime.date.today()

# Datetime
now = datetime.datetime.now()
time.sleep(0.1)
post_time = Field(Datetime(), Lt(now), value=datetime.datetime.now())

# Time
t = Field( Time(), value='1:59 pm')

#-------
print name.eval(), age.eval(), salary.eval(), dob.eval(), post_time.eval(), t.eval()

#-- Query
query = (age < 10) & (name == 'Joe Smith') | ~(salary < 10000)
print query.eval()