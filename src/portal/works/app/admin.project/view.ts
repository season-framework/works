import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public projects: any[] = [];
    public keyword: string = '';
    public filterStatus: string = '';
    public filterVisibility: string = '';
    public searchFocused: boolean = false;
    public page: number = 1;
    public lastPage: number = 1;
    public total: number = 0;
    public dump: number = 20;

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.loadProjects();
    }

    public async loadProjects() {
        const params: any = {
            page: this.page,
            dump: this.dump,
        };
        if (this.keyword) params.keyword = this.keyword;
        if (this.filterStatus) params.status = this.filterStatus;
        if (this.filterVisibility) params.visibility = this.filterVisibility;

        const { code, data } = await wiz.call("project_list", params);
        if (code === 200) {
            this.projects = data.rows || [];
            this.total = data.total || 0;
            this.lastPage = data.last_page || 1;
            this.page = data.page || 1;
        }
        await this.service.render();
    }

    public async search() {
        this.page = 1;
        await this.loadProjects();
    }

    public async goPage(p: number) {
        if (p < 1 || p > this.lastPage) return;
        this.page = p;
        await this.loadProjects();
    }

    public pageList(): number[] {
        const pages: number[] = [];
        const maxVisible = 10;
        let start = Math.max(1, this.page - Math.floor(maxVisible / 2));
        let end = Math.min(this.lastPage, start + maxVisible - 1);
        if (end - start + 1 < maxVisible) {
            start = Math.max(1, end - maxVisible + 1);
        }
        for (let i = start; i <= end; i++) {
            pages.push(i);
        }
        return pages;
    }

    public statusLabel(status: string): string {
        const labels: any = { draft: '초안', open: '운영', close: '종료' };
        return labels[status] || status;
    }

    public visibilityLabel(vis: string): string {
        const labels: any = { public: '공개', internal: '내부', private: '비공개' };
        return labels[vis] || vis;
    }

    public async changeStatus(project: any, newStatus: string) {
        if (project.status === newStatus) return;
        const { code } = await wiz.call("project_update_status", { id: project.id, status: newStatus });
        if (code === 200) {
            project.status = newStatus;
            await this.service.render();
        }
    }

    public async deleteProject(project: any) {
        const res = await this.service.alert.show({
            title: '프로젝트 삭제',
            status: 'error',
            message: `"${project.title || project.namespace}" 프로젝트를 삭제하시겠습니까?\n관련 데이터(멤버, 이슈 등)도 함께 삭제됩니다.`,
            action: '삭제',
            actionBtn: 'error',
            cancel: '취소',
        });
        if (!res) return;
        const { code } = await wiz.call("project_delete", { id: project.id });
        if (code === 200) {
            await this.loadProjects();
        }
    }

    public async viewStorage(project: any) {
        const { code, data } = await wiz.call("project_storage", { id: project.id });
        if (code === 200) {
            await this.service.alert.show({
                title: '스토리지 사용량',
                status: 'info',
                message: `${project.title || project.namespace}: ${data.size_mb} MB`,
                action: '확인',
            });
        }
    }
}
