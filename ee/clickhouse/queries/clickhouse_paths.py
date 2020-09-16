from typing import Any, Dict, List, Optional

from ee.clickhouse.client import sync_execute
from ee.clickhouse.queries.util import parse_timestamps
from posthog.constants import AUTOCAPTURE_EVENT, CUSTOM_EVENT, SCREEN_EVENT
from posthog.models.filter import Filter
from posthog.models.team import Team
from posthog.queries.base import BaseQuery
from posthog.utils import relative_date_parse, request_to_date_query


class ClickhousePaths(BaseQuery):
    # def _determine_path_type(self, requested_type=None):
    #     # Default
    #     event: Optional[str] = "$pageview"
    #     event_filter = {"event": event}
    #     path_type = "properties->> '$current_url'"
    #     start_comparator = "{} ~".format(path_type)
    #
    #     # determine requested type
    #     if requested_type:
    #         if requested_type == SCREEN_EVENT:
    #             event = SCREEN_EVENT
    #             event_filter = {"event": event}
    #             path_type = "properties->> '$screen_name'"
    #             start_comparator = "{} ~".format(path_type)
    #         elif requested_type == AUTOCAPTURE_EVENT:
    #             event = AUTOCAPTURE_EVENT
    #             event_filter = {"event": event}
    #             path_type = "tag_name_source"
    #             start_comparator = "group_id ="
    #         elif requested_type == CUSTOM_EVENT:
    #             event = None
    #             event_filter = {}
    #             path_type = "event"
    #             start_comparator = "event ="
    #     return event, path_type, event_filter, start_comparator
    #
    # def _apply_start_point(self, start_comparator: str, query_string: str, start_point: str) -> str:
    #     marked = "\
    #         SELECT *, CASE WHEN {} '{}' THEN timestamp ELSE NULL END as mark from ({}) as sessionified\
    #     ".format(
    #         start_comparator, start_point, query_string
    #     )
    #
    #     marked_plus = "\
    #         SELECT *, MIN(mark) OVER (\
    #                 PARTITION BY distinct_id\
    #                 , session ORDER BY timestamp\
    #                 ) AS max from ({}) as marked order by session\
    #     ".format(
    #         marked
    #     )
    #
    #     sessionified = "\
    #         SELECT * FROM ({}) as something where timestamp >= max \
    #     ".format(
    #         marked_plus
    #     )
    #     return sessionified
    #
    # def _add_elements(self, query_string: str) -> str:
    #     element = 'SELECT \'<\'|| e."tag_name" || \'> \'  || e."text" as tag_name_source, e."text" as text_source FROM "posthog_element" e JOIN \
    #                 ( SELECT group_id, MIN("posthog_element"."order") as minOrder FROM "posthog_element" GROUP BY group_id) e2 ON e.order = e2.minOrder AND e.group_id = e2.group_id where e.group_id = v2.group_id'
    #     element_group = 'SELECT g."id" as group_id FROM "posthog_elementgroup" g where v1."elements_hash" = g."hash"'
    #     sessions_sql = "SELECT * FROM ({}) as v1 JOIN LATERAL ({}) as v2 on true JOIN LATERAL ({}) as v3 on true".format(
    #         query_string, element_group, element
    #     )
    #     return sessions_sql

    def calculate_paths(self, filter: Filter, team: Team):
        # date_query = request_to_date_query({"date_from": filter._date_from, "date_to": filter._date_to}, exact=False)
        # resp = []
        # event, path_type, event_filter, start_comparator = self._determine_path_type(
        #     filter.path_type if filter else None
        # )
        #
        # sessions = (
        #     Event.objects.add_person_id(team.pk)
        #     .filter(team=team, **(event_filter), **date_query)
        #     .filter(~Q(event__in=["$autocapture", "$pageview", "$identify", "$pageleave"]) if event is None else Q())
        #     .filter(filter.properties_to_Q(team_id=team.pk) if filter and filter.properties else Q())
        #     .annotate(
        #         previous_timestamp=Window(
        #             expression=Lag("timestamp", default=None),
        #             partition_by=F("distinct_id"),
        #             order_by=F("timestamp").asc(),
        #         )
        #     )
        # )

        # sessions_sql, sessions_sql_params = sessions.query.sql_with_params()

        sessions_query = """
            SELECT distinct_id,
                   event_id,
                   timestamp,
                   path_type,
                   IF(
                      neighbor(distinct_id, -1) != distinct_id
                        OR dateDiff('minute', toDateTime(timestamp), toDateTime(neighbor(timestamp, -1))) > 30, 
                      1,
                      0
                   ) AS new_session
            FROM (
                    SELECT timestamp,
                           distinct_id,
                           id AS event_id,
                           JSONExtractString(properties, %(property)s) AS path_type
                    FROM events
                    WHERE team_id = %(team_id)s 
                      AND event = %(event)s
                    GROUP BY distinct_id, timestamp, event_id, properties
                    ORDER BY distinct_id, timestamp
            )
        """

        # if event == "$autocapture":
        #     sessions_sql = self._add_elements(query_string=sessions_sql)

        # events_notated = "\
        # SELECT *, CASE WHEN EXTRACT('EPOCH' FROM (timestamp - previous_timestamp)) >= (60 * 30) OR previous_timestamp IS NULL THEN 1 ELSE 0 END AS new_session\
        # FROM ({}) AS inner_sessions\
        # ".format(
        #     sessions_sql
        # )

        # sessionified = "\
        # SELECT events_notated.*, SUM(new_session) OVER (\
        #     ORDER BY distinct_id\
        #             ,timestamp\
        #     ) AS session\
        # FROM ({}) as events_notated\
        # ".format(
        #     events_notated
        # )
        #
        # if filter and filter.start_point:
        #     sessionified = self._apply_start_point(
        #         start_comparator=start_comparator, query_string=sessionified, start_point=filter.start_point,
        #     )
        #
        # final = "\
        # SELECT {} as path_type, id, sessionified.session\
        #     ,ROW_NUMBER() OVER (\
        #             PARTITION BY distinct_id\
        #             ,session ORDER BY timestamp\
        #             ) AS event_number\
        # FROM ({}) as sessionified\
        # ".format(
        #     path_type, sessionified
        # )
        #
        # counts = "\
        # SELECT event_number || '_' || path_type as target_event, id as target_id, LAG(event_number || '_' || path_type, 1) OVER (\
        #     PARTITION BY session\
        #     ) AS source_event , LAG(id, 1) OVER (\
        #     PARTITION BY session\
        #     ) AS source_id from \
        # ({}) as final\
        # where event_number <= 4\
        # ".format(
        #     final
        # )

        # cursor = connection.cursor()
        # cursor.execute(
        #     "\
        # SELECT source_event, target_event, MAX(target_id), MAX(source_id), count(*) from ({}) as counts\
        # where source_event is not null and target_event is not null\
        # group by source_event, target_event order by count desc limit 20\
        # ".format(
        #         counts
        #     ),
        #     sessions_sql_params,
        # )
        # rows = cursor.fetchall()

        aggregate_query = """
            SELECT concat(toString(group_index), '_', path_type)                                          AS target_event,
                   event_id                                                                               AS target_event_id,
                   if(group_index > 1, neighbor(concat(toString(group_index), '_', path_type), -1), null) AS source_event,
                   if(group_index > 1, neighbor(event_id, -1), null)                                      AS source_event_id
            FROM (
                  SELECT distinct_id,
                         event_id,
                         timestamp,
                         path_type,
                         arraySum(arraySlice(gids, 1, idx))                 AS gid,
                         indexOf(arrayReverse(arraySlice(gids, 1, idx)), 1) AS group_index
                  FROM (
                        SELECT groupArray(timestamp)   AS timestamps,
                               groupArray(path_type)   AS path_types,
                               groupArray(event_id)    AS event_ids,
                               groupArray(distinct_id) AS distinct_ids,
                               groupArray(new_session) AS gids
                         FROM ({sessions_query})
                       )
                  ARRAY JOIN
                       distinct_ids AS distinct_id,
                       event_ids AS event_id,
                       timestamps AS timestamp,
                       path_types AS path_type,
                       arrayEnumerate(gids) AS idx
            )
            WHERE group_index <= %(query_depth)s
        """

        count_query = """
            SELECT 
                source_event         AS source_event, 
                any(source_event_id) AS source_event_id, 
                target_event         AS target_event, 
                any(target_event_id) AS target_event_id, 
                COUNT(*)             AS event_count
            FROM ({aggregate_query}) 
            WHERE source_event IS NOT NULL 
              AND target_event IS NOT NULL
            GROUP BY source_event, target_event
            ORDER BY event_count DESC, source_event, target_event
        """

        final_query = count_query.format(aggregate_query=aggregate_query.format(sessions_query=sessions_query))

        rows = sync_execute(
            final_query, {"team_id": team.pk, "property": "$current_url", "event": "$pageview", "query_depth": 4}
        )

        resp: List[Dict[str, str]] = []
        for row in rows:
            resp.append(
                {"source": row[0], "target": row[2], "target_id": row[3], "source_id": row[1], "value": row[4],}
            )

        resp = sorted(resp, key=lambda x: x["value"], reverse=True)
        return resp

    def run(self, filter: Filter, team: Team, *args, **kwargs) -> List[Dict[str, Any]]:
        return self.calculate_paths(filter=filter, team=team)
