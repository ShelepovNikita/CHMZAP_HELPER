
from config import db
import with_excel as we

start_date = '2021-09-30'
end_date = '2023-04-21'

date = db.search_by_period_in_troubles(start_date, end_date)
we.create_excel(date, '/home/shelepovfamily/Dev/CHMZAP_HELPER/')
