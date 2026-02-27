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
    public plans: any[] = [];
    public users: any = {};

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.init();
        await this.service.auth.allow(true, '/authenticate');
        await this.service.render();
        await this.load();
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
            this.plans = data.plans || [];
            this.users = data.users || {};
        }
        this.loaded = true;
        await this.service.render();
    }

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
        if (status == 'open') return { text: '대기', cls: 'bg-slate-100 text-gray-500' };
        if (status == 'work') return { text: '진행', cls: 'bg-lime-100 text-lime-600' };
        if (status == 'finish') return { text: '완료', cls: 'bg-emerald-100 text-emerald-600' };
        if (status == 'close') return { text: '종료', cls: 'bg-red-100 text-red-500' };
        if (status == 'cancel') return { text: '취소', cls: 'bg-red-100 text-red-500' };
        return { text: status, cls: 'bg-slate-100 text-gray-500' };
    }

    public displayRole(role: string) {
        if (role == 'admin') return { text: '관리자', cls: 'bg-purple-100 text-purple-600' };
        if (role == 'manager') return { text: '매니저', cls: 'bg-blue-100 text-blue-600' };
        if (role == 'user') return { text: '멤버', cls: 'bg-green-100 text-green-600' };
        if (role == 'guest') return { text: '게스트', cls: 'bg-gray-100 text-gray-500' };
        return { text: role, cls: 'bg-gray-100 text-gray-500' };
    }

    public displayPlanStatus(status: string) {
        if (status == 'ready') return { text: '준비', cls: 'bg-slate-100 text-gray-500' };
        if (status == 'active') return { text: '진행', cls: 'bg-lime-100 text-lime-600' };
        if (status == 'finish') return { text: '완료', cls: 'bg-emerald-100 text-emerald-600' };
        return { text: status, cls: 'bg-slate-100 text-gray-500' };
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

    public navigateProject(namespace: string) {
        this.service.href('/project/' + namespace);
    }

    public navigateIssues() {
        this.service.href('/issues');
    }
}