import { OnInit, OnDestroy, HostListener } from '@angular/core';
import { ElementRef, ViewChild } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

export class Component implements OnInit, OnDestroy {
    constructor(
        public service: Service,
        public project: Project
    ) { }

    @HostListener('document:click')
    public onDocumentClick() {
        if (this.statusFilterOpen) {
            this.statusFilterOpen = false;
            this.service.render();
        }
    }

    @ViewChild('container')
    public workspace: ElementRef;

    public socket: any = null;
    public labels: any = [];

    public readOnly: boolean = true;

    public cache: any = {
        label: '',
        loaded: false,
        issues: {},
        hiddenIssues: {}
    };

    public issue: any = {
        id: null,
        modal: false,
        event: {}
    };

    public config: any = {
        labelSorted: {
            animation: 0,
            handle: '.btn-action-move'
        },
        issueSorted: {
            animation: 0,
            handle: '.issue-card',
            group: 'issue'
        }
    };

    public async alert(message: string, title: any = "", status: any = "error", action: string = '확인', cancel: any = false) {
        return await this.service.alert.show({
            title: title,
            message: message,
            cancel: cancel,
            actionBtn: status,
            action: action,
            status: status
        });
    }

    public async ngOnInit() {
        let self = this;
        this.config.issueSorted.onEnd = this.config.labelSorted.onEnd = async () => {
            let labels = self.labels;
            await self.updateLabels(labels);

            for (let i = 0; i < labels.length; i++) {
                let label = labels[i];

                for (let j = 0; j < label.issues.length; j++) {
                    let issueId = label.issues[j];
                    if (!this.cache.issues[issueId]) continue;
                    if (!this.cache.issues[issueId].label_id) continue;
                    if (label.id != this.cache.issues[issueId].label_id) {
                        let pd = {};
                        pd.issue_id = this.cache.issues[issueId].id;
                        pd.label_id = label.id;
                        this.pendingUpdateIssues.push(pd);
                        this.cache.issues[issueId].label_id = label.id;
                    }
                }
            }

            await this.updateIssueLabels();
        }

        this.readOnly = !this.project.accessLevel(['admin', 'manager', 'user']);
        if (this.readOnly) {
            this.config.labelSorted.handle = '.no-drag';
            this.config.issueSorted.handle = '.no-drag';
        }

        await this.service.init();
        await this.project.member.load();

        this.socket = wiz.socket();

        this.socket.on("connect", async () => {
            this.socket.emit("join", { project_id: this.project.id() });
        });

        this.socket.on("label", async () => {
            await this.load();
        });

        this.socket.on("issue", async (issue_id: any) => {
            delete this.cache.issues[issue_id];
            if (this.issue.id == issue_id)
                if (this.issue.event.update)
                    await this.issue.event.update();
            await this.load();
        });

        this.socket.on("message", async (data: any) => {
            let issue_id: any = data.issue_id;
            if (this.issue.id == issue_id)
                if (this.issue.event.messages)
                    await this.issue.event.messages(data);
            await this.service.render();
        });

        await this.load();
    }

    public async ngOnDestroy() {
        this.socket.close();
    }

    public async start() {
        await this.service.loading.show();
        await this.addLabel("TODO");
        await this.addLabel("작업중");
        await this.addLabel("검증중");
        await this.addLabel("완료됨");
        await this.addLabel("미분류", 1);
        await this.service.loading.hide();
    }

    public async load() {
        const { data } = await wiz.call("load", { project_id: this.project.id() });
        this.labels = [];
        for (let i = 0; i < data.length; i++) {
            this.labels.push(data[i]);
        }
        await this.sortLabel();
        this.cache.loaded = true;
        await this.service.render();
    }

    public hiddenIssues(label_id: string, status: string, as_object: boolean = false) {
        try {
            let obj = this.cache.hiddenIssues[label_id][status];
            if (as_object) return obj ? obj : {};
            if (!obj.issues) return [];
            return obj.issues;
        } catch {
        }
        return [];
    }

    public async search(status: string, label: any, clear: boolean = false) {
        let query = { project_id: this.project.id() };

        let label_id = label.id;

        if (!this.cache.hiddenIssues[label_id])
            this.cache.hiddenIssues[label_id] = {};
        if (!this.cache.hiddenIssues[label_id][status])
            this.cache.hiddenIssues[label_id][status] = { page: 0, isLastPage: false, issues: [] };

        let obj = this.cache.hiddenIssues[label_id][status];

        if (clear) {
            if (obj.page > 0) {
                obj.page = 0;
                obj.isLastPage = false;
                obj.issues = [];
                await this.service.render();
                return;
            }
        }

        obj.page++;

        if (label.mode != 1) query.label_id = label.id;
        query.page = obj.page;
        query.status = status;

        const { code, data } = await wiz.call("search", query);
        if (code != 200) return;
        let { rows, lastpage } = data;

        if (obj.page == lastpage) {
            obj.isLastPage = true;
        }

        for (let i = 0; i < rows.length; i++) {
            if (obj.issues.includes(rows[i])) continue;
            obj.issues.push(rows[i]);
        }

        await this.service.render();
    }

