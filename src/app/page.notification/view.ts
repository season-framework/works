import { OnInit } from "@angular/core";
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

import moment from 'moment';

export class Component implements OnInit {
    constructor(public service: Service, public project: Project) { }

    public items: any[] = [];
    public total: number = 0;
    public page: number = 1;
    public dump: number = 20;
    public loading: boolean = false;
    public tab: string = 'all'; // 'all' | 'mention'
    public users: any = {};
    public issue: any = { id: null, modal: false, event: {} };

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.init();
        await this.service.auth.allow(true, '/authenticate');
        await this.service.render();
        await this.loadPage();
    }

    public async switchTab(tab: string) {
        if (this.tab === tab) return;
        this.tab = tab;
        this.page = 1;
        this.items = [];
        this.total = 0;
        await this.service.render();
        await this.loadPage();
    }

    public async loadPage() {
        this.loading = true;
        await this.service.render();
        const apiName = this.tab === 'mention' ? 'mentioned_issues' : 'all_issues';
        const { code, data } = await wiz.call(apiName, { page: this.page, dump: this.dump });
        if (code == 200) {
            this.items = data.items || [];
            this.total = data.total || 0;
            this.users = data.users || {};
        }
        this.loading = false;
        await this.service.render();
    }

    public async prevPage() {
        if (this.page <= 1) return;
        this.page--;
        await this.loadPage();
    }

    public async nextPage() {
        if (this.page >= this.maxPage()) return;
        this.page++;
        await this.loadPage();
    }

    public maxPage(): number {
        return Math.ceil(this.total / this.dump) || 1;
    }

    public async openIssue(item: any) {
        if (!item.project || !item.project.namespace) return;
        try {
            await this.project.init(item.project.namespace);
        } catch (e) {
            return;
        }
        this.issue = {
            id: item.id,
            modal: true,
            event: {
                hide: async () => {
                    this.issue = { id: null, modal: false, event: {} };
                    await this.loadPage();
                    await this.service.render();
                }
            }
        };
        await this.service.render();
    }

    public getUserName(userId: string) {
        const user = this.users[userId];
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
        return moment(date).format("YY.MM.DD");
    }

    public displayStatus(status: string) {
        if (status == 'open') return { text: '대기', cls: 'bg-neutral-100 text-neutral-500 ring-neutral-200' };
        if (status == 'work') return { text: '진행', cls: 'bg-blue-50 text-blue-700 ring-blue-200' };
        if (status == 'finish') return { text: '완료', cls: 'bg-green-50 text-green-700 ring-green-200' };
        if (status == 'close') return { text: '종료', cls: 'bg-neutral-100 text-neutral-500 ring-neutral-200' };
        if (status == 'cancel') return { text: '취소', cls: 'bg-red-50 text-red-700 ring-red-200' };
        return { text: status, cls: 'bg-neutral-100 text-neutral-500 ring-neutral-200' };
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
}
