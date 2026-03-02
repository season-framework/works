import { OnInit, OnDestroy, HostListener } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

export class Component implements OnInit, OnDestroy {
    constructor(
        public service: Service,
        public project: Project
    ) { }

    public readOnly: boolean = true;

    public currentYear: number = new Date().getFullYear();
    public currentMonth: number = new Date().getMonth() + 1;
    public weeks: any[] = [];
    public events: any[] = [];
    public today: string = '';

    public selectedEvent: any = null;
    public isEditing: boolean = false;
    public showModal: boolean = false;

    // 카테고리
    public categories: any[] = [];
    public categoryFilters: any = {};
    public showCategoryAdd: boolean = false;
    public newCategoryName: string = '';
    public newCategoryColor: string = '#3b82f6';
    public editingCategoryId: string = '';
    public editingCategoryName: string = '';
    public editingCategoryColor: string = '';

    // 카테고리 드래그앤드롭
    public draggedCategory: any = null;
    public dragOverCategoryId: string = '';

    // 참가자
    public members: any[] = [];
    public attendeeSearch: string = '';
    public showAttendeeDropdown: boolean = false;

    // 필터
    public showMyOnly: boolean = false;
    public showFilterSidebar: boolean = false;

    // 드래그앤드롭
    public draggedEvent: any = null;

    public eventForm: any = {
        title: '',
        description: '',
        start_date: '',
        start_time: '09:00',
        end_date: '',
        end_time: '18:00',
        all_day: false,
        color: '#3b82f6',
        category_id: '',
        attendees: []
    };

    public colors: string[] = [
        '#ef4444', '#f97316', '#f59e0b', '#eab308',
        '#22c55e', '#10b981', '#14b8a6', '#06b6d4',
        '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7',
        '#ec4899', '#f43f5e', '#78716c', '#64748b'
    ];

    @HostListener('document:keydown.escape')
    public onEscKey() {
        if (this.showModal) {
            this.closeModal();
        }
    }

    public async ngOnInit() {
        await this.service.init();
        this.readOnly = !this.project.accessLevel(['admin', 'manager', 'user']);
        this.today = this.formatDate(new Date());
        await this.loadCategories();
        await this.loadMembers();
        await this.loadEvents();
        await this.service.render();
    }

    ngOnDestroy() { }

    public async call(action: string, pd: any = {}) {
        pd.project_id = this.project.id();
        return await wiz.call(action, pd);
    }

    private formatDate(date: Date): string {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
    }

    // ── 카테고리 ──

    public async loadCategories() {
        const { code, data } = await this.call("categories");
        if (code === 200) {
            this.categories = data;
            for (const cat of this.categories) {
                if (!(cat.id in this.categoryFilters)) {
                    this.categoryFilters[cat.id] = true;
                }
            }
            if (!('__none__' in this.categoryFilters)) {
                this.categoryFilters['__none__'] = true;
            }
        }
    }

    public async addCategory() {
        if (!this.newCategoryName.trim()) return;
        const { code } = await this.call("create_category", {
            name: this.newCategoryName.trim(),
            color: this.newCategoryColor
        });
        if (code === 200) {
            this.newCategoryName = '';
            this.newCategoryColor = '#3b82f6';
            this.showCategoryAdd = false;
            await this.loadCategories();
            await this.service.render();
        }
    }

    public async startEditCategory(cat: any) {
        this.editingCategoryId = cat.id;
        this.editingCategoryName = cat.name;
        this.editingCategoryColor = cat.color || '#3b82f6';
        await this.service.render();
    }

    public async saveEditCategory(cat: any) {
        if (!this.editingCategoryName.trim()) return;
        await this.call("update_category", {
            id: cat.id,
            name: this.editingCategoryName.trim(),
            color: this.editingCategoryColor
        });
        this.editingCategoryId = '';
        await this.loadCategories();
        await this.service.render();
    }

    public async cancelEditCategory() {
        this.editingCategoryId = '';
        await this.service.render();
    }

    public async removeCategory(cat: any) {
        const res = await this.service.alert.show({
            title: '카테고리 삭제',
            message: `'${cat.name}' 카테고리를 삭제하시겠습니까?`,
            cancel: '취소',
            actionBtn: 'error',
            action: '삭제',
            status: 'error'
        });
        if (!res) return;
        await this.call("delete_category", { id: cat.id });
        await this.loadCategories();
        await this.loadEvents();
        await this.service.render();
    }

    // ── 카테고리 드래그앤드롭 ──

    public onCategoryDragStart(event: DragEvent, cat: any) {
        if (this.readOnly) return;
        this.draggedCategory = cat;
        if (event.dataTransfer) {
            event.dataTransfer.effectAllowed = 'move';
            event.dataTransfer.setData('text/plain', cat.id);
        }
    }

