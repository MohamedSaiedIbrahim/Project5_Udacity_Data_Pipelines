from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 insert_sql="",
                 mode='append',
                 primary_key="",
                 *args, **kwargs):
        
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.insert_sql = insert_sql
        self.mode = mode
        self.primary_key = primary_key

    def execute(self, context):
        
        self.log.info("Getting credentials")
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.mode == 'truncate':
            self.log.info(f'Deleting data from {self.table} table...')
            redshift_hook.run(f'DELETE FROM {self.table};')
        
        table_insert_sql = f"""
            insert into {self.table}
            {self.insert_sql}
        """

        self.log.info("Loading data into dimension table in Redshift")
        redshift_hook.run(table_insert_sql)
