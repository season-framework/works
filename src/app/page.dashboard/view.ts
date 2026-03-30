import { OnInit } from "@angular/core";
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

import moment from 'moment';

export class Component implements OnInit {
    constructor(
        public service: Service,
        public project: Project
    ) { }

    public loaded: boolean = false;
    public projects: any[] = [];
    public issues: any = { counts: { open: 0, work: 0, finish: 0 }, total: 0, recent: [] };
    public createdIssues: any[] = [];
    public meetings: any[] = [];
    public users: any = {};

    // 알림
    public notifications: any[] = [];
    public notifTotal: number = 0;

    // 이슈 상세 팝업
    public issue: any = { id: null, modal: false, event: {} };

    // 활동 통계
    public issuesByProject: any[] = [];
    public activityTrend: any[] = [];
    public maxProjectIssueCount: number = 1;
    public maxTrendCount: number = 0;

    // 캘린더
    public calYear: number = new Date().getFullYear();
    public calMonth: number = new Date().getMonth() + 1;
    public calEvents: any[] = [];
    public calWeeks: any[][] = [];
    public calLoading: boolean = false;
    public calSelectedDate: string = '';
    public calSelectedEvents: any[] = [];

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.init();
        await this.service.auth.allow(true, '/authenticate');
        await this.service.render();
        await this.load();
        await this.loadCalendar();
    }

    public async load() {
        this.loaded = false;
        await this.service.render();
        const { code, data } = await wiz.call("load");
        if (code == 200) {
            this.projects = data.projects || [];
            this.issues = data.issues || { counts: { open: 0, work: 0, finish: 0 }, total: 0, recent: [] };
            this.createdIssues = data.created_issues || [];
            this.meetings = data.meetings || [];
            this.users = data.users || {};
            this.issuesByProject = data.issues_by_project || [];
            this.activityTrend = data.activity_trend || [];
            this.maxProjectIssueCount = Math.max(...this.issuesByProject.map((i: any) => i.count), 1);
            this.maxTrendCount = Math.max(...this.activityTrend.map((i: any) => i.count), 0);
        }
        this.loaded = true;
        await this.service.render();

        // 알림 로드 (비동기)
        await this.loadNotifications();
    }

    public async loadNotifications() {
        const { code, data } = await wiz.call("notifications", { dump: 10 });
        if (code == 200) {
            this.notifications = data.items || [];
            this.notifTotal = data.total || 0;
        }
        await this.service.render();
    }

    public async onNotifClick(item: any) {
        if (item.ref_type === 'issue') {
            await this.openIssue(item);
        } else if (item.ref_type === 'calendar') {
            if (item.project && item.project.namespace) {
                this.service.href(`/project/${item.project.namespace}/calendar`);
            }
        } else {
            this.service.href('/notification');
        }
    }

    public async openIssue(item: any) {
        await this.project.init(item.project_id);

        this.issue.id = item.ref_id || item.issue_id || item.id;
        this.issue.event = {};
        this.issue.modal = true;
        this.issue.parent = this;
        this.issue.loaded = false;

        this.issue.event.hide = (async () => {
            this.issue.id = null;
            this.issue.modal = false;
            this.issue.loaded = false;
            await this.service.render();
            await this.loadNotifications();
        }).bind(this);

        this.issue.event.onLoad = (async () => {
            this.issue.loaded = true;
            await this.service.render();
        }).bind(this);

        await this.service.render();
    }

    public notifTypeLabel(type: string) {
        const labels: any = {
            'calendar_invited': '캘린더 초대',
            'calendar_updated': '캘린더 수정',
            'calendar_deleted': '캘린더 삭제',
            'issue_assigned': '이슈',
            'issue_mentioned': '멘션',
        };
        return labels[type] || type;
    }

    // ── 캘린더 로직 ──

    public navigateToIssue(item: any) {
        if (item.project && item.project.namespace) {
            this.service.href(`/project/${item.project.namespace}/issueboard/${item.id}`);
        }
    }

    public async loadCalendar() {
        this.calLoading = true;
        await this.service.render();
        const { code, data } = await wiz.call("my_calendar", { year: this.calYear, month: this.calMonth });
        if (code == 200) {
            this.calEvents = data.events || [];
        } else {
            this.calEvents = [];
        }
        this.buildCalendarGrid();
        this.calLoading = false;
        await this.service.render();
    }

    public buildCalendarGrid() {
        const year = this.calYear;
        const month = this.calMonth;
        const firstDay = new Date(year, month - 1, 1);
        const lastDay = new Date(year, month, 0);
        const startDow = firstDay.getDay(); // 0=Sun
        const totalDays = lastDay.getDate();

        const today = moment().format('YYYY-MM-DD');
        const weeks: any[][] = [];
        let week: any[] = [];

        // 이전 달 빈칸
        for (let i = 0; i < startDow; i++) {
            week.push({ day: 0, date: '', events: [], isToday: false, isCurrentMonth: false });
        }

        for (let d = 1; d <= totalDays; d++) {
            const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
            const dayEvents = this.calEvents.filter(ev => {
                const evStart = (ev.start || '').substring(0, 10);
                const evEnd = (ev.end || '').substring(0, 10);
                return dateStr >= evStart && dateStr <= evEnd;
            });
            week.push({
                day: d,
                date: dateStr,
                events: dayEvents,
                isToday: dateStr === today,
                isCurrentMonth: true
            });
            if (week.length === 7) {
                weeks.push(week);
                week = [];
            }
        }

        // 남은 빈칸
        if (week.length > 0) {
            while (week.length < 7) {
                week.push({ day: 0, date: '', events: [], isToday: false, isCurrentMonth: false });
            }
            weeks.push(week);
        }

        this.calWeeks = weeks;
    }

    public async calPrev() {
        this.calMonth--;
        if (this.calMonth < 1) {
            this.calMonth = 12;
            this.calYear--;
        }
        this.calSelectedDate = '';
        this.calSelectedEvents = [];
        await this.loadCalendar();
    }

    public async calNext() {
        this.calMonth++;
        if (this.calMonth > 12) {
            this.calMonth = 1;
            this.calYear++;
        }
        this.calSelectedDate = '';
        this.calSelectedEvents = [];
        await this.loadCalendar();
    }

    public async calToday() {
        const now = new Date();
        this.calYear = now.getFullYear();
        this.calMonth = now.getMonth() + 1;
        this.calSelectedDate = '';
        this.calSelectedEvents = [];
        await this.loadCalendar();
    }

    public async selectDate(cell: any) {
        if (!cell.isCurrentMonth) return;
        if (this.calSelectedDate === cell.date) {
            this.calSelectedDate = '';
            this.calSelectedEvents = [];
        } else {
            this.calSelectedDate = cell.date;
            this.calSelectedEvents = cell.events;
        }
        await this.service.render();
    }

    public calMonthLabel(): string {
        return `${this.calYear}년 ${this.calMonth}월`;
    }

    public calEventColor(ev: any): string {
        if (ev.category && ev.category.color) return ev.category.color;
        if (ev.color) return ev.color;
        return '#6366f1';
    }

    public calFormatTime(dateStr: string): string {
        if (!dateStr) return '';
        return moment(dateStr).format('HH:mm');
    }

    public calFormatDateRange(ev: any): string {
        if (!ev.start) return '';
        const s = moment(ev.start);
        const e = ev.end ? moment(ev.end) : null;
        if (ev.all_day) {
            if (e && !s.isSame(e, 'day')) {
                return `${s.format('M/D')} ~ ${e.format('M/D')}`;
            }
            return s.format('M월 D일');
        }
        if (e && !s.isSame(e, 'day')) {
            return `${s.format('M/D HH:mm')} ~ ${e.format('M/D HH:mm')}`;
        }
        if (e) {
            return `${s.format('HH:mm')} ~ ${e.format('HH:mm')}`;
        }
        return s.format('HH:mm');
    }

    // ── 기존 유틸리티 ──

    public getUserInfo(userId: string) {
        return this.users[userId] || null;
    }

    public getUserName(userId: string) {
        const user = this.getUserInfo(userId);
        return user ? user.name : '-';
    }

    public displayDate(date: any) {
        if (!date) return '-';
        let targetdate = moment(date);
        let diff = new Date().getTime() - new Date(targetdate).getTime();
        diff = diff / 1000 / 60 / 60;
        if (diff > 24 * 7) return targetdate.format("YY.MM.DD");
        if (diff > 24) return targetdate.format("M월 D일");
        if (diff > 1) return Math.floor(diff) + "시간전";
        diff = diff * 60;
        if (diff < 2) return "방금전";
        return Math.floor(diff) + "분전";
    }

    public displayShortDate(date: any) {
        if (!date) return '-';
        let targetdate = moment(date);
        return targetdate.format("YY.MM.DD");
    }

    public displayStatus(status: string) {
        if (status == 'open') return { text: '대기', cls: 'bg-neutral-100 text-neutral-500 ring-neutral-200' };
        if (status == 'work') return { text: '진행', cls: 'bg-blue-50 text-blue-700 ring-blue-200' };
        if (status == 'finish') return { text: '완료', cls: 'bg-green-50 text-green-700 ring-green-200' };
        if (status == 'close') return { text: '종료', cls: 'bg-neutral-100 text-neutral-500 ring-neutral-200' };
        if (status == 'cancel') return { text: '취소', cls: 'bg-red-50 text-red-700 ring-red-200' };
        return { text: status, cls: 'bg-neutral-100 text-neutral-500 ring-neutral-200' };
    }

    public displayRole(role: string) {
        if (role == 'admin') return { text: '관리자', cls: 'bg-purple-50 text-purple-700 ring-purple-200' };
        if (role == 'manager') return { text: '매니저', cls: 'bg-blue-50 text-blue-700 ring-blue-200' };
        if (role == 'user') return { text: '멤버', cls: 'bg-green-50 text-green-700 ring-green-200' };
        if (role == 'guest') return { text: '게스트', cls: 'bg-neutral-100 text-neutral-500 ring-neutral-200' };
        return { text: role, cls: 'bg-neutral-100 text-neutral-500 ring-neutral-200' };
    }

    public isOverdue(planend: any) {
        if (!planend) return false;
        try {
            let endtime = new Date(planend).getTime();
            let now = new Date().getTime();
            return now - endtime > 1000 * 60 * 60 * 24;
        } catch (e) {
            return false;
        }
    }

    public trendDayLabel(dateStr: string): string {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        const labels = ['일', '월', '화', '수', '목', '금', '토'];
        return labels[d.getDay()];
    }

    public navigateProject(namespace: string) {
        this.service.href('/project/' + namespace);
    }

    public navigateIssues() {
        this.service.href('/issues');
    }
}
