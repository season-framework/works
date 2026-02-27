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
    def load(meeting_limit=10):
        """대시보드 데이터 통합 조회"""
        projects = Model.my_projects()
        issues = Model.my_issues_summary()
        created_issues = Model.my_created_issues()
        meetings = Model.recent_meetings(limit=meeting_limit)
        plans = Model.my_plans()

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
            'users': users
        }
