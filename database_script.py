from sqlalchemy import create_engine, MetaData
import pandas as pd
import os
from datetime import datetime
import shutil

# Create engine (it's in awa)
engine = create_engine('sqlite:///awa/test.db')
# print(engine.table_names())

# Get data from all tables
task = pd.read_sql_table('task', 'sqlite:///awa/test.db')
strategy = pd.read_sql_table('strategy', 'sqlite:///awa/test.db')
project = pd.read_sql_table('project', 'sqlite:///awa/test.db')
alembic_version = pd.read_sql_table('alembic_version', 'sqlite:///awa/test.db')


# Save database copy to Excel file
file_path = os.path.join('pickles', f"database_copy_{datetime.now().strftime('%y%m%d%H%M')}.xlsx")
writer = pd.ExcelWriter(file_path)
task.to_excel(writer, sheet_name='task', index=False)
strategy.to_excel(writer, sheet_name='strategy', index=False)
project.to_excel(writer, sheet_name='project', index=False)
alembic_version.to_excel(writer, sheet_name='alembic_version', index=False)
writer.save()

# Copy Excel file to edit it
shutil.copyfile(file_path, os.path.join('pickles', f"database_copy_input.xlsx"))


# Insert data to db
input_file = os.path.join('pickles', 'database_copy_input.xlsx')
# input_file = os.path.join('pickles', 'database_copy_2005271615.xlsx')
# input_file = os.path.join('pickles', 'database_copy_test_fixing.xlsx')
strategy = pd.read_excel(input_file, sheet_name='strategy')
strategy.to_sql(name='strategy', con=engine, index=False, if_exists='append')
project = pd.read_excel(input_file, sheet_name='project')
project.to_sql(name='project', con=engine, index=False, if_exists='append')
task = pd.read_excel(input_file, sheet_name='task')
task.to_sql(name='task', con=engine, index=False, if_exists='append')
# Check docs for extra options: e.g. if_exists='replace', index_label='id'