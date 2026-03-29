import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")

projectdb = orm.use("project", module="works")
memberdb = orm.use("member", module="works")
projectconfigdb = orm.use("project/config", module="works")
issuedb = orm.use("issueboard/issue", module="works")
issueworkerdb = orm.use("issueboard/issue/worker", module="works")
meetingdb = orm.use("meeting", module="works")
plandb = orm.use("plan", module="works")
readdb = orm.use("issueboard/issue/read", module="works")
mentiondb = orm.use("issueboard/mention", module="works")

class Model:
    """대시보드 전용 통합 조회 Struct"""

    @staticmethod
    def _excluded_project_ids():
        """닫힌 프로젝트 + untrack 프로젝트 ID 목록"""
        user_id = config.session_user_id()
        closed = projectdb.rows(status='close', fields="id")
        closed_ids = [x['id'] for x in closed]
        untracks = projectconfigdb.rows(user_id=user_id, key="untrack", value="true")
        untrack_ids = [x['project_id'] for x in untracks]
        return list(set(closed_ids + untrack_ids))

    @staticmethod
    def my_projects():
        """현재 로그인 사용자가 멤버인 프로젝트 목록 (닫힌/untrack 제외)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        memberships = memberdb.rows(user=user_id, fields="project_id,role")
        project_ids = [m['project_id'] for m in memberships if m['project_id'] not in excluded]
        role_map = {m['project_id']: m['role'] for m in memberships}

        if not project_ids:
            return []

        projects = projectdb.rows(
            id=project_ids,
            status=['draft', 'open'],
            fields="id,namespace,title,short,icon,status,updated,start,end",
            orderby="updated",
            order="DESC"
        )

        for p in projects:
            p['role'] = role_map.get(p['id'], 'guest')

        return projects

    @staticmethod
    def my_issues_summary():
        """나에게 배정된 이슈 요약 (상태별 카운트 + 최근 업데이트 목록)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        fields = 'id,project_id,status,title,user_id,worker,updated,planend'

        def query_assigned(db, qs):
            base = db.worker_id.in_([user_id]) & db.status.in_(['open', 'work', 'finish']) & db.role.in_(['manager'])
            if excluded:
                base = base & db.project_id.not_in(excluded)
            qs = qs.where(base)
            return qs

        assigned = issueworkerdb.rows(
            query=query_assigned,
            fields=fields,
            order="DESC",
            orderby="updated",
            dump=20,
            page=1,
            groupby="id"
        )

        counts = {'open': 0, 'work': 0, 'finish': 0}
        for issue in assigned:
            s = issue.get('status', '')
            if s in counts:
                counts[s] += 1

        # 프로젝트 정보 매핑
        project_cache = {}
        for item in assigned:
            pid = item['project_id']
            if pid not in project_cache:
                p = projectdb.get(id=pid, fields="id,namespace,title,short,icon")
                project_cache[pid] = p if p else {}
            item['project'] = project_cache[pid]

        return {
            'counts': counts,
            'total': sum(counts.values()),
            'recent': assigned[:10]
        }

    @staticmethod
    def my_created_issues():
        """내가 생성한 이슈 중 미완료 건 (open, work)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        fields = 'id,project_id,status,title,user_id,worker,updated,planend'

        def query_created(db, qs):
            base = db.user_id.in_([user_id]) & db.status.in_(['open', 'work'])
            if excluded:
                base = base & db.project_id.not_in(excluded)
            qs = qs.where(base)
            return qs

        rows = issueworkerdb.rows(
            query=query_created,
            fields=fields,
            order="DESC",
            orderby="updated",
            dump=10,
            page=1,
            groupby="id"
        )

        # 프로젝트 정보 매핑
        project_cache = {}
        for item in rows:
            pid = item['project_id']
            if pid not in project_cache:
                p = projectdb.get(id=pid, fields="id,namespace,title,short,icon")
                project_cache[pid] = p if p else {}
            item['project'] = project_cache[pid]

        return rows

    @staticmethod
    def recent_meetings(limit=10):
        """내가 참여한 프로젝트의 최근 회의록"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        memberships = memberdb.rows(user=user_id, fields="project_id")
        my_project_ids = [m['project_id'] for m in memberships if m['project_id'] not in excluded]

        if not my_project_ids:
            return []

        rows = meetingdb.rows(
            project_id=my_project_ids,
            status=['edit', 'read'],
            fields="id,project_id,user_id,title,meetdate,created,updated",
            orderby="meetdate",
            order="DESC",
            dump=limit,
            page=1
        )

        # 프로젝트 정보 매핑
        project_cache = {}
        for item in rows:
            pid = item['project_id']
            if pid not in project_cache:
                p = projectdb.get(id=pid, fields="id,namespace,title,short,icon")
                project_cache[pid] = p if p else {}
            item['project'] = project_cache[pid]

        return rows

    @staticmethod
    def my_plans():
        """내가 담당하는 계획 항목 중 진행중인 것 (ready, active)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        rows = plandb.rows(
            user=user_id,
            status=['ready', 'active'],
            fields="id,project_id,title,status,start,end,parent,order,mm,period,updated",
            orderby="updated",
            order="DESC"
        )

        # 닫힌/untrack 프로젝트 제외
        rows = [r for r in rows if r['project_id'] not in excluded]

        # 프로젝트 정보 매핑
        project_cache = {}
        for item in rows:
            pid = item['project_id']
            if pid not in project_cache:
                p = projectdb.get(id=pid, fields="id,namespace,title,short,icon")
                project_cache[pid] = p if p else {}
            item['project'] = project_cache[pid]

        return rows

    @staticmethod
    def unread_issues(limit=10, page=1):
        """안읽은 이슈 목록 조회 (읽음 상태 추적 + 멘션 기반)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        # 1. is_read=False인 레코드
        unread_records = readdb.rows(user_id=user_id, is_read=False, fields="issue_id")
        unread_issue_ids = [r['issue_id'] for r in unread_records]

        # 2. 멘션 기반 안읽음 이슈
        mention_records = mentiondb.rows(mentioned_user_id=user_id, is_read=False, fields="issue_id")
        mention_issue_ids = [m['issue_id'] for m in mention_records]

        # 합집합
        all_unread_ids = list(set(unread_issue_ids + mention_issue_ids))

        if not all_unread_ids:
            return {'items': [], 'total': 0}

        # 프로젝트 필터 적용
        def query_fn(db, qs):
            qs = qs.where(db.id.in_(all_unread_ids))
            if excluded:
                qs = qs.where(db.project_id.not_in(excluded))
            return qs

        issues = issuedb.rows(
            query=query_fn,
            order="DESC",
            orderby="updated",
            page=page,
            dump=limit,
            fields="id,project_id,title,status,level,user_id,worker,updated,planend"
        )

        total = issuedb.count(query=query_fn)

        # 프로젝트 정보 매핑
        project_cache = {}
        for item in issues:
            pid = item['project_id']
            if pid not in project_cache:
                p = projectdb.get(id=pid, fields="id,namespace,title,short,icon")
                project_cache[pid] = p if p else {}
            item['project'] = project_cache[pid]

        # 읽음 상태 및 멘션 여부 매핑
        mention_id_set = set(mention_issue_ids)
        read_records = readdb.rows(user_id=user_id, issue_id=[i['id'] for i in issues])
        read_map = {r['issue_id']: r for r in read_records}
        for item in issues:
            record = read_map.get(item['id'])
            item['is_read'] = False  # 기본적으로 안읽음 (여기 목록은 안읽은 것만)
            item['is_mentioned'] = item['id'] in mention_id_set

        return {'items': issues, 'total': total}

    @staticmethod
    def all_related_issues(limit=20, page=1):
        """관련된 전체 이슈 (읽음/안읽음 모두 포함, 읽음 상태 표시)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        # 읽음 추적 테이블에 있는 모든 이슈 ID
        read_records = readdb.rows(user_id=user_id, fields="issue_id,is_read")
        read_issue_ids = [r['issue_id'] for r in read_records]
        read_map = {r['issue_id']: r['is_read'] for r in read_records}

        # 멘션 기반 이슈
        mention_records = mentiondb.rows(mentioned_user_id=user_id, fields="issue_id,is_read")
        mention_issue_ids = [m['issue_id'] for m in mention_records]
        mention_read_map = {m['issue_id']: m['is_read'] for m in mention_records}
        mention_id_set = set(mention_issue_ids)

        # 합집합
        all_ids = list(set(read_issue_ids + mention_issue_ids))

        if not all_ids:
            return {'items': [], 'total': 0}

        def query_fn(db, qs):
            qs = qs.where(db.id.in_(all_ids))
            if excluded:
                qs = qs.where(db.project_id.not_in(excluded))
            return qs

        issues = issuedb.rows(
            query=query_fn,
            order="DESC",
            orderby="updated",
            page=page,
            dump=limit,
            fields="id,project_id,title,status,level,user_id,worker,updated,planend"
        )

        total = issuedb.count(query=query_fn)

        # 프로젝트 정보 매핑
        project_cache = {}
        for item in issues:
            pid = item['project_id']
            if pid not in project_cache:
                p = projectdb.get(id=pid, fields="id,namespace,title,short,icon")
                project_cache[pid] = p if p else {}
            item['project'] = project_cache[pid]

        # 읽음/멘션 상태 매핑
        for item in issues:
            iid = item['id']
            # is_read: read 테이블과 mention 테이블 모두 확인
            item_read = read_map.get(iid, True)
            item_mention_read = mention_read_map.get(iid, True)
            item['is_read'] = item_read and item_mention_read
            item['is_mentioned'] = iid in mention_id_set

        return {'items': issues, 'total': total}

    @staticmethod
    def mentioned_issues(limit=20, page=1):
        """멘션된 이슈만 조회 (읽음/안읽음 모두 포함)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        mention_records = mentiondb.rows(mentioned_user_id=user_id, fields="issue_id,is_read")
        mention_issue_ids = [m['issue_id'] for m in mention_records]
        mention_read_map = {m['issue_id']: m['is_read'] for m in mention_records}

        if not mention_issue_ids:
            return {'items': [], 'total': 0}

        def query_fn(db, qs):
            qs = qs.where(db.id.in_(mention_issue_ids))
            if excluded:
                qs = qs.where(db.project_id.not_in(excluded))
            return qs

        issues = issuedb.rows(
            query=query_fn,
            order="DESC",
            orderby="updated",
            page=page,
            dump=limit,
            fields="id,project_id,title,status,level,user_id,worker,updated,planend"
        )

        total = issuedb.count(query=query_fn)

        # 프로젝트 정보 매핑
        project_cache = {}
        for item in issues:
            pid = item['project_id']
            if pid not in project_cache:
                p = projectdb.get(id=pid, fields="id,namespace,title,short,icon")
                project_cache[pid] = p if p else {}
            item['project'] = project_cache[pid]

        # 읽음 상태 매핑 (read 테이블도 함께 확인)
        read_records = readdb.rows(user_id=user_id, issue_id=mention_issue_ids, fields="issue_id,is_read")
        read_map = {r['issue_id']: r['is_read'] for r in read_records}
        for item in issues:
            iid = item['id']
            mention_is_read = mention_read_map.get(iid, True)
            read_is_read = read_map.get(iid, True)
            item['is_read'] = mention_is_read and read_is_read
            item['is_mentioned'] = True

        return {'items': issues, 'total': total}

    @staticmethod
    def issues_by_project(limit=5):
        """프로젝트별 배정 이슈 분포 (상위 N개)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        def query_assigned(db, qs):
            base = db.worker_id.in_([user_id]) & db.status.in_(['open', 'work', 'finish']) & db.role.in_(['manager'])
            if excluded:
                base = base & db.project_id.not_in(excluded)
            qs = qs.where(base)
            return qs

        assigned = issueworkerdb.rows(
            query=query_assigned,
            fields='id,project_id',
            groupby="id"
        )

        project_counts = {}
        for item in assigned:
            pid = item['project_id']
            project_counts[pid] = project_counts.get(pid, 0) + 1

        sorted_projects = sorted(project_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

        result = []
        for pid, count in sorted_projects:
            p = projectdb.get(id=pid, fields="id,namespace,title,short,icon")
            if p:
                result.append({'project': p, 'count': count})

        return result

    @staticmethod
    def activity_trend(days=14):
        """최근 N일간 일별 이슈 활동 추이 (배정 이슈 기준)"""
        user_id = config.session_user_id()
        excluded = Model._excluded_project_ids()

        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=days - 1)
        start_str = start_date.strftime('%Y-%m-%d 00:00:00')

        def query_fn(db, qs):
            base = db.worker_id.in_([user_id]) & db.role.in_(['manager'])
            base = base & (db.updated >= start_str)
            if excluded:
                base = base & db.project_id.not_in(excluded)
            qs = qs.where(base)
            return qs

        rows = issueworkerdb.rows(
            query=query_fn,
            fields='id,updated',
            groupby="id"
        )

        day_counts = {}
        for r in rows:
            updated = r.get('updated', '')
            if updated:
                date_str = str(updated)[:10]
                day_counts[date_str] = day_counts.get(date_str, 0) + 1

        result = []
        for i in range(days):
            d = start_date + datetime.timedelta(days=i)
            date_str = d.strftime('%Y-%m-%d')
            result.append({
                'date': date_str,
                'count': day_counts.get(date_str, 0),
                'is_today': d == today
            })

        return result

    @staticmethod
    def load(meeting_limit=10):
        """대시보드 데이터 통합 조회"""
        projects = Model.my_projects()
        issues = Model.my_issues_summary()
        created_issues = Model.my_created_issues()
        meetings = Model.recent_meetings(limit=meeting_limit)
        plans = Model.my_plans()
        issues_by_project = Model.issues_by_project()
        activity_trend = Model.activity_trend()

        # 모든 데이터에서 user_id 수집
        user_ids = set()
        for item in issues.get('recent', []):
            user_ids.add(item.get('user_id', ''))
            for w in item.get('worker', []):
                user_ids.add(w)
        for item in created_issues:
            user_ids.add(item.get('user_id', ''))
        for item in meetings:
            user_ids.add(item.get('user_id', ''))

        user_ids.discard('')
        users = {}
        for uid in user_ids:
            users[uid] = config.get_user_info(wiz, uid)

        return {
            'projects': projects,
            'issues': issues,
            'created_issues': created_issues,
            'meetings': meetings,
            'plans': plans,
            'users': users,
            'issues_by_project': issues_by_project,
            'activity_trend': activity_trend
        }
