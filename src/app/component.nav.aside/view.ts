import { OnInit } from '@angular/core';
import { HostListener } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

export class Component implements OnInit {
    constructor(
        public service: Service,
        public project: Project,
    ) { }

    // 프로젝트 스위칭 드롭다운
    public projectSwitcher: any = {
        open: false,
        projects: [],
        keyword: ''
    };

    public async ngOnInit() {
        await this.service.init();
        await this.loadMyProjects();
    }

    @HostListener('document:click', ['$event'])
    public clickout(event: any) {
        this.service.navbar.toggle(true);
        // 프로젝트 스위칭 드롭다운 외부 클릭 시 닫기
        const target = event?.target;
        if (target && !target.closest('.project-switcher-container')) {
            this.projectSwitcher.open = false;
        }
    }

    public async loadMyProjects() {
        try {
            const { code, data } = await wiz.call('my_projects');
            if (code === 200) {
                this.projectSwitcher.projects = data || [];
            }
        } catch (e) { }
    }

    public toggleProjectSwitcher(event: any) {
        event.stopPropagation();
        this.projectSwitcher.open = !this.projectSwitcher.open;
        if (this.projectSwitcher.open) {
            this.projectSwitcher.keyword = '';
        }
        this.service.render();
    }

    public filteredProjects(): any[] {
        const kw = (this.projectSwitcher.keyword || '').trim().toLowerCase();
        if (!kw) return this.projectSwitcher.projects;
        return this.projectSwitcher.projects.filter((p: any) =>
            (p.title || '').toLowerCase().includes(kw) ||
            (p.namespace || '').toLowerCase().includes(kw)
        );
    }

    public switchProject(p: any) {
        this.projectSwitcher.open = false;
        this.service.href(`/project/${p.namespace}/info`);
    }

    public async logout() {
        const res = await this.service.alert.show({
            title: "Logout",
            status: "error",
            message: "정말 로그아웃하시겠습니까?",
            action: "logout",
            actionBtn: "error",
            cancel: "cancel",
        });
        if (!res) return;
        location.href = "/auth/logout?returnTo=/authenticate";
    }
}