    public async loadClosed(label: any, clear: boolean = false) {
        await this.search("close", label, clear);
    }

    public async loadCanceled(label: any, clear: boolean = false) {
        await this.search("cancel", label, clear);
    }

    public async sortLabel() {
        this.labels.sort((a, b) => {
            let modediff = a.mode - b.mode;
            if (modediff != 0) return modediff;
            return a.order - b.order;
        });
        await this.service.render();
    }

    public async addLabel(title: string, mode: number = 0) {
        if (!title) return;
        this.cache.label = "";

        let obj = {
            title, mode,
            order: this.labels.length + 1,
            project_id: this.project.id()
        };

        await wiz.call("addLabel", obj);
    }

    public async removeLabel(item: any) {
        if (item.mode == 1) return;
        let res = await this.alert(`'${item.title}' 라벨을 정말로 삭제하시겠습니까? 삭제된 라벨의 이슈는 미분류 항목으로 이동됩니다.`, "라벨 삭제", "error", "삭제", "취소");
        if (!res) return;
        const { code } = await wiz.call("removeLabel", item);
        if (code !== 200) return;
        this.labels.remove(item);
        await this.service.render();
    }

    public async updateLabels(items: any) {
        for (let i = 0; i < items.length; i++)
            items[i].order = i + 1;
        await wiz.call("updateLabels", { project_id: this.project.id(), data: JSON.stringify(items) });
    }

    public async addIssue(label: any) {
        await this.openIssue("new", label);
        await this.service.render();
    }

    public async openIssue(issueId: number | string = "new", label: any = null) {
        this.issue.id = issueId;
        this.issue.event = {};
        this.issue.modal = true;
        if (!label)
            label = this.labels[this.labels.length - 1];
        this.issue.label_id = label.id;
        this.issue.label = label;
        this.issue.parent = this;
        await this.service.render();
    }

    public pendingUpdateIssues: any = [];
    public isUpdateIssueLabel: boolean = false;
    public pendingIssues: any = [];
    public isLoadingIssue: boolean = false;

    public isLoadedIssue(issueId: any) {
        if (this.cache.issues[issueId])
            return true;

        this.loadIssue(issueId);
        return false;
    }

    public async updateIssueLabels() {
        if (this.isUpdateIssueLabel) return;
        this.isUpdateIssueLabel = true;

        let data = [];
        for (let i = 0; i < this.pendingUpdateIssues.length; i++) data.push(this.pendingUpdateIssues[i]);
        await wiz.call("updateIssue", { project_id: this.project.id(), data: JSON.stringify(data) });
        for (let i = 0; i < data.length; i++) this.pendingUpdateIssues.remove(data[i]);

        this.isUpdateIssueLabel = false;
        if (this.pendingUpdateIssues.length > 0)
            return this.updateIssueLabels();
    }

    public onProcessIssue(issue: any) {
        if (!issue) return true;
        // 상태 필터 적용
        if (this.statusFilter) {
            return issue.status === this.statusFilter;
        }
        return ["open", "work", "finish", "noti", "event"].includes(issue.status);
    }

    public async loadIssue(issueId: any) {
        if (!this.pendingIssues.includes(issueId))
            this.pendingIssues.push(issueId);
        if (this.isLoadingIssue)
            return;

        this.isLoadingIssue = true;

        let issueIds = JSON.stringify(this.pendingIssues);
        let { data } = await wiz.call("loadIssues", { project_id: this.project.id(), issueIds: issueIds });
        for (let i = 0; i < data.length; i++) {
            this.cache.issues[data[i].id] = data[i];
            this.pendingIssues.remove(data[i].id);
        }

        this.isLoadingIssue = false;
        await this.service.render();
    }

    public async scroll(move: any) {
        if (move == 'left') {
            this.workspace.nativeElement.scrollLeft = this.workspace.nativeElement.scrollLeft - 600;
        } else {
            this.workspace.nativeElement.scrollLeft = this.workspace.nativeElement.scrollLeft + 600;
        }
    }

    public labelExtended: any = {};

    public async gridOption(label) {
        this.labelExtended[label.id] = !this.labelExtended[label.id];
        await this.service.render();
    }

    public targetMember: any = null;
    public memberSearch: boolean = false;
    public memberSearchText: string = '';

    // ===== 상태 필터 (칸반/게시판 공통) =====
    public statusFilter: string = '';
    public statusFilterOpen: boolean = false;
    public statusFilterOptions: any[] = [
        { value: '', label: '전체' },
        { value: 'noti', label: '공지' },
        { value: 'event', label: '일정' },
        { value: 'open', label: '예정' },
        { value: 'work', label: '진행' },
        { value: 'finish', label: '완료' }
    ];

