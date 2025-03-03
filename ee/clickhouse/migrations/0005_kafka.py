from infi.clickhouse_orm import migrations  # type: ignore

from ee.clickhouse.sql.elements import ELEMENTS_TABLE_MV_SQL, KAFKA_ELEMENTS_TABLE_SQL
from ee.clickhouse.sql.events import EVENTS_TABLE_MV_SQL, KAFKA_EVENTS_TABLE_SQL
from ee.clickhouse.sql.person import (
    KAFKA_OMNI_PERSONS_TABLE_SQL,
    KAFKA_PERSONS_DISTINCT_ID_TABLE_SQL,
    KAFKA_PERSONS_TABLE_SQL,
    OMNI_PERSONS_TABLE_MV_SQL,
    PERSONS_DISTINCT_ID_TABLE_MV_SQL,
    PERSONS_TABLE_MV_SQL,
)

operations = [
    migrations.RunSQL(KAFKA_EVENTS_TABLE_SQL),
    migrations.RunSQL(KAFKA_ELEMENTS_TABLE_SQL),
    migrations.RunSQL(KAFKA_PERSONS_TABLE_SQL),
    migrations.RunSQL(KAFKA_OMNI_PERSONS_TABLE_SQL),
    migrations.RunSQL(KAFKA_PERSONS_DISTINCT_ID_TABLE_SQL),
    migrations.RunSQL(EVENTS_TABLE_MV_SQL),
    migrations.RunSQL(ELEMENTS_TABLE_MV_SQL),
    migrations.RunSQL(PERSONS_TABLE_MV_SQL),
    migrations.RunSQL(OMNI_PERSONS_TABLE_MV_SQL),
    migrations.RunSQL(PERSONS_DISTINCT_ID_TABLE_MV_SQL),
]
