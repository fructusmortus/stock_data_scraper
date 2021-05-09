from sqlalchemy.orm import sessionmaker

from db_models import db_connect, create_table, Companies, Table1


class FinvizPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        table_1 = Table1()
        company = session.query(Companies).filter_by(ticker=item['ticker']).first()
        if company:
            table_1.ticker = company.ticker
        else:
            company = Companies()
            company.ticker = item['ticker']
            company.full_name = item['full_name']
            company.sector = item['sector']
            company.industry = item['industry']
            company.country = item['country']
            table_1.ticker = item['ticker']
            session.add(company)
        table_1.table_1 = item['table1']
        session.add(table_1)
        session.commit()
        session.close()
        return item
