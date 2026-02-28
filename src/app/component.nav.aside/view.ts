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
        keyword: '',
        highlightIndex: -1,
        panelStyle: {}
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
            this.projectSwitcher.highlightIndex = -1;
            // 트리거 버튼 위치 기반으로 fixed 드롭다운 좌표 계산
            const trigger = event.currentTarget as HTMLElement;
            const rect = trigger.getBoundingClientRect();
            this.projectSwitcher.panelStyle = {
                'bottom': (window.innerHeight - rect.top + 4) + 'px',
                'left': rect.left + 'px'
            };
        }
        this.service.render();
    }

    public onSwitcherKeydown(event: KeyboardEvent) {
        const items = this.filteredProjects();
        if (event.key === 'ArrowDown') {
            event.preventDefault();
            this.projectSwitcher.highlightIndex = Math.min(this.projectSwitcher.highlightIndex + 1, items.length - 1);
            this.scrollToHighlighted();
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            this.projectSwitcher.highlightIndex = Math.max(this.projectSwitcher.highlightIndex - 1, 0);
            this.scrollToHighlighted();
        } else if (event.key === 'Enter') {
            event.preventDefault();
            if (this.projectSwitcher.highlightIndex >= 0 && this.projectSwitcher.highlightIndex < items.length) {
                this.switchProject(items[this.projectSwitcher.highlightIndex]);
            }
        } else if (event.key === 'Escape') {
            this.projectSwitcher.open = false;
        }
        this.service.render();
    }

    private scrollToHighlighted() {
        setTimeout(() => {
            const container = document.querySelector('.project-switcher-list');
            const active = container?.querySelector('.project-switcher-highlight');
            if (active && container) {
                active.scrollIntoView({ block: 'nearest' });
            }
        }, 0);
    }

    public filteredProjects(): any[] {
        const kw = (this.projectSwitcher.keyword || '').trim().toLowerCase();
        if (!kw) return this.projectSwitcher.projects;
        return this.projectSwitcher.projects.filter((p: any) =>
            (p.title || '').toLowerCase().includes(kw) ||
            (p.short || '').toLowerCase().includes(kw) ||
            (p.namespace || '').toLowerCase().includes(kw)
        );
    }

    public onSwitcherInput() {
        this.projectSwitcher.highlightIndex = this.filteredProjects().length > 0 ? 0 : -1;
    }

    public switchProject(p: any) {
        this.projectSwitcher.open = false;
        // 현재 보고 있는 메뉴를 유지하여 이동, 프로젝트 페이지가 아니면 기본 경로로
        const currentMenu = WizRoute.segment?.menu;
        if (currentMenu) {
            this.service.href(`/project/${p.namespace}/${currentMenu}`);
        } else {
            this.service.href(`/project/${p.namespace}`);
        }
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