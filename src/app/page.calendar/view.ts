import { OnInit, OnDestroy, HostListener } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit, OnDestroy {
    constructor(public service: Service) { }

    public currentYear: number = new Date().getFullYear();
    public currentMonth: number = new Date().getMonth() + 1;
    public weeks: any[] = [];
    public events: any[] = [];
    public today: string = '';

    public selectedEvent: any = null;
    public showModal: boolean = false;

    // 프로젝트 필터
    public projects: any[] = [];
    public projectFilters: any = {};
    public showClosedProjects: boolean = false;
    public myOnly: boolean = false;
    public currentUserId: string = '';

    // 드래그앤드롭
    public draggedEvent: any = null;

    @HostListener('document:keydown.escape')
    public onEscKey() {
        if (this.showModal) {
            this.closeModal();
        }
    }

    public async ngOnInit() {
        await this.service.init();
        this.today = this.formatDate(new Date());
        try {
            await this.loadProjects();
            await this.loadEvents();
        } catch (e) {
            console.error(e);
        }
        this.service.auth.allow();
        await this.service.render();
    }

    ngOnDestroy() { }

    private formatDate(date: Date): string {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
    }

    // ── 프로젝트 로드 ──

    public async loadProjects() {
        const { code, data } = await wiz.call("my_projects");
        if (code === 200) {
            this.projects = data.projects || [];
            if (data.user_id) this.currentUserId = data.user_id;
            for (const p of this.projects) {
                if (!(p.id in this.projectFilters)) {
                    this.projectFilters[p.id] = true;
                }
            }
        }
    }

    public get displayProjects() {
        if (this.showClosedProjects) return this.projects;
        return this.projects.filter((p: any) => p.status !== 'close');
    }

    public toggleProject(projectId: string) {
        this.projectFilters[projectId] = !this.projectFilters[projectId];
        this.buildCalendar();
        this.service.render();
    }

    public get allProjectsChecked(): boolean {
        return this.displayProjects.every((p: any) => this.projectFilters[p.id] !== false);
    }

    public toggleAllProjects() {
        const newVal = !this.allProjectsChecked;
        for (const p of this.displayProjects) {
            this.projectFilters[p.id] = newVal;
        }
        this.buildCalendar();
        this.service.render();
    }

    public toggleShowClosed() {
        this.showClosedProjects = !this.showClosedProjects;
        this.buildCalendar();
        this.service.render();
    }

    public toggleMyOnly() {
        this.myOnly = !this.myOnly;
        this.buildCalendar();
        this.service.render();
    }

    public get filteredEvents() {
        return this.events.filter((ev: any) => {
            const pid = ev.project_id;
            if (this.projectFilters[pid] === false) return false;
            if (this.myOnly && this.currentUserId) {
                if (ev.user_id !== this.currentUserId) {
                    const isAttendee = (ev.attendees || []).some((a: any) => a.user_id === this.currentUserId);
                    if (!isAttendee) return false;
                }
            }
            return true;
        });
    }

    // ── 캘린더 그리드 ──

    public buildCalendar() {
        const year = this.currentYear;
        const month = this.currentMonth;

        const firstDay = new Date(year, month - 1, 1);
        const lastDay = new Date(year, month, 0);
        const startOffset = firstDay.getDay();
        const totalDays = lastDay.getDate();

        const prevLastDay = new Date(year, month - 1, 0);
        const prevTotalDays = prevLastDay.getDate();

        const days: any[] = [];

        for (let i = startOffset - 1; i >= 0; i--) {
            const d = prevTotalDays - i;
            const dateStr = this.formatDate(new Date(year, month - 2, d));
            days.push({ day: d, date: dateStr, currentMonth: false, events: [] });
        }

        for (let d = 1; d <= totalDays; d++) {
            const dateStr = this.formatDate(new Date(year, month - 1, d));
            days.push({ day: d, date: dateStr, currentMonth: true, events: [] });
        }

        const remaining = 7 - (days.length % 7);
        if (remaining < 7) {
            for (let d = 1; d <= remaining; d++) {
                const dateStr = this.formatDate(new Date(year, month, d));
                days.push({ day: d, date: dateStr, currentMonth: false, events: [] });
            }
        }

        const filtered = this.filteredEvents;
        for (const ev of filtered) {
            const evStart = ev.start.substring(0, 10);
            const evEnd = ev.end.substring(0, 10);
            for (const cell of days) {
                if (cell.date >= evStart && cell.date <= evEnd) {
                    cell.events.push(ev);
                }
            }
        }

        this.weeks = [];
        for (let i = 0; i < days.length; i += 7) {
            this.weeks.push(days.slice(i, i + 7));
        }
    }

    public async loadEvents() {
        const { code, data } = await wiz.call("search", {
            year: this.currentYear,
            month: this.currentMonth
        });
        if (code === 200) {
            this.events = data;
        } else {
            this.events = [];
        }
        this.buildCalendar();
        await this.service.render();
    }

    public async prevMonth() {
        this.currentMonth--;
        if (this.currentMonth < 1) {
            this.currentMonth = 12;
            this.currentYear--;
        }
        await this.loadEvents();
    }

    public async nextMonth() {
        this.currentMonth++;
        if (this.currentMonth > 12) {
            this.currentMonth = 1;
            this.currentYear++;
        }
        await this.loadEvents();
    }

    public async goToday() {
        const now = new Date();
        this.currentYear = now.getFullYear();
        this.currentMonth = now.getMonth() + 1;
        await this.loadEvents();
    }

    // ── 드래그앤드롭 ──

    public onDragStart(event: DragEvent, ev: any) {
        this.draggedEvent = ev;
        if (event.dataTransfer) {
            event.dataTransfer.effectAllowed = 'move';
            event.dataTransfer.setData('text/plain', ev.id);
        }
    }

    public onDragOver(event: DragEvent) {
        if (!this.draggedEvent) return;
        event.preventDefault();
        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = 'move';
        }
    }

    public async onDrop(event: DragEvent, cell: any) {
        event.preventDefault();
        if (!this.draggedEvent) return;

        const ev = this.draggedEvent;
        this.draggedEvent = null;

        const oldStart = ev.start.substring(0, 10);
        const newDate = cell.date;
        const diffMs = new Date(newDate).getTime() - new Date(oldStart).getTime();
        const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));
        if (diffDays === 0) return;

        const startDate = new Date(ev.start.replace(' ', 'T'));
        const endDate = new Date(ev.end.replace(' ', 'T'));
        startDate.setDate(startDate.getDate() + diffDays);
        endDate.setDate(endDate.getDate() + diffDays);

        const pad = (n: number) => String(n).padStart(2, '0');
        const fmtDt = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;

        const { code } = await wiz.call("move", {
            id: ev.id,
            project_id: ev.project_id,
            start: fmtDt(startDate),
            end: fmtDt(endDate)
        });
        if (code === 200) {
            await this.loadEvents();
        }
    }

    // ── 모달 (읽기 전용) ──

    public async openEvent(ev: any) {
        this.selectedEvent = ev;
        this.showModal = true;
        await this.service.render();
    }

    public closeModal() {
        this.showModal = false;
        this.selectedEvent = null;
        this.service.render();
    }

    public navigateToProject(ev: any) {
        if (ev.project_namespace) {
            this.service.href(`/project/${ev.project_namespace}/calendar`);
        }
    }

    public getEventColor(ev: any): string {
        if (ev.category && ev.category.color) return ev.category.color;
        return ev.color || '#3b82f6';
    }

    public getProjectTitle(projectId: string): string {
        const p = this.projects.find((x: any) => x.id === projectId);
        return p ? (p.title || p.namespace) : '';
    }

    public get monthLabel(): string {
        return `${this.currentYear}년 ${this.currentMonth}월`;
    }

    public dayNames: string[] = ['일', '월', '화', '수', '목', '금', '토'];
}
