from sqlalchemy import create_engine, MetaData
import pandas as pd
from os import path

# Create engine (it's in awa)
engine = create_engine('sqlite:///awa/test.db')
# print(engine.table_names())


# Get data from all tables
task = pd.read_sql_table('task', 'sqlite:///awa/test.db')
strategy = pd.read_sql_table('strategy', 'sqlite:///awa/test.db')
project = pd.read_sql_table('project', 'sqlite:///awa/test.db')
alembic_version = pd.read_sql_table('alembic_version', 'sqlite:///awa/test.db')

writer = pd.ExcelWriter(path.join('pickles', 'dbcopy.xlsx'))
task.to_excel(writer, sheet_name='task', index=False)
strategy.to_excel(writer, sheet_name='strategy', index=False)
project.to_excel(writer, sheet_name='project', index=False)
alembic_version.to_excel(writer, sheet_name='alembic_version', index=False)
writer.save()

# Insert data to db
# task = pd.read_excel(path.join('pickles', 'dbcopy_insert.xlsx'), sheet_name='task')
# task.to_sql(name='task', con=engine, index=False, if_exists='append')
# Check docs for extra options: e.g. if_exists='replace', index_label='id'