    public onCategoryDragOver(event: DragEvent, cat: any) {
        if (this.readOnly || !this.draggedCategory) return;
        if (this.draggedCategory.id === cat.id) return;
        event.preventDefault();
        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = 'move';
        }
        this.dragOverCategoryId = cat.id;
    }

    public async onCategoryDrop(event: DragEvent, targetCat: any) {
        event.preventDefault();
        if (this.readOnly || !this.draggedCategory) return;
        if (this.draggedCategory.id === targetCat.id) {
            this.draggedCategory = null;
            this.dragOverCategoryId = '';
            return;
        }

        const fromIndex = this.categories.findIndex((c: any) => c.id === this.draggedCategory.id);
        const toIndex = this.categories.findIndex((c: any) => c.id === targetCat.id);
        if (fromIndex === -1 || toIndex === -1) return;

        // 배열에서 이동
        const [moved] = this.categories.splice(fromIndex, 1);
        this.categories.splice(toIndex, 0, moved);

        this.draggedCategory = null;
        this.dragOverCategoryId = '';
        await this.service.render();

        // 서버에 순서 저장
        const orderList = this.categories.map((c: any, i: number) => ({
            id: c.id,
            sort_order: i + 1
        }));
        await this.call("reorder_categories", {
            order_list: JSON.stringify(orderList)
        });
    }

    public async onCategoryDragEnd() {
        this.draggedCategory = null;
        this.dragOverCategoryId = '';
        await this.service.render();
    }

    // ── 구성원 (참가자 용) ──

    public async loadMembers() {
        const { code, data } = await this.call("members");
        if (code === 200) {
            this.members = data;
        }
    }

    public get filteredMembers() {
        const selectedIds = (this.eventForm.attendees || []);
        const available = this.members.filter((m: any) => !selectedIds.includes(m.id));
        if (!this.attendeeSearch) return available.slice(0, 5);
        const q = this.attendeeSearch.toLowerCase();
        return available.filter((m: any) => {
            return (m.name && m.name.toLowerCase().includes(q)) ||
                   (m.email && m.email.toLowerCase().includes(q));
        }).slice(0, 5);
    }

    public delayHideDropdown() {
        setTimeout(() => {
            this.showAttendeeDropdown = false;
        }, 200);
    }

    public addAttendeeToForm(member: any) {
        if (!this.eventForm.attendees) this.eventForm.attendees = [];
        if (!this.eventForm.attendees.includes(member.id)) {
            this.eventForm.attendees.push(member.id);
        }
        this.attendeeSearch = '';
        this.showAttendeeDropdown = false;
    }

    public removeAttendeeFromForm(userId: string) {
        this.eventForm.attendees = (this.eventForm.attendees || []).filter((id: string) => id !== userId);
    }

    public getMemberName(userId: string): string {
        const m = this.members.find((x: any) => x.id === userId);
        return m ? (m.name || m.email) : userId;
    }

    // ── 필터 ──

    public toggleMyOnly() {
        this.showMyOnly = !this.showMyOnly;
        this.buildCalendar();
        this.service.render();
    }

    public toggleCategoryFilter(catId: string) {
        this.categoryFilters[catId] = !this.categoryFilters[catId];
        this.buildCalendar();
        this.service.render();
    }

    public get filteredEvents() {
        let evts = this.events;
        if (this.showMyOnly) {
            const myId = this.service.auth.session?.id;
            evts = evts.filter((ev: any) => {
                if (ev.user_id === myId) return true;
                if (ev.attendees && ev.attendees.some((a: any) => a.user_id === myId)) return true;
                return false;
            });
        }
        evts = evts.filter((ev: any) => {
            const catId = ev.category_id || '__none__';
            return this.categoryFilters[catId] !== false;
        });
        return evts;
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
        const { code, data } = await this.call("search", {
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
        if (this.readOnly) return;
        this.draggedEvent = ev;
        if (event.dataTransfer) {
            event.dataTransfer.effectAllowed = 'move';
            event.dataTransfer.setData('text/plain', ev.id);
        }
    }

    public onDragOver(event: DragEvent) {
        if (this.readOnly || !this.draggedEvent) return;
        event.preventDefault();
        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = 'move';
        }
    }

    public async onDrop(event: DragEvent, cell: any) {
        event.preventDefault();
        if (this.readOnly || !this.draggedEvent) return;

        const ev = this.draggedEvent;
        this.draggedEvent = null;

        const oldStart = ev.start.substring(0, 10);
        const oldEnd = ev.end.substring(0, 10);
        const newDate = cell.date;

        // 날짜 차이 계산
        const diffMs = new Date(newDate).getTime() - new Date(oldStart).getTime();
        const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));
        if (diffDays === 0) return;

        const startDate = new Date(ev.start.replace(' ', 'T'));
        const endDate = new Date(ev.end.replace(' ', 'T'));
        startDate.setDate(startDate.getDate() + diffDays);
        endDate.setDate(endDate.getDate() + diffDays);

        const pad = (n: number) => String(n).padStart(2, '0');
        const fmtDt = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;

        const { code } = await this.call("move", {
            id: ev.id,
            start: fmtDt(startDate),
            end: fmtDt(endDate)
        });
        if (code === 200) {
            await this.loadEvents();
        }
    }

    // ── 모달 ──

    public openCreateModal(date?: string) {
        if (this.readOnly) return;
        this.selectedEvent = null;
        this.isEditing = true;
        const d = date || this.formatDate(new Date());
        this.eventForm = {
            title: '',
            description: '',
            start_date: d,
            start_time: '09:00',
            end_date: d,
            end_time: '18:00',
            all_day: false,
            color: '#3b82f6',
            category_id: '',
            attendees: []
        };
        this.attendeeSearch = '';
        this.showAttendeeDropdown = false;
        this.showModal = true;
    }

    public async openEvent(event: any) {
        const { code, data } = await this.call("read", { id: event.id });
        if (code !== 200) return;
        this.selectedEvent = data.data;
        this.isEditing = false;
        this.eventForm = {
            title: this.selectedEvent.title,
            description: this.selectedEvent.description || '',
            start_date: this.selectedEvent.start.substring(0, 10),
            start_time: this.selectedEvent.start.substring(11, 16) || '09:00',
            end_date: this.selectedEvent.end.substring(0, 10),
            end_time: this.selectedEvent.end.substring(11, 16) || '18:00',
            all_day: this.selectedEvent.all_day,
            color: this.selectedEvent.color || '#3b82f6',
            category_id: this.selectedEvent.category_id || '',
            attendees: (this.selectedEvent.attendees || []).map((a: any) => a.user_id)
        };
        this.attendeeSearch = '';
        this.showAttendeeDropdown = false;
        this.showModal = true;
        await this.service.render();
    }

    public async startEdit() {
        this.isEditing = true;
        await this.service.render();
    }

    public async closeModal() {
        this.showModal = false;
        this.selectedEvent = null;
        this.isEditing = false;
        await this.service.render();
    }

    public async saveEvent() {
        const form = this.eventForm;
        if (!form.title || !form.title.trim()) {
            this.service.toast.error('제목을 입력해주세요');
            return;
        }

        const startStr = form.all_day
            ? `${form.start_date} 00:00:00`
            : `${form.start_date} ${form.start_time}:00`;
        const endStr = form.all_day
            ? `${form.end_date} 23:59:59`
            : `${form.end_date} ${form.end_time}:00`;

        const payload: any = {
            title: form.title.trim(),
            description: form.description,
            start: startStr,
            end: endStr,
            all_day: form.all_day,
            color: form.color,
            category_id: form.category_id || '',
            attendees: JSON.stringify(form.attendees || [])
        };

        let res: any;
        if (this.selectedEvent && this.selectedEvent.id) {
            payload.id = this.selectedEvent.id;
            res = await this.call("update", payload);
        } else {
            res = await this.call("create", payload);
        }

        if (res.code === 200) {
            this.service.toast.success('저장되었습니다');
            this.closeModal();
            await this.loadEvents();
        } else {
            this.service.toast.error(res.data?.message || '저장 중 오류가 발생했습니다');
        }
    }

    public async deleteEvent() {
        if (!this.selectedEvent?.id) return;
        const res = await this.service.alert.show({
            title: '일정 삭제',
            message: '이 일정을 삭제하시겠습니까?',
            cancel: '취소',
            actionBtn: 'error',
            action: '삭제',
            status: 'error'
        });
        if (!res) return;

        const { code } = await this.call("delete", { id: this.selectedEvent.id });
        if (code === 200) {
            this.service.toast.success('삭제되었습니다');
            this.closeModal();
            await this.loadEvents();
        }
    }

    public getEventColor(ev: any): string {
        if (ev.category && ev.category.color) return ev.category.color;
        return ev.color || '#3b82f6';
    }

    public getCategoryName(catId: string): string {
        if (!catId) return '';
        const cat = this.categories.find((c: any) => c.id === catId);
        return cat ? cat.name : '';
    }

    public get monthLabel(): string {
        return `${this.currentYear}년 ${this.currentMonth}월`;
    }

    public dayNames: string[] = ['일', '월', '화', '수', '목', '금', '토'];
}
