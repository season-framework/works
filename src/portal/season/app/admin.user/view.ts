import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public users: any[] = [];
    public selectedUser: any = null;
    public keyword: string = '';
    public filterMembership: string = '';
    public filterStatus: string = '';
    public searchFocused: boolean = false;
    public page: number = 1;
    public lastPage: number = 1;
    public total: number = 0;
    public dump: number = 20;

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.loadUsers();
    }

    public async loadUsers() {
        const params: any = {
            page: this.page,
            dump: this.dump,
        };
        if (this.keyword) params.keyword = this.keyword;
        if (this.filterMembership) params.membership = this.filterMembership;
        if (this.filterStatus) params.status = this.filterStatus;

        const { code, data } = await wiz.call("user_list", params);
        if (code === 200) {
            this.users = data.rows || [];
            this.total = data.total || 0;
            this.lastPage = data.last_page || 1;
            this.page = data.page || 1;
        }
        await this.service.render();
    }

    public async search() {
        this.page = 1;
        await this.loadUsers();
    }

    public async goPage(p: number) {
        if (p < 1 || p > this.lastPage) return;
        this.page = p;
        await this.loadUsers();
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
        const labels: any = { active: '활성', pending: '대기', block: '차단', deleted: '삭제됨' };
        return labels[status] || status;
    }

    public async selectUser(user: any) {
        const { code, data } = await wiz.call("user_get", { id: user.id });
        if (code === 200) {
            this.selectedUser = data;
        }
        await this.service.render();
    }

    public async saveUser() {
        if (!this.selectedUser) return;
        const { code } = await wiz.call("user_update", {
            id: this.selectedUser.id,
            name: this.selectedUser.name,
            email: this.selectedUser.email,
            membership: this.selectedUser.membership,
            status: this.selectedUser.status,
            mobile: this.selectedUser.mobile || '',
        });
        if (code === 200) {
            await this.service.alert.show({ title: '저장 완료', status: 'success', message: '사용자 정보가 저장되었습니다.', action: '확인' });
            await this.loadUsers();
        }
    }

    public async resetPassword() {
        if (!this.selectedUser) return;
        const res = await this.service.alert.show({
            title: '비밀번호 초기화',
            status: 'warning',
            message: '임시 비밀번호가 발급됩니다. 계속하시겠습니까?',
            action: '초기화',
            actionBtn: 'warning',
            cancel: '취소',
        });
        if (!res) return;
        const { code, data } = await wiz.call("user_reset_password", { id: this.selectedUser.id });
        if (code === 200) {
            await this.service.alert.show({
                title: '비밀번호 초기화 완료',
                status: 'success',
                message: `임시 비밀번호: ${data.password}`,
                action: '확인',
            });
        }
    }

    public async deleteUser() {
        if (!this.selectedUser) return;
        const res = await this.service.alert.show({
            title: '사용자 삭제',
            status: 'error',
            message: `${this.selectedUser.name} (${this.selectedUser.email})을 삭제하시겠습니까?`,
            action: '삭제',
            actionBtn: 'error',
            cancel: '취소',
        });
        if (!res) return;
        const { code } = await wiz.call("user_delete", { id: this.selectedUser.id });
        if (code === 200) {
            this.selectedUser = null;
            await this.loadUsers();
        }
    }

    public async switchToUser() {
        if (!this.selectedUser) return;
        const res = await this.service.alert.show({
            title: '사용자 전환',
            status: 'warning',
            message: `${this.selectedUser.name} (${this.selectedUser.email})으로 전환하시겠습니까?`,
            action: '전환',
            actionBtn: 'warning',
            cancel: '취소',
        });
        if (!res) return;
        const { code } = await wiz.call("user_switch", { id: this.selectedUser.id });
        if (code === 200) {
            location.href = '/';
        }
    }
}
