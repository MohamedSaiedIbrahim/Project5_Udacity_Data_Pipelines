from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    
    ui_color = '#89DA59'
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 *args, **kwargs):
        
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id,
        self.tables = tables
    
    def execute(self, context):
        
        self.log.info("Getting credentials")
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Running test")
        for table in self.tables:
            records = redshift_hook.get_records('select count(*) from {table}')
            if records[0][0] < 1:
                raise ValueError(f"""
                    Data quality check failed. \
                    {records[0][0]} equals Zero
                """)
            else:
                self.log.info("Data quality check passed")
                