    public toggleStatusFilter(event: any) {
        event.stopPropagation();
        this.statusFilterOpen = !this.statusFilterOpen;
        this.service.render();
    }

    public async setStatusFilter(value: string) {
        this.statusFilter = value;
        this.statusFilterOpen = false;
        if (this.viewMode === 'board') {
            this.boardData.status = value || 'active';
            this.boardData.page = 1;
            await this.loadBoardData();
        }
        await this.service.render();
    }

    public statusFilterLabel(): string {
        const opt = this.statusFilterOptions.find(o => o.value === this.statusFilter);
        return opt ? opt.label : '전체';
    }

    public async selectMember() {
        if (this.memberSearch) this.targetMember = null;
        this.memberSearchText = '';
        this.memberSearch = !this.memberSearch;
        await this.service.render();
    }

    public searchMember(user: any, keyword: string) {
        if (!['admin', 'manager', 'user'].includes(user.role)) return false;
        if (user.meta.name.indexOf(keyword) >= 0) return true;
        return false;
    }

    public async searchByMember(target) {
        this.targetMember = target;
        this.memberSearch = false;
        await this.service.render();
    }

    public isSearchedUser(issue) {
        if (!this.targetMember) return true;
        if (issue.user_id == this.targetMember.meta.id) return true;
        if (issue.worker.includes(this.targetMember.meta.id)) return true;
        return false;
    }

    // ===== 보기 모드 (kanban / board) =====
    public viewMode: string = 'kanban';
    public boardData: any = {
        rows: [],
        page: 1,
        lastpage: 1,
        total: 0,
        status: 'active',
        loading: false,
        keyword: '',
        searchFocused: false
    };

    public async toggleViewMode() {
        this.viewMode = this.viewMode === 'kanban' ? 'board' : 'kanban';
        if (this.viewMode === 'board') {
            // 상태 필터가 설정되어 있으면 게시판 상태에 반영
            if (this.statusFilter) {
                this.boardData.status = this.statusFilter;
            } else {
                this.boardData.status = 'active';
            }
            this.boardData.page = 1;
            await this.loadBoardData();
        }
        await this.service.render();
    }

    public async loadBoardData() {
        this.boardData.loading = true;
        await this.service.render();

        const { code, data } = await wiz.call("loadAllIssues", {
            project_id: this.project.id(),
            page: this.boardData.page,
            status: this.boardData.status,
            keyword: this.boardData.keyword || ''
        });

        if (code === 200) {
            // 라벨별 서브헤더 삽입
            let processedRows = [];
            let lastLabelId = null;
            for (let row of (data.rows || [])) {
                if (row.label_id !== lastLabelId) {
                    processedRows.push({ _type: 'header', label_title: row.label_title, label_id: row.label_id });
                    lastLabelId = row.label_id;
                }
                row._type = 'data';
                processedRows.push(row);
            }
            this.boardData.rows = processedRows;
            this.boardData.lastpage = data.lastpage || 1;
            this.boardData.total = data.total || 0;
        }
        this.boardData.loading = false;
        await this.service.render();
    }

    public async boardChangePage(page: number) {
        if (page < 1 || page > this.boardData.lastpage) return;
        this.boardData.page = page;
        await this.loadBoardData();
    }

    public async boardChangeStatus(status: string) {
        this.boardData.status = status;
        this.boardData.page = 1;
        await this.loadBoardData();
    }

    public statusLabel(status: string): string {
        const map = { open: '예정', work: '진행중', finish: '완료', close: '종료', cancel: '취소', noti: '공지', event: '일정' };
        return map[status] || status;
    }

    public statusColor(status: string): string {
        const map = { open: 'bg-neutral-100 text-neutral-600', work: 'bg-blue-50 text-blue-600', finish: 'bg-emerald-50 text-emerald-600', close: 'bg-neutral-200 text-neutral-500', cancel: 'bg-red-50 text-red-500', noti: 'bg-amber-50 text-amber-600', event: 'bg-purple-50 text-purple-600' };
        return map[status] || 'bg-neutral-100 text-neutral-600';
    }

    public levelLabel(level: number): string {
        const map = { 0: '낮음', 1: '보통', 2: '중요', 3: '긴급' };
        return map[level] || '보통';
    }

    public levelColor(level: number): string {
        const map = { 0: 'text-neutral-400', 1: 'text-neutral-600', 2: 'text-amber-600', 3: 'text-red-600' };
        return map[level] || 'text-neutral-600';
    }

    public boardPageRange(): number[] {
        const pages = [];
        const start = Math.max(1, this.boardData.page - 2);
        const end = Math.min(this.boardData.lastpage, this.boardData.page + 2);
        for (let i = start; i <= end; i++) pages.push(i);
        return pages;
    }

    public async boardSearch() {
        this.boardData.page = 1;
        await this.loadBoardData();
    }

    public async boardClearSearch() {
        this.boardData.keyword = '';
        this.boardData.page = 1;
        await this.loadBoardData();
    }

}