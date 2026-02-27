import { OnInit, OnDestroy, ElementRef, ViewChild } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Project } from '@wiz/libs/portal/works/project';

export class Component implements OnInit, OnDestroy {
    constructor(
        public service: Service,
        public project: Project,
        private elRef: ElementRef
    ) { }

    @ViewChild('autocompleteContainer') autocompleteContainer: ElementRef;

    public readOnly: boolean = true;
    public newuser: any = { role: 'user' };

    // 자동완성 관련
    public searchKeyword: string = '';
    public selectedUser: any = null;
    public showDropdown: boolean = false;
    public searching: boolean = false;
    public highlightIndex: number = -1;
    public searchResults: any = { internal: [], external: [] };
    private searchTimer: any = null;
    private clickOutsideHandler: any = null;

    public async ngOnInit() {
        await this.service.init();
        this.readOnly = !this.project.accessLevel(['admin', 'manager']);
        await this.project.member.load();

        // 외부 클릭 시 드롭다운 닫기
        this.clickOutsideHandler = (event: MouseEvent) => {
            const container = this.elRef.nativeElement.querySelector('[\\#autocompleteContainer]') || this.elRef.nativeElement;
            if (!container.contains(event.target)) {
                this.showDropdown = false;
                this.service.render();
            }
        };
        document.addEventListener('click', this.clickOutsideHandler);

        await this.service.render();
    }

    public ngOnDestroy() {
        if (this.clickOutsideHandler) {
            document.removeEventListener('click', this.clickOutsideHandler);
        }
        if (this.searchTimer) {
            clearTimeout(this.searchTimer);
        }
    }

    public async alert(message: string, status: any = "error", action: string = '확인', cancel: any = false) {
        return await this.service.alert.show({
            title: '',
            message: message,
            cancel: cancel,
            actionBtn: status,
            action: action,
            status: status
        });
    }

    // 자동완성: 입력 시 검색
    public onSearchInput() {
        if (this.searchTimer) clearTimeout(this.searchTimer);
        this.selectedUser = null;
        this.highlightIndex = -1;

        if (this.searchKeyword.trim().length < 1) {
            this.searchResults = { internal: [], external: [] };
            this.showDropdown = false;
            this.service.render();
            return;
        }

        this.searching = true;
        this.showDropdown = true;
        this.service.render();

        this.searchTimer = setTimeout(async () => {
            await this.searchUsers();
        }, 300);
    }

    // 포커스 시 상위 목록 표시
    public async onSearchFocus() {
        if (this.selectedUser) return;
        if (this.searchResults.internal.length > 0 || this.searchResults.external.length > 0) {
            this.showDropdown = true;
            await this.service.render();
            return;
        }
        await this.searchUsers();
    }

    // 키보드 네비게이션
    public onSearchKeydown(event: KeyboardEvent) {
        const totalItems = this.searchResults.internal.length + this.searchResults.external.length;
        if (!this.showDropdown || totalItems === 0) return;

        if (event.key === 'ArrowDown') {
            event.preventDefault();
            this.highlightIndex = (this.highlightIndex + 1) % totalItems;
            this.service.render();
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            this.highlightIndex = this.highlightIndex <= 0 ? totalItems - 1 : this.highlightIndex - 1;
            this.service.render();
        } else if (event.key === 'Enter') {
            event.preventDefault();
            if (this.highlightIndex >= 0) {
                const user = this.getUserByGlobalIndex(this.highlightIndex);
                if (user) this.selectUser(user);
            }
        } else if (event.key === 'Escape') {
            this.showDropdown = false;
            this.service.render();
        }
    }

    // 전체 인덱스 계산
    public getGlobalIndex(group: string, localIndex: number): number {
        if (group === 'internal') return localIndex;
        return this.searchResults.internal.length + localIndex;
    }

    // 전체 인덱스로 사용자 가져오기
    private getUserByGlobalIndex(index: number): any {
        const internalLen = this.searchResults.internal.length;
        if (index < internalLen) return this.searchResults.internal[index];
        return this.searchResults.external[index - internalLen] || null;
    }

    // 기존 멤버 이메일 목록 가져오기 (현재 프로젝트 실제 멤버만)
    private getExcludeEmails(): string {
        const members = this.project.member.list();
        return members
            .filter((m: any) => m.id != null)
            .map((m: any) => m.meta?.email)
            .filter((e: string) => !!e)
            .join(',');
    }

    // API 검색 호출
    private async searchUsers() {
        try {
            const exclude = this.getExcludeEmails();
            const res: any = await wiz.call("search", { keyword: this.searchKeyword.trim() || '', exclude });
            if (res.code === 200) {
                this.searchResults = {
                    internal: res.data.internal || [],
                    external: res.data.external || []
                };
            } else {
                this.searchResults = { internal: [], external: [] };
            }
        } catch (e) {
            this.searchResults = { internal: [], external: [] };
        }
        this.searching = false;
        this.showDropdown = true;
        await this.service.render();
    }

    // 사용자 선택
    public selectUser(user: any) {
        this.selectedUser = user;
        this.searchKeyword = user.name;
        this.showDropdown = false;
        this.highlightIndex = -1;
        this.service.render();
    }

    // 선택 해제
    public clearSelection() {
        this.selectedUser = null;
        this.searchKeyword = '';
        this.searchResults = { internal: [], external: [] };
        this.showDropdown = false;
        this.service.render();
    }

    public async roleChanged(user: any) {
        await this.project.member.update(user.user, user.role);
        await this.project.member.load();
        await this.service.render();
    }

    public async remove(user: any) {
        const res = await this.service.alert.show({
            title: "구성원 제외",
            status: "error",
            message: `"${user.meta.name}" 사용자를 이 프로젝트에서 제외하시겠습니까?`,
            action: "제외하기",
            actionBtn: "error",
            cancel: "cancel",
        });
        if (!res) return;
        await this.project.member.remove(user.user);
        await this.project.member.load();
        await this.service.render();
    }

    public async create() {
        if (!this.selectedUser) return;

        const email = this.selectedUser.email;
        const role = this.newuser.role;

        const { code, data } = await this.project.member.create(email, role);

        if (code != 200) {
            await this.service.error(data);
            return;
        }

        this.clearSelection();
        this.newuser = { role: 'user' };
        await this.project.member.load();
        await this.service.render();
    }

}
