import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    constructor(public service: Service) { }

    public data: any = {};
    public loginHistory: any = { rows: [], total: 0, page: 1 };
    public activeSessions: any[] = [];
    public passwordOpen: boolean = false;

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow(true, "/authenticate");
        await this.load();
    }

    public async alert(message: string, status: any = "error") {
        return await this.service.alert.show({
            title: '',
            message: message,
            cancel: false,
            actionBtn: status,
            action: "확인",
            status: status
        });
    }

    public async load() {
        const { data } = await wiz.call("session");
        let { user } = data;
        try {
            if (user.birth) user.birth = new Date(user.birth).format("yyyy-MM-dd");
        } catch (e) {
            user.birth = null;
        }

        this.data.user = user;
        this.data.password = {};

        await this.loadLoginHistory();
        await this.loadActiveSessions();
        await this.service.render();
    }

    public async update() {
        let userinfo = JSON.stringify(this.data.user);
        const { code, data } = await wiz.call("update", { userinfo });
        if (code == 200) {
            await this.alert("저장되었습니다", 'success');
            await this.load();
            await this.service.auth.init();
            return;
        }
        await this.alert("오류가 발생했습니다");
    }

    public async changePassword() {
        let pdata = JSON.parse(JSON.stringify(this.data.password));

        if (pdata.data != pdata.repeat) {
            await this.alert("변경 비밀번호를 다시 확인해주세요");
            return;
        }

        let pd: any = {};
        pd.current = this.service.auth.hash(pdata.current);
        pd.data = this.service.auth.hash(pdata.data);

        const { code, data } = await wiz.call("change_password", pd);

        if (code != 200) {
            await this.alert(data);
            return;
        }

        location.href = "/auth/logout";
    }

    public async updateIcon() {
        let res = await this.service.alert.show({
            title: '',
            message: '아이콘을 변경하시겠습니까?',
            cancel: '닫기',
            actionBtn: 'warning',
            action: '확인',
            status: 'warning'
        });

        if (!res) return;

        let icon = await this.service.file.read({ type: 'image', accept: 'image/*', width: 96, quality: 1 });
        this.data.user.profile_image = icon;
        await this.service.render();
    }

    public async deleteIcon() {
        this.data.user.profile_image = '';
        await this.service.render();
    }

    public async loadLoginHistory(page: number = 1) {
        const { code, data } = await wiz.call("login_history", { page, dump: 10 });
        if (code == 200) {
            this.loginHistory = { rows: data.rows, total: data.total, page: data.page };
        }
        await this.service.render();
    }

    public async loadActiveSessions() {
        const { code, data } = await wiz.call("active_sessions");
        if (code == 200) {
            this.activeSessions = data.sessions || [];
        }
        await this.service.render();
    }

    public async forceLogout(sessionId: string) {
        let res = await this.service.alert.show({
            title: '',
            message: '이 기기를 강제 로그아웃하시겠습니까?',
            cancel: '취소',
            actionBtn: 'error',
            action: '로그아웃',
            status: 'error'
        });

        if (!res) return;

        const { code, data } = await wiz.call("force_logout", { session_id: sessionId });
        if (code == 200) {
            await this.alert("강제 로그아웃 되었습니다", 'success');
            await this.loadActiveSessions();
        } else {
            await this.alert(data.message || "오류가 발생했습니다");
        }
    }

    public togglePassword() {
        this.passwordOpen = !this.passwordOpen;
        this.service.render();
    }

    public get historyTotalPages(): number {
        return Math.ceil(this.loginHistory.total / 10) || 1;
    }

    public async goHistoryPage(page: number) {
        if (page < 1 || page > this.historyTotalPages) return;
        await this.loadLoginHistory(page);
    }

    public methodLabel(method: string): string {
        const map: any = { password: '비밀번호', saml: 'SSO', otp: 'OTP' };
        return map[method] || method;
    }

    public statusLabel(status: string): string {
        return status === 'success' ? '성공' : '실패';
    }
}
