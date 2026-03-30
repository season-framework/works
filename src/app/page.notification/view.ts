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
    public tab: string = 'all';
    public users: any = {};

    // 이슈 상세 팝업
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

        let params: any = { page: this.page, dump: this.dump };
        if (this.tab === 'issue') params.ref_type = 'issue';
        else if (this.tab === 'calendar') params.ref_type = 'calendar';

        const { code, data } = await wiz.call('list', params);
        if (code == 200) {
            this.items = data.items || [];
            this.total = data.total || 0;
            this.users = data.users || {};
        }
        this.loading = false;
        await this.service.render();
    }

    public async markRead(item: any) {
        if (item.is_read) return;
        await wiz.call('mark_read', { notification_id: item.id });
        item.is_read = true;
        await this.service.render();
    }

    public async markAllRead() {
        const res = await this.service.alert.show({
            title: "모두 읽음",
            message: "모든 알림을 읽음 처리하시겠습니까?",
            action: "확인",
            cancel: "취소",
        });
        if (!res) return;
        await wiz.call('mark_all_read');
        for (let item of this.items) {
            item.is_read = true;
        }
        await this.service.render();
    }

    public async onClickItem(item: any) {
        await this.markRead(item);
        if (item.ref_type === 'issue') {
            await this.openIssue(item);
        } else if (item.ref_type === 'calendar') {
            if (item.project && item.project.namespace) {
                this.service.href(`/project/${item.project.namespace}/calendar`);
            }
        }
    }

    public async openIssue(item: any) {
        await this.project.init(item.project_id);

        this.issue.id = item.ref_id || item.issue_id;
        this.issue.event = {};
        this.issue.modal = true;
        this.issue.parent = this;
        this.issue.loaded = false;

        this.issue.event.hide = (async () => {
            this.issue.id = null;
            this.issue.modal = false;
            this.issue.loaded = false;
            await this.service.render();
            await this.loadPage();
        }).bind(this);

        this.issue.event.onLoad = (async () => {
            this.issue.loaded = true;
            await this.service.render();
        }).bind(this);

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

    public displayDate(date: any) {
        if (!date) return '-';
        let targetdate = moment(date);
        let diff = new Date().getTime() - new Date(targetdate as any).getTime();
        diff = diff / 1000 / 60 / 60;
        if (diff > 24 * 7) return targetdate.format("YY.MM.DD");
        if (diff > 24) return targetdate.format("M월 D일");
        if (diff > 1) return Math.floor(diff) + "시간전";
        diff = diff * 60;
        if (diff < 2) return "방금전";
        return Math.floor(diff) + "분전";
    }

    public displayShortDate(date: any) {
        if (!date) return '';
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
        } catch { return false; }
    }

    public typeIcon(type: string) {
        if (type?.startsWith('calendar')) return { icon: 'ti-calendar-event', cls: 'text-green-500' };
        if (type?.startsWith('issue_mentioned')) return { icon: 'ti-at', cls: 'text-amber-500' };
        if (type?.startsWith('issue')) return { icon: 'ti-message-circle', cls: 'text-blue-500' };
        return { icon: 'ti-bell', cls: 'text-neutral-400' };
    }

    public typeLabel(type: string) {
        const labels: any = {
            'calendar_invited': '캘린더 초대',
            'calendar_updated': '캘린더 수정',
            'calendar_deleted': '캘린더 삭제',
            'issue_assigned': '이슈',
            'issue_mentioned': '멘션',
        };
        return labels[type] || type;
    }
}
